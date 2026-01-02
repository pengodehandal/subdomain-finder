# 🔍 SubHunter - Mass Subdomain Discovery Tool

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Windows-blue?style=for-the-badge&logo=windows" alt="Windows"/>
  <img src="https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python" alt="Python"/>
  <img src="https://img.shields.io/badge/Browser-Chromium-orange?style=for-the-badge&logo=googlechrome" alt="Chromium"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License"/>
</p>

<p align="center">
  <b>Automated mass subdomain finder using live browser automation</b><br>
  <i>Bypass captcha manually, real-time results saving, clean output</i>
</p>

---

## 🌐 Language / Bahasa

- [English](#english)
- [Bahasa Indonesia](#bahasa-indonesia)

---

# English

## 📖 Description

**SubHunter** is a powerful mass subdomain discovery tool that uses live browser automation (Playwright) to scan multiple domains for subdomains. Unlike traditional tools that use HTTP requests, SubHunter opens a real browser window, allowing you to manually solve CAPTCHAs when they appear.

### ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🖥️ **Live Browser** | Uses real Chromium browser - you can see everything happening |
| 🤖 **CAPTCHA Friendly** | Manually solve CAPTCHAs in the browser when they appear |
| 💾 **Real-time Saving** | Results are saved immediately - no data loss if script crashes |
| 🎯 **Smart Filtering** | Only captures subdomains of your target domain (no junk data) |
| 📋 **Mass Scanning** | Scan hundreds of domains from a single text file |
| 🧹 **Clean Output** | Automatically removes duplicates and sorts results |

## ⚠️ Requirements

- **Operating System:** Windows 10/11 only
- **Python:** Version 3.8 or higher
- **Internet:** Stable connection required

## 🚀 Installation

### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. During installation, **CHECK** ✅ "Add Python to PATH"
3. Click "Install Now"

### Step 2: Download SubHunter

**Option A: Using Git**
```bash
git clone https://github.com/pengodehandal/subdomain-finder.git
cd subdomain-finder
```

**Option B: Download ZIP**
1. Click the green "Code" button above
2. Select "Download ZIP"
3. Extract the ZIP file

### Step 3: Install Dependencies

Open **Command Prompt** or **PowerShell** in the SubHunter folder:

```bash
pip install playwright
```

Or simply double-click `install.bat`

### Step 4: Install Browser

```bash
playwright install chromium
```

This is included in `install.bat` if you used that method.

## 📝 Usage

### Method 1: Using run.bat (Easy)

1. Double-click `run.bat`
2. Follow the prompts

### Method 2: Using Command Line

```bash
python subhunter.py
```

### Step-by-Step Guide

#### 1. Prepare Domain List

Create a text file (e.g., `domains.txt`) with one domain per line:

```
example.com
target.org
company.co.id
university.ac.id
```

#### 2. Run SubHunter

```bash
python subhunter.py
```

#### 3. Follow the Prompts

```
╔═══════════════════════════════════════════════════════════╗
║            SUBHUNTER - Mass Subdomain Discovery           ║
║                   Live Browser Edition                    ║
╚═══════════════════════════════════════════════════════════╝

[?] Enter path to domain list file (one domain per line):
>>> domains.txt

[?] Enter output file path (default: sublist.txt):
>>> results.txt
```

#### 4. Handle CAPTCHA (if appears)

When a CAPTCHA appears in the browser window, simply solve it manually. The script will wait and continue automatically.

#### 5. Get Results

Results are saved to your specified output file in real-time:

```
mail.example.com
admin.example.com
api.example.com
dev.example.com
```

## 📸 Example Output

```
[+] Found 212 subdomains for ut.ac.id
    → akademik.ut.ac.id
    → alumni.ut.ac.id
    → bandung.ut.ac.id
    → banjarmasin.ut.ac.id
    → batam.ut.ac.id
    ...
[+] Saved 212 subdomains to sublist.txt

==================================================
[2/5] Processing: undip.ac.id
==================================================
```

## ⚙️ How It Works

```
┌─────────────────┐
│  Domain List    │
│  (domains.txt)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Open Browser   │
│  (Chromium)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Navigate to    │
│  c99.nl scanner │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Input Domain   │──────► CAPTCHA? ──► Solve Manually
│  Click Scan     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Extract        │
│  Subdomains     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Save to File   │──────► Real-time!
│  (Immediately)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Next Domain    │──────► Repeat
└─────────────────┘
```

## ❓ Troubleshooting

| Problem | Solution |
|---------|----------|
| `python is not recognized` | Reinstall Python and check "Add to PATH" |
| `playwright not found` | Run `pip install playwright` |
| Browser doesn't open | Run `playwright install chromium` |
| No subdomains found | Check your internet connection, or the website may be blocking requests |
| Script crashes | Your results are safe! Check the output file |

## 🛡️ Disclaimer

This tool is for **educational and authorized security testing purposes only**. Always obtain proper authorization before scanning any domains you don't own. The developers are not responsible for any misuse of this tool.

---

# Bahasa Indonesia

## 📖 Deskripsi

**SubHunter** adalah tool pencari subdomain massal yang powerful menggunakan otomasi browser langsung (Playwright). Berbeda dengan tool tradisional yang pakai HTTP requests, SubHunter membuka jendela browser asli, sehingga kamu bisa solve CAPTCHA secara manual ketika muncul.

### ✨ Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| 🖥️ **Live Browser** | Pakai browser Chromium asli - kamu bisa lihat semua yang terjadi |
| 🤖 **CAPTCHA Friendly** | Solve CAPTCHA manual di browser ketika muncul |
| 💾 **Real-time Saving** | Hasil langsung disimpan - ga ada data hilang kalau script crash |
| 🎯 **Smart Filtering** | Cuma ambil subdomain dari target domain (ga ada data sampah) |
| 📋 **Mass Scanning** | Scan ratusan domain dari satu file text |
| 🧹 **Clean Output** | Otomatis hapus duplikat dan urutkan hasil |

## ⚠️ Persyaratan

- **Sistem Operasi:** Khusus Windows 10/11
- **Python:** Versi 3.8 atau lebih tinggi
- **Internet:** Butuh koneksi stabil

## 🚀 Instalasi

### Langkah 1: Install Python

1. Download Python dari [python.org](https://www.python.org/downloads/)
2. Saat instalasi, **CENTANG** ✅ "Add Python to PATH"
3. Klik "Install Now"

### Langkah 2: Download SubHunter

**Opsi A: Pakai Git**
```bash
git clone https://github.com/pengodehandal/subdomain-finder.git
cd subdomain-finder
```

**Opsi B: Download ZIP**
1. Klik tombol hijau "Code" di atas
2. Pilih "Download ZIP"
3. Extract file ZIP nya

### Langkah 3: Install Dependencies

Buka **Command Prompt** atau **PowerShell** di folder SubHunter:

```bash
pip install playwright
```

Atau tinggal double-click `install.bat`

### Langkah 4: Install Browser

```bash
playwright install chromium
```

Ini sudah termasuk di `install.bat` kalau kamu pakai cara itu.

## 📝 Cara Pakai

### Cara 1: Pakai run.bat (Gampang)

1. Double-click `run.bat`
2. Ikuti petunjuknya

### Cara 2: Pakai Command Line

```bash
python subhunter.py
```

### Panduan Langkah demi Langkah

#### 1. Siapkan List Domain

Buat file text (contoh: `domains.txt`) dengan satu domain per baris:

```
example.com
target.org
company.co.id
university.ac.id
```

#### 2. Jalankan SubHunter

```bash
python subhunter.py
```

#### 3. Ikuti Instruksi

```
╔═══════════════════════════════════════════════════════════╗
║            SUBHUNTER - Mass Subdomain Discovery           ║
║                   Live Browser Edition                    ║
╚═══════════════════════════════════════════════════════════╝

[?] Enter path to domain list file (one domain per line):
>>> domains.txt

[?] Enter output file path (default: sublist.txt):
>>> results.txt
```

#### 4. Handle CAPTCHA (kalau muncul)

Ketika CAPTCHA muncul di jendela browser, tinggal solve manual aja. Script akan nunggu dan lanjut otomatis.

#### 5. Ambil Hasil

Hasil disimpan ke file output secara real-time:

```
mail.example.com
admin.example.com
api.example.com
dev.example.com
```

## 📸 Contoh Output

```
[+] Found 212 subdomains for ut.ac.id
    → akademik.ut.ac.id
    → alumni.ut.ac.id
    → bandung.ut.ac.id
    → banjarmasin.ut.ac.id
    → batam.ut.ac.id
    ...
[+] Saved 212 subdomains to sublist.txt

==================================================
[2/5] Processing: undip.ac.id
==================================================
```

## ⚙️ Cara Kerja

```
┌─────────────────┐
│  List Domain    │
│  (domains.txt)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Buka Browser   │
│  (Chromium)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Buka website   │
│  c99.nl scanner │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Input Domain   │──────► CAPTCHA? ──► Solve Manual
│  Klik Scan      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Ambil          │
│  Subdomain      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Simpan ke File │──────► Real-time!
│  (Langsung)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Domain         │──────► Ulangi
│  Berikutnya     │
└─────────────────┘
```

## ❓ Troubleshooting / Solusi Masalah

| Masalah | Solusi |
|---------|--------|
| `python is not recognized` | Install ulang Python dan centang "Add to PATH" |
| `playwright not found` | Jalankan `pip install playwright` |
| Browser ga kebuka | Jalankan `playwright install chromium` |
| Ga nemu subdomain | Cek koneksi internet, atau website mungkin blocking |
| Script crash | Hasil aman! Cek file output nya |

## 🛡️ Disclaimer

Tool ini hanya untuk **tujuan edukasi dan pengujian keamanan yang sudah diizinkan**. Selalu dapatkan izin yang tepat sebelum scanning domain yang bukan milik kamu. Developer tidak bertanggung jawab atas penyalahgunaan tool ini.

---

## 📄 License

MIT License - bebas dipakai dan dimodifikasi!

## 🤝 Contributing

Pull requests welcome! Untuk perubahan besar, silakan buka issue dulu.

## ⭐ Star Repo Ini!

Kalau tool ini berguna, kasih bintang ya! ⭐

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/pengodehandal">@pengodehandal</a>
</p>
