import time
from pyrogram import Client, filters
import config

@Client.on_message(filters.me & filters.command("ping", prefixes=config.CMD_HANDLER))
async def ping_handler(client, message):
    start_time = time.time()
    await message.edit_text("Pinging...")
    end_time = time.time()
    latency = round((end_time - start_time) * 1000, 2)
    await message.edit_text(f"🏓 **Pong!**\nLatency: `{latency}ms`")
