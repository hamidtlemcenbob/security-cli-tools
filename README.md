# Ethical Hacker Toolkit — CLI Security Tools

[![GitHub Release](https://img.shields.io/github/v/release/hamidtlemcenbob/security-cli-tools)](https://github.com/hamidtlemcenbob/security-cli-tools/releases)
[![Python](https://img.shields.io/badge/python-3.6+-green)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/hamidtlemcenbob/security-cli-tools)](https://github.com/hamidtlemcenbob/security-cli-tools/stargazers)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macOS%20%7C%20windows-lightgrey)]()

14 professional CLI security auditing tools for penetration testers, bug bounty hunters, and security researchers. **Zero dependencies beyond Python 3.**

## Tools

| # | Tool | Description | Price |
|---|------|-------------|-------|
| 1 | **Website Security Checker** | Security headers, tech stack, vuln detection | $5 |
| 2 | **Port Scanner** | Multi-threaded TCP (25 common ports) | $5 |
| 3 | **SSL Certificate Inspector** | TLS/SSL certificate details & cipher analysis | $5 |
| 4 | **DNS Lookup Tool** | A, AAAA, MX, NS, TXT, CNAME, SOA records | $5 |
| 5 | **HTTP Header Inspector** | HSTS, CSP, X-Frame-Options, X-Content-Type-Options | $5 |
| 6 | **Subdomain Finder** | 50+ common subdomain patterns | $5 |
| 7 | **Log Analyzer** | SQLi, XSS, brute force attack detection | $5 |
| 8 | **SSL Cert Watcher** | Multi-domain certificate expiry monitoring | $5 |
| 9 | **Password Auditor** | Entropy, strength, crack time estimation | $5 |
| 10 | **File Integrity Monitor** | SHA-256 file change tracking | $5 |
| 11 | **WHOIS Lookup** | RDAP domain registration info | $5 |
| 12 | **HTTP Benchmarker** | Response time statistics (min, max, avg, stddev) | $5 |
| 13 | **URL Extractor** | Web page link & resource discovery | $5 |
| 14 | **File Hash Checker** | MD5, SHA-1, SHA-256, SHA-512 | $5 |
| — | **Bundle (All 14)** | Complete toolkit — 14 tools for price of 4 | **$19.99** |

## Quick Start

```bash
# Website security audit
python3 site-checker.py example.com

# Port scan
python3 port-scan.py 10.0.0.1

# SSL inspection
python3 ssl-check.py example.com

# DNS records
python3 dns-lookup.py example.com

# HTTP security headers
python3 header-check.py https://example.com

# Subdomain enumeration
python3 sub-find.py example.com

# Certificate expiry monitor
python3 cert-watch.py example.com google.com github.com

# Password strength audit
python3 pass-audit.py MyP@ssw0rd123

# Log analysis
python3 log-analyzer.py access.log

# File integrity check
python3 hash-check.py important.pdf
```

All tools output structured **JSON**.

## Example Output

```json
{
  "domain": "example.com",
  "protocol": "TLSv1.3",
  "cipher": ["TLS_AES_256_GCM_SHA384", "TLSv1.3", 256],
  "issuer": {},
  "expiry": null
}
```

## Why These Tools?

- **Zero dependencies** — Pure Python 3, works anywhere Python runs
- **Fast** — Multi-threaded scanning
- **Portable** — Linux, macOS, Windows
- **Scriptable** — JSON output for CI/CD pipelines
- **Privacy-first** — No telemetry, no cloud, no accounts

## How to Buy

### Option 1: USDT (BEP-20)
Send USDT to: `0xed7881bc052e497efd44ba49558111e6ff1f36ff`
Network: **BSC (BEP-20)**
Email benslimanmalek329@gmail.com with transaction hash to receive files.

### Option 2: Binance Pay
https://s.binance.com/npzZMIWV

### Option 3: Gumroad
https://bensliman71.gumroad.com

## Links

- **Store:** https://tinyurl.com/2bsw5tx2
- **GitHub:** https://github.com/hamidtlemcenbob/security-cli-tools
- **Releases:** https://github.com/hamidtlemcenbob/security-cli-tools/releases
- **Download:** [ethical-hacker-toolkit-v1.0.0.zip](https://github.com/hamidtlemcenbob/security-cli-tools/releases/download/v1.0.0/ethical-hacker-toolkit-v1.0.0.zip)

## License

MIT — free to use, modify, and redistribute.
