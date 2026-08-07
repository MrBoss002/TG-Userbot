import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
import config

@Client.on_message(filters.me & filters.command("type", prefixes=config.CMD_HANDLER))
async def typewriter(client: Client, message: Message):
    if len(message.command) < 2:
        await message.edit_text("Usage: `.type <text to animate>`")
        return

    text_to_type = message.text.split(maxsplit=1)[1]
    typed_text = ""

    for char in text_to_type:
        typed_text += char
        # Appends a block character while typing for effect
        try:
            await message.edit_text(typed_text + " ▌")
            await asyncio.sleep(0.15)
        except Exception:
            pass  # Avoid edit limits/errors on fast typing

    # Final edit showing full text without cursor
    await message.edit_text(text_to_type)
