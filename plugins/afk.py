import time
from pyrogram import Client, filters
from pyrogram.types import Message
import config

# Global state tracking
IS_AFK = False
AFK_REASON = ""
AFK_TIME = 0

# Owner Profile Context
HANDLE = "MrBoss002"

# Command: Go AFK (.afk or .afk <reason>)
@Client.on_message(filters.me & filters.command("afk", prefixes=config.CMD_HANDLER))
async def set_afk(client: Client, message: Message):
    global IS_AFK, AFK_REASON, AFK_TIME
    
    IS_AFK = True
    AFK_TIME = time.time()
    
    # Extract reason if provided
    if len(message.command) > 1:
        AFK_REASON = message.text.split(maxsplit=1)[1]
        await message.edit_text(f"🔋 **Stepping away fr fr.**\n**Why:** `{AFK_REASON}`")
    else:
        AFK_REASON = ""
        await message.edit_text("🔋 **Stepping away fr fr. Catch ya later.**")

# Auto-Reply: Triggers when someone mentions you or sends a PM while AFK
@Client.on_message((filters.mentioned | filters.private) & ~filters.me & ~filters.bot, group=1)
async def afk_reply(client: Client, message: Message):
    global IS_AFK, AFK_REASON, AFK_TIME
    
    if not IS_AFK:
        return

    # Calculate duration
    afk_duration = round(time.time() - AFK_TIME)
    mins, secs = divmod(afk_duration, 60)
    hours, mins = divmod(mins, 60)
    
    time_str = ""
    if hours > 0:
        time_str += f"{hours}h "
    if mins > 0:
        time_str += f"{mins}m "
    time_str += f"{secs}s"

    # Gen-Z style response format
    msg_text = (
        f"🎧 **@{HANDLE} is ghosting for a bit.**\n\n"
        f"⏳ **Ghosting for:** `{time_str}`\n"
    )

    if AFK_REASON:
        msg_text += f"💭 **Current status:** `{AFK_REASON}`\n"

    msg_text += "\nDrop your msg, they'll reply whenever they feel like it 💀"

    await message.reply_text(msg_text)

# Auto-UnAFK: Disables AFK status when you post any message
@Client.on_message(filters.me & ~filters.command("afk", prefixes=config.CMD_HANDLER), group=2)
async def unset_afk(client: Client, message: Message):
    global IS_AFK, AFK_REASON, AFK_TIME
    
    if IS_AFK:
        afk_duration = round(time.time() - AFK_TIME)
        mins, secs = divmod(afk_duration, 60)
        hours, mins = divmod(mins, 60)
        
        time_str = ""
        if hours > 0:
            time_str += f"{hours}h "
        if mins > 0:
            time_str += f"{mins}m "
        time_str += f"{secs}s"

        IS_AFK = False
        AFK_REASON = ""
        
        info_msg = await message.reply_text(f"🔥 **Back in the game!** Was gone for `{time_str}`.")
        time.sleep(5)
        await info_msg.delete()
