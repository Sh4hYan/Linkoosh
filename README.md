# Linkoosh

**Linkoosh** – A powerful Telegram bot to deliver high-quality videos, audio, and media from Instagram, YouTube, SoundCloud, and more. Reliable, Free, Fast, and Easy to Use! 🚀

---

## Features

- 📸 Download videos and photos from **Instagram** (posts, reels, IGTV, live links)  
- ▶️ Download videos and audio from **YouTube** (videos, shorts, live streams, playlists)  
- 🎵 Download tracks from **SoundCloud** (support for short links: `on.soundcloud.com`)  
- ⚡ Fast, reliable, and easy to use  
- 📤 Supports streaming files directly in Telegram  
- 🗑️ Automatic cleanup of temporary files after download  
- ❌ Works without FFMPEG  

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
python bot.py
```

**How to use:**

1. Start the bot: `/start`  
2. Send a link from **Instagram**, **YouTube**, or **SoundCloud**  
3. The bot will download and send the media directly to you  
4. Only one download at a time per chat to prevent overload  

---

## Supported Links

**📸 Instagram:**  
- Posts: `https://www.instagram.com/p/...`  
- Reels: `https://www.instagram.com/reel/...`  
- IGTV: `https://www.instagram.com/tv/...`  
- Live: `https://www.instagram.com/live/...`  

**▶️ YouTube:**  
- Videos: `https://www.youtube.com/watch?v=...`  
- Shorts: `https://www.youtube.com/shorts/...`  
- Live streams: `https://www.youtube.com/live/...`  
- Playlists: `https://www.youtube.com/playlist?list=...`  
- Short links: `https://youtu.be/...`  

**🎵 SoundCloud:**  
- Normal links: `https://soundcloud.com/...`  
- Short links: `https://on.soundcloud.com/...`  
- Mobile links: `https://m.soundcloud.com/...`  
- Other subdomains: `https://www.soundcloud.com/...`  

---

## Upcoming Features

- 🎶 Spotify downloads  
- 📹 Support for other media platforms  
- 👥 Admin panel for channel/group controls  
- ⚡ Improved performance and multi-download support  

> This is the **initial release**! Many more exciting features are coming soon.

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
