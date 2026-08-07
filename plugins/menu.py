import time
import psutil
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message
import config

START_TIME = time.time()

# Function to calculate uptime
def get_uptime():
    seconds = int(time.time() - START_TIME)
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

# Small utility to convert text to typewriter/monospace font style like your WhatsApp bot
def to_mono(text: str) -> str:
    return f"`{text.upper()}`"

@Client.on_message(filters.me & filters.command(["menu", "help"], prefixes=config.CMD_HANDLER))
async def show_menu(client: Client, message: Message):
    # Fetch live system specs & time info
    now = datetime.now()
    date_str = now.strftime("%-d/%-m/%Y")
    time_str = now.strftime("%I:%M:%S %p")
    day_str = now.strftime("%A")
    
    # Fetch memory usage
    mem = psutil.virtual_memory()
    ram_used = int(mem.used / (1024 * 1024))
    ram_total = int(mem.total / (1024 * 1024))
    uptime_str = get_uptime()

    # Dynamic Menu Header
    menu_text = (
        "┌━━≪≪☆≫≫━━┓\n"
        "  ༺𝑴𝒓𝑩𝒐𝒔𝒔𝟎𝟎𝟐༻\n"
        "└━━≪≪☆≫≫━━┛\n"
        " ┏━━≪≪✟≫≫━━┓\n"
        f" ┃ 📅 **Date:** `{date_str}`\n"
        f" ┃ ⏰ **Time:** `{time_str}`\n"
        f" ┃ 🌀 **Day:** `{day_str}`\n"
        f" ┃ ✨ **Version:** `3.5.4`\n"
        f" ┃ 🪻 **RAM:** `{ram_used}/{ram_total}MB`\n"
        f" ┃ ⏳ **Uptime:** `{uptime_str}`\n"
        " ┗━━≪≪✟≫≫━━┛\n"
    )

    # Categories and commands mapped out in WhatsApp bot style
    categories = {
        "MISC": ["AFK", "ALIVE", "PING", "TYPE", "FONT"],
        "GAMES": ["DICE", "BASKET", "FOOTBALL", "BOWLING", "DART", "SLOTS", "TTT", "WCG", "GUESS"],
        "MEDIA": ["KANG", "STICKER", "TOIMAGE", "SETPP"],
        "ADMIN": ["BAN", "UNBAN", "KICK", "MUTE", "UNMUTE", "PROMOTE", "DEMOTE", "ADD", "INVITE"],
        "GROUPS": ["LOCK", "UNLOCK", "ANTILINK", "ANTIFORWARD", "PDM", "WELCOME", "GOODBYE", "FILTER", "GINFO", "TAG", "VOTE", "JOIN"]
    }

    # Build category blocks
    for cat_name, cmds in categories.items():
        menu_text += f" ┏━⚝ {cat_name} ⚝\n"
        for cmd in cmds:
            menu_text += f" ┃ ⟢ {cmd}\n"
        menu_text += " ┗━━━━━━━━━━━━━━━━━⟢\n"

    menu_text += "\n🤍 **Bot By «MrBoss002»**\n⚔️ Thanks for using «MrBoss002» bot"

    await message.edit_text(menu_text)
