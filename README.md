# Vivastreet Reposter Bot

A Python bot that automates login, bypasses Cloudflare, and reposts ads on **Vivastreet** using [DrissionPage](https://github.com/g1879/DrissionPage) and the [CloudflareBypassForScraping](https://github.com/sarperavci/CloudflareBypassForScraping) library.

## ✨ Features

- 🔑 Auto-login with email & password
- 🍪 Saves and reloads cookies
- 🛡️ Cloudflare Turnstile bypass via CloudflareBypassForScraping
- 🔄 Automatic ad reposting loop
- ⏳ Interval-based reposting (default 15 min)
- 🚪 Graceful shutdown on exit signals (Ctrl+C / kill)

## 📦 Requirements

- Python 3.9+
- [DrissionPage](https://pypi.org/project/DrissionPage/)
- [CloudflareBypassForScraping](https://github.com/sarperavci/CloudflareBypassForScraping)

Install dependencies:

```bash
pip install drissionpage
```

## ⚙️ Configuration

Edit your credentials inside the script:

```python
EMAIL = "youremail@example.com"
PASSWORD = "yourpassword"
```

## ▶️ Usage

Run the bot:

```bash
python vivastreet_reposter.py
```

The bot will:

1. Attempt login (or reuse cookies)
2. Accept site disclaimers automatically
3. Bypass Cloudflare verification
4. Repost all available ads
5. Sleep, then repeat

## 🛑 Exit

Press `Ctrl+C` or send a `SIGTERM` — the bot will close the browser automatically.

## ⚠️ Disclaimer

This project is for **educational purposes only**.\
Use at your own risk — automating Vivastreet may violate their Terms of Service.

