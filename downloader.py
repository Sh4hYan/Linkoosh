import os
import yt_dlp
import tempfile
import shutil
import subprocess

# YT Audio Downloader
def YT_DOWNLOADER(url, progress_callback=None):
    temp_dir = tempfile.mkdtemp()
    output_template = os.path.join(temp_dir, "%(title)s.%(ext)s")

    ydl_opts = {
        'outtmpl': output_template,
        'noplaylist': True,
        'format': 'bestaudio/best',
        'progress_hooks': [progress_callback] if progress_callback else [],
        'no_warnings': True,
        'cookiefile': 'cookies.txt',
        'extract_flat': False,
        'postprocessors': [],
        'writethumbnail': True,
        'writesubtitles': False,
        'writeautomaticsub': False,
        'extractor_args': {
            'soundcloud': {
                'format': 'http_mp3_128_url/http_mp3_128_url/progressive/http_mp3_256_url'
            }
        },
        'format_sort': ['acodec:mp3'],
        'prefer_free_formats': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            if info_dict.get("is_live"):
                raise Exception("LIVE_STREAM")
            
            info_dict = ydl.extract_info(url, download=True)
            downloaded_files = []
            duration = info_dict.get('duration', 0)
            thumb_path = None
            artist = info_dict.get('artist') or info_dict.get('uploader') or info_dict.get('channel') or "Unknown Artist"
            title = info_dict.get('title', 'Unknown Title')

            for root, _, files in os.walk(temp_dir):
                for f in files:
                    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                        thumb_path = os.path.join(root, f)
                        break

            for root, _, files in os.walk(temp_dir):
                for f in files:
                    if f.lower().endswith(('.mp3', '.m4a', '.ogg', '.opus', '.wav', '.flac', '.aac')):
                        file_path = os.path.join(root, f)
                        downloaded_files.append(file_path)

        return downloaded_files, thumb_path, duration, artist, title

    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise e


# Instagram Video Downloader
def VIDEO_DOWNLOADER(url, progress_callback=None):
    temp_dir = tempfile.mkdtemp()
    output_template = os.path.join(temp_dir, "%(title)s_%(id)s.%(ext)s")

    ydl_opts = {
        'outtmpl': output_template,
        'writethumbnail': False,
        'noplaylist': False,
        'progress_hooks': [progress_callback] if progress_callback else [],
        'no_warnings': True,
        'cookiefile': 'cookies.txt',
        'extract_flat': False,
        'ignore_no_formats_error': True,
        'format': 'best[ext=mp4][vcodec^=avc][acodec^=aac]/best[ext=mp4][vcodec^=avc]/best[ext=mp4]/best',
        'postprocessors': [],
        'merge_output_format': None,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            downloaded_files = []

            entries = info_dict.get("entries", [info_dict])
            for entry in entries:
                if entry.get("ext") in ["jpg", "jpeg", "png", "webp"]:
                    continue

                try:
                    file_path = ydl.prepare_filename(entry)
                    if os.path.exists(file_path):
                        downloaded_files.append(file_path)
                except Exception:
                    continue

        return downloaded_files, None

    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise e


# Instagram Phothos Downloader
def INSTAGRAM_DOWNLOADER(url, progress_callback=None):
    temp_dir = tempfile.mkdtemp()
    downloaded_files = []
    thumb_path = None

    try:
        try:
            videos, _ = VIDEO_DOWNLOADER(url, progress_callback=progress_callback)
            if videos:
                downloaded_files.extend(videos)
                print(f"✅ Successfully downloaded {len(videos)} videos with yt-dlp: {[os.path.basename(f) for f in videos]}")
            else:
                print("⚠️ No videos found with yt-dlp")
        except Exception as e:
            print(f"⚠️ Failed to download videos with yt-dlp")

        if not downloaded_files:
            print("🔄 Trying gallery-dl for photos and videos...")
            subprocess.run(
                ["gallery-dl", "--cookies", "cookies.txt", "--directory", temp_dir, url],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            for root, _, files in os.walk(temp_dir):
                for f in files:
                    file_path = os.path.join(root, f)
                    if file_path.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".mp4", ".webm", ".mkv")):
                        downloaded_files.append(file_path)
                        print(f"📁 Found file: {file_path}")

        return downloaded_files, thumb_path

    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise e