import time, random, asyncio

download_messages = [
    "⏳ Processing your request...",
    "⏳ Connecting to YouTube server...",
    "⏳ Checking the provided link...",
    "⏳ Finding the best quality...",
    "⏳ Starting the download...",
]

upload_messages = [
    "📤 Processing your download...",
    "📤 Enhancing your file...",
    "📤 Uploading in Telegram",
    "📤 Streaming your file in Telegram..."
]

final_messages = [
    "🎬 Final request...",
    "🎬 Final processing...",
    "🎬 Ready to send..."
]

# Reformat Size & Duration
def format_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.{decimal_places}f} {unit}"
        size /= 1024

def format_duration(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds} Seconds"
    minutes, sec = divmod(seconds, 60)
    return f"{minutes}m, {sec}s"


# Upload Progress
last_update_time = 0

async def upload_progress_callback(current, total, message):
    global last_update_time
    current_time = time.time()
    if current_time - last_update_time < 1:
        return
    last_update_time = current_time

    percentage = (current / total) * 100
    progress_bar = "⬢" * int(percentage / 5) + "⬡" * (20 - int(percentage / 5))
    
    try:
        await message.edit(
            f"📤 در حال آپلود به تلگرامتون...\n\n"
            f"{progress_bar}\n"
            f"📊 {percentage:.1f}% | {format_size(current)} / {format_size(total)}\n"
        )
    except:
        pass
    
    
    
    
# Download Progress Class
class DownloadProgress:
    def __init__(self, message, bot_loop):
        self.message = message
        self.bot_loop = bot_loop
        self.last_update = 0
        self.last_percent = -1
        self.stage_count = 0
        
    async def update_progress(self, text):
        try:
            await self.message.edit(text)
        except Exception as e:
            print(f"An Error Occurred During Upload {e}")
    
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded_bytes = d.get('downloaded_bytes', 0)
            
            if total_bytes and total_bytes > 0:
                percent = downloaded_bytes / total_bytes * 100
                current_time = time.time()
                
                eta_str = "Calculating..."
                
                eta = d.get('eta')
                if eta:
                    minutes, seconds = divmod(eta, 60)
                    seconds = round(seconds)
                    if minutes > 0:
                        eta_str = f"{minutes}m {seconds}s"
                    else:
                        eta_str = f"{seconds}s"
                    
                if abs(percent - self.last_percent) >= 1 or current_time - self.last_update > 3:
                    self.last_percent = percent
                    self.last_update = current_time
                    
                    if percent < 25 and self.stage_count == 0:
                        progress_text = random.choice(download_messages)
                        self.stage_count = 1
                    elif percent < 50 and self.stage_count == 1:
                        progress_text = random.choice(download_messages[2:])
                        self.stage_count = 2
                    elif percent < 75 and self.stage_count == 2:
                        progress_text = random.choice(upload_messages)
                        self.stage_count = 3
                    elif percent < 90 and self.stage_count == 3:
                        progress_text = random.choice(final_messages)
                        self.stage_count = 4
                    else:
                        progress_text = f"📉 Downloading: {percent:.1f}%"
                    
                    asyncio.run_coroutine_threadsafe(
                        self.update_progress(f"{progress_text} \n⏰ Remaining time: {eta_str}"), 
                        self.bot_loop
                    )
                    
        elif d['status'] == 'finished':
            asyncio.run_coroutine_threadsafe(
                self.update_progress("✅ Download completed! Processing file..."), 
                self.bot_loop
            )