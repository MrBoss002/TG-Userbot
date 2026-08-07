import os
import io
import asyncio
from PIL import Image
from pyrogram import Client, filters
from pyrogram.types import Message
import config

# Helper: Resize image to fit Telegram sticker dimensions (512x512 max)
def resize_image(image_path: str) -> str:
    im = Image.open(image_path)
    maxsize = (512, 512)
    im.thumbnail(maxsize, Image.Resampling.LANCZOS)
    
    output_path = "sticker.png"
    im.save(output_path, "PNG")
    return output_path

# Command: .kang / .sticker - Steal or convert image/sticker to sticker format
@Client.on_message(filters.me & filters.command(["kang", "sticker"], prefixes=config.CMD_HANDLER))
async def kang_sticker(client: Client, message: Message):
    reply = message.reply_to_message
    if not reply or not (reply.photo or reply.sticker or reply.document):
        await message.edit_text("⚠️ Reply to an image, sticker, or image document to kang it.")
        await asyncio.sleep(3)
        await message.delete()
        return

    await message.edit_text("🔄 **Kanging sticker...**")

    try:
        # Download media
        downloaded_file = await client.download_media(reply)
        
        # Process image
        sticker_file = resize_image(downloaded_file)
        
        # Send back as a custom Telegram sticker
        await client.send_sticker(
            chat_id=message.chat.id,
            sticker=sticker_file,
            reply_to_message_id=reply.id
        )
        
        await message.delete()

        # Clean up local temporary files
        if os.path.exists(downloaded_file):
            os.remove(downloaded_file)
        if os.path.exists(sticker_file):
            os.remove(sticker_file)

    except Exception as e:
        await message.edit_text(f"❌ **Failed to kang sticker:** `{e}`")

# Command: .toimage / .toimg - Convert a sticker back into a normal photo
@Client.on_message(filters.me & filters.command(["toimage", "toimg"], prefixes=config.CMD_HANDLER))
async def sticker_to_image(client: Client, message: Message):
    reply = message.reply_to_message
    if not reply or not reply.sticker:
        await message.edit_text("⚠️ Reply to a sticker to convert it to an image.")
        await asyncio.sleep(3)
        await message.delete()
        return

    if reply.sticker.is_animated or reply.sticker.is_video:
        await message.edit_text("⚠️ Animated and video stickers aren't supported yet.")
        await asyncio.sleep(3)
        await message.delete()
        return

    await message.edit_text("🖼️ **Converting sticker to image...**")

    try:
        # Download sticker file
        downloaded_file = await client.download_media(reply)
        
        # Convert to PNG using PIL
        im = Image.open(downloaded_file)
        png_path = "converted_image.png"
        im.save(png_path, "PNG")

        # Reply with photo
        await client.send_photo(
            chat_id=message.chat.id,
            photo=png_path,
            caption="✨ **Converted cleanly.**",
            reply_to_message_id=reply.id
        )

        await message.delete()

        # Cleanup files
        if os.path.exists(downloaded_file):
            os.remove(downloaded_file)
        if os.path.exists(png_path):
            os.remove(png_path)

    except Exception as e:
        await message.edit_text(f"❌ **Failed to convert sticker:** `{e}`")
