import os, asyncio, shutil, random
from telethon import events, types
from downloader import INSTAGRAM_DOWNLOADER, YT_DOWNLOADER
from tools import upload_progress_callback, DownloadProgress
from tools import format_size, format_duration
from config import CHANNEL # If use

active_downloads = {}

# All Handlers After Start
def start_handlers(bot):
    @bot.on(events.NewMessage(pattern=r"(?i)/start$"))
    async def start(event):
        welcome_message = random.choice([
            f"سلام {event.sender.first_name} 👋🏻 یک لینک از اینستاگرام، یوتیوب، اسپاتیفای، ساوندکلاد و... بهم بده، من فایلشو برات می‌فرستم!",
            f"درود {event.sender.first_name} ✨\nمن یک ربات دانلودرم. کافیه یک لینک بدی (اینستاگرام، یوتیوب، اسپاتیفای و..)، فایلش رو بهت میدم!",
        ])
        await event.reply(welcome_message)
        
    @bot.on(events.NewMessage(pattern =
    r"(https?://(?:www\.)?(?:instagram\.com|instagr\.am)/[^\s]+"
    r"|https?://(?:www\.)?(?:youtube\.com/(?:watch\?v=|shorts/|live/|playlist\?list=)|youtu\.be/)[^\s]+"
    r"|https?://(?:www\.|m\.|on\.|w\.)?soundcloud\.com/[^\s]+)"
))
    
    async def handler(event):
        link = event.text.strip()

        if event.chat_id in active_downloads:
            await event.respond("⛔️ شما در حال حاضر یک دانلود در حال انجام دارید! صبر کنید تا قبلی تمام شود.")
            return

        active_downloads[event.chat_id] = True
        
        message = random.choice([
            "🔍 شروع دانلود لینک شما...",
            "📕 در حال دریافت اطلاعات لینک...",
            "⏳ در حال پردازش لینک شما...",
            "🗳 در حال آماده‌سازی برای دانلود...",
        ])
        message = await event.reply(message)

        temp_dir  = None
        DOWNLOADED = False
        
        try:
            if "instagram.com" in link:
                await message.edit("📸 در حال دانلود از سرورهای اینستاگرام...")
                progress = DownloadProgress(message, bot.loop)
                files, thumb_path = await asyncio.get_event_loop().run_in_executor(
                    None, lambda: INSTAGRAM_DOWNLOADER(link, progress.progress_hook)
                )
                if not files:
                    print(f"[❌ Failed, None File] Link sent by {event.sender.first_name}")
                    await message.edit("❌ هیچ فایلی از اینستاگرام پیدا نشد، یک لینک معتبر بفرستید")
                    return

                await message.edit("📤 در حال ارسال به تلگرامتون...")

                for f in files:
                    file_extension = os.path.splitext(f)[1].lower()
                    file_name = os.path.basename(f)
                    if file_extension in ['.mp4', '.mov', '.avi', '.mkv']:
                        await bot.send_file(
                            event.chat_id, f,
                            caption="From 💙 @ShahDLbot\n\n`Developed by` @idleer",
                            supports_streaming=True,
                            thumb=thumb_path if thumb_path else None,
                            progress_callback=lambda current, total: asyncio.create_task(
                        upload_progress_callback(current, total, message)
                    ),
                        )
                        DOWNLOADED = True
                        print(f"[✅] New File Uploaded by {event.sender.first_name}, file: {file_name}")
                    else:
                        await bot.send_file(
                            event.chat_id, f,
                            caption="📸 عکس دریافت شد.\n\n`Developed by` @idleer",
                            thumb=thumb_path if thumb_path else None,
                            progress_callback=lambda current, total: asyncio.create_task(
                        upload_progress_callback(current, total, message)
                    ),
                        )
                        DOWNLOADED = True
                        print(f"[✅] New File Uploaded by {event.sender.first_name}, file: {file_name}")

                    if os.path.exists(f):
                        os.remove(f)
                if thumb_path and os.path.exists(thumb_path):
                    os.remove(thumb_path)

            elif (
    "youtube.com/" in link
    or "youtu.be/" in link
    or "soundcloud.com/" in link
):
                progress = DownloadProgress(message, bot.loop)
                files, thumb_path, duration, artist, title = await asyncio.get_event_loop().run_in_executor(
                    None, lambda: YT_DOWNLOADER(link, progress.progress_hook)
                )
                
                if not files:
                    print(f"[❌ Failed, None File] Link sent by {event.sender.first_name}")
                    await message.edit("❌ هیچ فایلی پیدا نشد، لطفا یک لینک معتبر رو امتحان کنید.")
                    return
                
                file_path = files[0]
                temp_dir = os.path.dirname(file_path)
                file_extension = os.path.splitext(file_path)[1].lower()
                file_size = os.path.getsize(file_path)
                file_name = os.path.basename(file_path)
                final_duration = format_duration(int(duration)) if duration > 0 else "Unknown"
                
                await message.edit("🎵 در حال ارسال فایل صوتی به شما...")
                
                await bot.send_file(
                    event.chat_id,
                    file_path,
                   caption=(
                        f"🎵 {title}\n"
                        f"🎤 {artist}\n"
                        f"⏱ Duration: {final_duration}\n"
                        f"📦 Size: {format_size(file_size)}\n\n"
                        f"`Developed by` @idleer"
                    ),
                    thumb=thumb_path if thumb_path and os.path.exists(thumb_path) else None,
                    supports_streaming=True,
                    progress_callback=lambda current, total: asyncio.create_task(
                        upload_progress_callback(current, total, message)
                    ),
                    attributes=[types.DocumentAttributeAudio(
                        voice=False,
                        duration=int(duration),
                        title=title,
                        performer=artist
                    )]
                )
                DOWNLOADED = True
                print(f"[✅] New Audio Uploaded by {event.sender.first_name}, Artist: {artist}, Title: {title}")

                if os.path.exists(file_path):
                    os.remove(file_path)
                if thumb_path and os.path.exists(thumb_path):
                    os.remove(thumb_path)
            
            if DOWNLOADED:
                await message.edit("✅👇🏻 دانلود تکمیل و برای شما ارسال شد.")
            else:
                await message.edit("❌ لینکی که فرستادید پشتیبانی نشد یا فایلی پیدا نشد.")

                
        except Exception as e:
            if "LIVE_STREAM" in str(e):
                print(f"[❌ Failed, LIVE] Live Stream Detected! Link Sent By {event.sender.first_name}")
                await message.edit("❌ این لینک در حال حاضر در پخش زنده است! بعد از اتمام لایو دوباره لینک رو ارسال کنید.")
            else:
                await message.edit("⚠️ خطا در پردازش لینک! لطفا یک لینک معتبر ارسال کنید.")
                print(f"Error: {e}")
        finally:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
            active_downloads.pop(event.chat_id, None)