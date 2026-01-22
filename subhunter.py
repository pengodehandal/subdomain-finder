#!/usr/bin/env python3
"""
Mass Subdomain Finder using Live Browser (Playwright)
Website: https://subdomainfinder.c99.nl/
FIXED VERSION - Updated selectors for 2024/2025
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
║                      [FIXED VERSION]                      ║
╚═══════════════════════════════════════════════════════════╝
{Colors.RESET}
    {Colors.YELLOW}[*] Website: subdomainfinder.c99.nl{Colors.RESET}
    {Colors.YELLOW}[*] Updated selectors for 2024/2025{Colors.RESET}
"""
    print(banner)

async def find_subdomains(domain: str, page, all_subdomains: list, output_file: str):
    """Scan single domain for subdomains"""
    print(f"\n{Colors.YELLOW}[*] Scanning: {domain}{Colors.RESET}")
    
    # Extract base domain for filtering
    base_domain = domain.lower().strip()
    
    try:
        # Navigate to the website
        await page.goto("https://subdomainfinder.c99.nl/", wait_until="networkidle", timeout=60000)
        print(f"{Colors.GREEN}[+] Page loaded successfully{Colors.RESET}")
        
        # Wait for the NEW input field selector
        await page.wait_for_selector('input#cdomain', timeout=30000)
        print(f"{Colors.GREEN}[+] Found input field: input#cdomain{Colors.RESET}")
        
        # Clear and fill the domain input
        await page.fill('input#cdomain', '')
        await page.fill('input#cdomain', domain)
        print(f"{Colors.GREEN}[+] Domain entered: {domain}{Colors.RESET}")
        
        # Small delay before clicking
        await asyncio.sleep(1)
        
        # Click the scan button - try multiple selectors
        scan_clicked = False
        scan_selectors = [
            'button:has-text("Start Scan")',
            'button:has-text("Scan")',
            'button[type="submit"]',
            'input[type="submit"]',
            '#scan_subdomains',
            '.btn-primary',
            'button.btn'
        ]
        
        for selector in scan_selectors:
            try:
                btn = await page.query_selector(selector)
                if btn:
                    await btn.click()
                    print(f"{Colors.GREEN}[+] Clicked scan button: {selector}{Colors.RESET}")
                    scan_clicked = True
                    break
            except:
                continue
        
        if not scan_clicked:
            # Fallback: press Enter on the input field
            await page.press('input#cdomain', 'Enter')
            print(f"{Colors.YELLOW}[*] Pressed Enter to submit{Colors.RESET}")
        
        print(f"{Colors.CYAN}[*] Scan started... waiting for results (max 2 min){Colors.RESET}")
        
        # Wait for results - multiple possible indicators
        result_found = False
        result_selectors = [
            'span[onclick*="copyAllSubdomains"]',
            'table tbody tr',
            '.result-table',
            '#results',
            'table tr td'
        ]
        
        for selector in result_selectors:
            try:
                await page.wait_for_selector(selector, timeout=120000)
                print(f"{Colors.GREEN}[+] Results indicator found: {selector}{Colors.RESET}")
                result_found = True
                break
            except:
                continue
        
        if not result_found:
            print(f"{Colors.YELLOW}[!] Timeout waiting for results, checking anyway...{Colors.RESET}")
        
        # Extra delay to ensure everything is loaded
        await asyncio.sleep(5)
        
        # Extract subdomains
        print(f"{Colors.CYAN}[*] Extracting subdomains...{Colors.RESET}")
        
        subdomains = await page.evaluate('''
            (baseDomain) => {
                let subs = [];
                
                // Method 1: Check for data in result table
                let tables = document.querySelectorAll('table');
                tables.forEach(table => {
                    let rows = table.querySelectorAll('tbody tr, tr');
                    rows.forEach((row, idx) => {
                        let cells = row.querySelectorAll('td');
                        if (cells.length >= 1) {
                            let text = cells[0].innerText.trim().toLowerCase();
                            // Validate it's a subdomain
                            if (text && 
                                text.includes('.') && 
                                text.endsWith(baseDomain) &&
                                !text.match(/^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}$/) &&
                                !text.toLowerCase().includes('subdomain') &&
                                text.length > 3) {
                                subs.push(text);
                            }
                        }
                    });
                });
                
                // Method 2: Look for links containing the domain
                if (subs.length === 0) {
                    let links = document.querySelectorAll('a');
                    links.forEach(link => {
                        let text = link.innerText.trim().toLowerCase();
                        if (text.endsWith(baseDomain) && 
                            text.includes('.') &&
                            !text.match(/^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}$/)) {
                            subs.push(text);
                        }
                    });
                }
                
                // Method 3: Scan body text for domain patterns
                if (subs.length === 0) {
                    let body = document.body.innerText;
                    let regex = new RegExp('[a-zA-Z0-9][a-zA-Z0-9.-]*\\\\.' + baseDomain.replace('.', '\\\\.'), 'gi');
                    let matches = body.match(regex);
                    if (matches) {
                        matches.forEach(m => {
                            let clean = m.toLowerCase();
                            if (!clean.match(/^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}$/)) {
                                subs.push(clean);
                            }
                        });
                    }
                }
                
                return [...new Set(subs)];
            }
        ''', base_domain)
        
        if subdomains:
            print(f"{Colors.GREEN}[+] Found {len(subdomains)} subdomains for {domain}{Colors.RESET}")
            for sub in subdomains:
                print(f"    {Colors.CYAN}→ {sub}{Colors.RESET}")
            all_subdomains.extend(subdomains)
            
            # REAL-TIME SAVE
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
    for d in domains[:10]:  # Show first 10 only
        print(f"    {Colors.CYAN}• {d}{Colors.RESET}")
    if len(domains) > 10:
        print(f"    {Colors.CYAN}• ... and {len(domains)-10} more{Colors.RESET}")
    
    # Get output file
    print(f"\n{Colors.CYAN}[?] Enter output file path (default: sublist.txt):{Colors.RESET}")
    output_file = input(f"{Colors.BOLD}>>> {Colors.RESET}").strip() or "sublist.txt"
    
    all_subdomains = []
    
    # Clear/create output file at start
    with open(output_file, 'w') as f:
        f.write('')
    print(f"{Colors.GREEN}[+] Output file ready: {output_file}{Colors.RESET}")
    
    print(f"\n{Colors.YELLOW}[*] Starting browser (visible mode for captcha handling)...{Colors.RESET}")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        page = await context.new_page()
        
        print(f"{Colors.GREEN}[+] Browser launched!{Colors.RESET}")
        print(f"{Colors.YELLOW}[!] If captcha appears, solve it manually{Colors.RESET}")
        
        for i, domain in enumerate(domains, 1):
            print(f"\n{Colors.BOLD}{'='*50}{Colors.RESET}")
            print(f"{Colors.CYAN}[{i}/{len(domains)}] Processing: {domain}{Colors.RESET}")
            print(f"{Colors.BOLD}{'='*50}{Colors.RESET}")
            
            await find_subdomains(domain, page, all_subdomains, output_file)
            
            # Small delay between scans to avoid rate limiting
            if i < len(domains):
                print(f"{Colors.YELLOW}[*] Waiting 2 seconds before next scan...{Colors.RESET}")
                await asyncio.sleep(2)
        
        await browser.close()
    
    # Final summary
    if all_subdomains:
        with open(output_file, 'r') as f:
            saved_subs = list(set([line.strip() for line in f if line.strip()]))
        saved_subs.sort()
        
        with open(output_file, 'w') as f:
            for sub in saved_subs:
                f.write(sub + '\n')
        
        print(f"\n{Colors.GREEN}{'='*50}{Colors.RESET}")
        print(f"{Colors.GREEN}[+] SCAN COMPLETE!{Colors.RESET}")
        print(f"{Colors.GREEN}[+] Total unique subdomains: {len(saved_subs)}{Colors.RESET}")
        print(f"{Colors.GREEN}[+] Results saved to: {output_file}{Colors.RESET}")
        print(f"{Colors.GREEN}{'='*50}{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}[!] No subdomains found for any domain{Colors.RESET}")

if __name__ == "__main__":
    asyncio.run(main())
