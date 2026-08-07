import time
import sys
import pyrogram
from pyrogram import Client, filters
from pyrogram.types import Message
import config

START_TIME = time.time()

def get_readable_time(seconds: int) -> str:
    mins, secs = divmod(seconds, 60)
    hours, mins = divmod(mins, 60)
    days, hours = divmod(hours, 24)
    
    time_str = ""
    if days > 0:
        time_str += f"{days}d "
    if hours > 0:
        time_str += f"{hours}h "
    if mins > 0:
        time_str += f"{mins}m "
    time_str += f"{secs}s"
    return time_str

@Client.on_message(filters.me & filters.command("alive", prefixes=config.CMD_HANDLER))
async def alive_handler(client: Client, message: Message):
    uptime = get_readable_time(int(time.time() - START_TIME))
    pyro_ver = pyrogram.__version__
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    alive_text = (
        "⚡ **TG-Userbot is up & cookin'**\n\n"
        f"👤 **Master:** `@MrBoss002`\n"
        f"⏳ **Uptime:** `{uptime}`\n"
        f"🐍 **Python:** `{py_ver}`\n"
        f"🔥 **Pyrogram:** `{pyro_ver}`\n\n"
        "✨ _Running smooth, no cap._"
    )

    await message.edit_text(alive_text)
