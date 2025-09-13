# Linkoosh
> This is the **initial release**! Many more exciting features are coming soon. 🚦

## Features (Now)

- 📸🎵▶️ Download any audio, videos and photos from **Instagram**, **YouTube** and **SoundCloud**
- ⚡ Fast, reliable, and easy to use  
- 📤 Supports streaming files directly in Telegram
- ❌ Works without FFMPEG !!! 

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/Sh4hYan/Linkoosh.git
cd Linkoosh
```

2. **Create a virtual environment (recommended)**

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure your bot**

- Open `config.py`  
- Add your Telegram bot token, API ID, API HASH, and optionally CHANNEL ID or ADMINS:

```python
API_ID = 123456
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"
CHANNEL = None  # Optional
ADMINS = None   # Optional
```

---

## Usage

Run the bot:

```bash
python main.py
```
---

## Upcoming Features (Future)

- 🎶 Spotify downloads  
- 📹 Support for other media platforms  
- 👥 Admin panel for channel/group controls  
- ⚡ Improved performance and multi-download support  

---

## Notes

- All temporary files are automatically removed after download.  
- Keep `config.py` private and **never push your tokens to public repositories**.  
- For troubleshooting logs, check the console output.  
- Only **one active download per chat** is allowed at a time.  

---

## Contact & Support

- Telegram: [@idleer](https://t.me/idleer) 📲  
- Stay tuned for updates and new features!  

---

## Contribution

Contributions are welcome! Feel free to fork, submit issues, or open pull requests.

---

**Enjoy downloading with Linkoosh!** 😎
