#!/usr/bin/env python3
"""
Mass Subdomain Finder using Live Browser (Playwright)
Website: https://subdomainfinder.c99.nl/
"""

import asyncio
import os
from playwright.async_api import async_playwright

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════╗
║            SUBHUNTER - Mass Subdomain Discovery           ║
║                   Live Browser Edition                    ║
╚═══════════════════════════════════════════════════════════╝
{Colors.RESET}
    {Colors.YELLOW}[*] GitHub: github.com/pengodehandal/subdomain-finder{Colors.RESET}
    {Colors.YELLOW}[*] Platform: Windows Only{Colors.RESET}
"""
    print(banner)

async def find_subdomains(domain: str, page, all_subdomains: list, output_file: str):
    """Scan single domain for subdomains"""
    print(f"\n{Colors.YELLOW}[*] Scanning: {domain}{Colors.RESET}")
    
    # Extract base domain for filtering (e.g., "undip.ac.id" from input)
    base_domain = domain.lower().strip()
    
    try:
        # Navigate to the website
        await page.goto("https://subdomainfinder.c99.nl/", wait_until="networkidle", timeout=60000)
        print(f"{Colors.GREEN}[+] Page loaded successfully{Colors.RESET}")
        
        # Wait for input field
        await page.wait_for_selector('input#domain9', timeout=30000)
        print(f"{Colors.GREEN}[+] Found input field: input#domain9{Colors.RESET}")
        
        # Clear and fill the domain input
        await page.fill('input#domain9', '')
        await page.fill('input#domain9', domain)
        print(f"{Colors.GREEN}[+] Domain entered: {domain}{Colors.RESET}")
        
        # Click the scan button
        await page.click('button#scan_subdomains')
        print(f"{Colors.CYAN}[*] Scan started... waiting for results{Colors.RESET}")
        
        # Wait for results - look for the copy button which appears when results are ready
        # This might take a while depending on the domain
        try:
            await page.wait_for_selector('span[onclick*="copyAllSubdomains"]', timeout=120000)
            print(f"{Colors.GREEN}[+] Results loaded!{Colors.RESET}")
        except:
            print(f"{Colors.YELLOW}[!] Timeout waiting for results, checking if any subdomains found...{Colors.RESET}")
        
        # Small delay to ensure everything is loaded
        await asyncio.sleep(3)
        
        # Debug: Print table structure to console
        print(f"{Colors.CYAN}[DEBUG] Inspecting page structure...{Colors.RESET}")
        table_info = await page.evaluate('''
            () => {
                let info = [];
                let tables = document.querySelectorAll('table');
                tables.forEach((table, idx) => {
                    let rows = table.querySelectorAll('tr');
                    if (rows.length > 0) {
                        let firstRow = rows[0];
                        let cells = firstRow.querySelectorAll('td, th');
                        let headers = Array.from(cells).map(c => c.innerText.trim().substring(0, 30));
                        info.push(`Table ${idx}: ${rows.length} rows, headers: ${headers.join(' | ')}`);
                    }
                });
                return info.join('\\n');
            }
        ''')
        if table_info:
            print(f"{Colors.CYAN}[DEBUG] {table_info}{Colors.RESET}")
        
        # METHOD 1: Try to get subdomains via the copyAllSubdomains function
        # This extracts what the "Copy to clipboard" button would copy
        print(f"{Colors.CYAN}[*] Trying to extract subdomains...{Colors.RESET}")
        
        # First, let's intercept what copyAllSubdomains would copy
        # by overriding the clipboard API temporarily
        subdomains = await page.evaluate('''
            (baseDomain) => {
                let subs = [];
                
                // Method A: Check for data in result table - specifically the Subdomain column (first column)
                let table = document.querySelector('table');
                if (table) {
                    let rows = table.querySelectorAll('tbody tr, tr');
                    rows.forEach((row, idx) => {
                        // Skip header row
                        let cells = row.querySelectorAll('td');
                        if (cells.length >= 1) {
                            let text = cells[0].innerText.trim().toLowerCase();
                            // Validate it's a subdomain, not IP, not empty, not header text
                            // AND must end with the base domain (filter out "Recent scans")
                            if (text && 
                                text.includes('.') && 
                                text.endsWith(baseDomain) &&
                                !text.match(/^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}$/) &&
                                !text.toLowerCase().includes('subdomain') &&
                                !text.toLowerCase().includes('cloudflare') &&
                                text.length > 3) {
                                subs.push(text);
                            }
                        }
                    });
                }
                
                // Method B: Look for the actual function and its data source
                // Some sites store subdomains in a JS variable
                if (subs.length === 0) {
                    // Try to find any array containing domain-like strings
                    let scripts = document.querySelectorAll('script');
                    scripts.forEach(script => {
                        let content = script.textContent || '';
                        // Look for arrays with subdomain patterns
                        let matches = content.match(/["']([a-zA-Z0-9][-a-zA-Z0-9]*\\.)+[a-zA-Z]{2,}["']/g);
                        if (matches) {
                            matches.forEach(m => {
                                let clean = m.replace(/["']/g, '').toLowerCase();
                                if (!clean.match(/^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}$/) &&
                                    clean.endsWith(baseDomain)) {
                                    subs.push(clean);
                                }
                            });
                        }
                    });
                }
                
                return [...new Set(subs)];
            }
        ''', base_domain)
        
        # If first method didn't work, try alternative methods
        if not subdomains:
            print(f"{Colors.YELLOW}[*] First method didn't work, trying alternatives...{Colors.RESET}")
            subdomains = await page.evaluate('''
                (baseDomain) => {
                    let subs = [];
                    
                    // Method: Scan all text looking for subdomain patterns
                    let body = document.body.innerText;
                    // Match patterns like: something.domain.tld
                    let lines = body.split('\\n');
                    lines.forEach(line => {
                        let parts = line.trim().split(/\\s+/);
                        parts.forEach(part => {
                            let lowerPart = part.toLowerCase();
                            // Check if it looks like a subdomain (has dots, not an IP)
                            // AND must end with base domain
                            if (lowerPart.includes('.') && 
                                lowerPart.endsWith(baseDomain) &&
                                !lowerPart.match(/^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}$/) &&
                                lowerPart.match(/^[a-zA-Z0-9][a-zA-Z0-9.-]*\\.[a-zA-Z]{2,}$/)) {
                                subs.push(lowerPart);
                            }
                        });
                    });
                    
                    return [...new Set(subs)];
                }
            ''', base_domain)
        
        if subdomains:
            print(f"{Colors.GREEN}[+] Found {len(subdomains)} subdomains for {domain}{Colors.RESET}")
            for sub in subdomains:
                print(f"    {Colors.CYAN}→ {sub}{Colors.RESET}")
            all_subdomains.extend(subdomains)
            
            # REAL-TIME SAVE - append to file immediately
            with open(output_file, 'a') as f:
                for sub in subdomains:
                    f.write(sub + '\n')
            print(f"{Colors.GREEN}[+] Saved {len(subdomains)} subdomains to {output_file}{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}[!] No subdomains found for {domain}{Colors.RESET}")
            
        return subdomains
        
    except Exception as e:
        print(f"{Colors.RED}[!] Error scanning {domain}: {str(e)}{Colors.RESET}")
        return []

async def main():
    print_banner()
    
    # Get domain list file from user
    print(f"{Colors.CYAN}[?] Enter path to domain list file (one domain per line):{Colors.RESET}")
    domain_file = input(f"{Colors.BOLD}>>> {Colors.RESET}").strip()
    
    # Check if file exists
    if not os.path.exists(domain_file):
        print(f"{Colors.RED}[!] File not found: {domain_file}{Colors.RESET}")
        return
    
    # Read domains from file
    with open(domain_file, 'r') as f:
        domains = [line.strip() for line in f if line.strip()]
    
    if not domains:
        print(f"{Colors.RED}[!] No domains found in file{Colors.RESET}")
        return
    
    print(f"\n{Colors.GREEN}[+] Loaded {len(domains)} domains{Colors.RESET}")
    for d in domains:
        print(f"    {Colors.CYAN}• {d}{Colors.RESET}")
    
    # Get output file
    print(f"\n{Colors.CYAN}[?] Enter output file path (default: sublist.txt):{Colors.RESET}")
    output_file = input(f"{Colors.BOLD}>>> {Colors.RESET}").strip() or "sublist.txt"
    
    all_subdomains = []
    
    # Clear/create output file at start
    with open(output_file, 'w') as f:
        f.write('')  # Clear file
    print(f"{Colors.GREEN}[+] Output file ready: {output_file}{Colors.RESET}")
    
    print(f"\n{Colors.YELLOW}[*] Starting browser (headless=False so you can see & handle captcha if needed)...{Colors.RESET}")
    
    async with async_playwright() as p:
        # Launch browser in headed mode so user can see and handle captcha
        browser = await p.chromium.launch(
            headless=False,  # Set to False so you can see the browser and handle captcha
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        page = await context.new_page()
        
        print(f"{Colors.GREEN}[+] Browser launched!{Colors.RESET}")
        print(f"{Colors.YELLOW}[!] If captcha appears, solve it manually in the browser window{Colors.RESET}")
        
        for i, domain in enumerate(domains, 1):
            print(f"\n{Colors.BOLD}{'='*50}{Colors.RESET}")
            print(f"{Colors.CYAN}[{i}/{len(domains)}] Processing: {domain}{Colors.RESET}")
            print(f"{Colors.BOLD}{'='*50}{Colors.RESET}")
            
            await find_subdomains(domain, page, all_subdomains, output_file)
        
        await browser.close()
    
    # Final summary and deduplication
    if all_subdomains:
        # Read file and remove duplicates
        with open(output_file, 'r') as f:
            saved_subs = list(set([line.strip() for line in f if line.strip()]))
        saved_subs.sort()
        
        # Write back deduplicated results
        with open(output_file, 'w') as f:
            for sub in saved_subs:
                f.write(sub + '\n')
        
        print(f"\n{Colors.GREEN}{'='*50}{Colors.RESET}")
        print(f"{Colors.GREEN}[+] SCAN COMPLETE!{Colors.RESET}")
        print(f"{Colors.GREEN}[+] Total unique subdomains: {len(saved_subs)}{Colors.RESET}")
        print(f"{Colors.GREEN}[+] Results saved to: {output_file}{Colors.RESET}")
        print(f"{Colors.GREEN}[+] (Results were saved in real-time){Colors.RESET}")
        print(f"{Colors.GREEN}{'='*50}{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}[!] No subdomains found for any domain{Colors.RESET}")

if __name__ == "__main__":
    asyncio.run(main())
