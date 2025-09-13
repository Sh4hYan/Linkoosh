from telethon import TelegramClient
from config import API_ID, API_HASH, BOT_TOKEN
from handlers import start_handlers

bot = TelegramClient('YOUR_SESSION', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
start_handlers(bot)

print("The Bot is Running...")
bot.run_until_disconnected()