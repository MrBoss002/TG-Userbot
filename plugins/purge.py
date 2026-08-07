import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
import config

# Delete a single replied-to message
@Client.on_message(filters.me & filters.command("del", prefixes=config.CMD_HANDLER))
async def del_message(client: Client, message: Message):
    if not message.reply_to_message:
        await message.edit_text("⚠️ Reply to a msg you wanna nuke.")
        await asyncio.sleep(3)
        await message.delete()
        return

    await message.reply_to_message.delete()
    await message.delete()

# Delete all messages from the replied message up to the current one
@Client.on_message(filters.me & filters.command("purge", prefixes=config.CMD_HANDLER))
async def purge_messages(client: Client, message: Message):
    if not message.reply_to_message:
        await message.edit_text("⚠️ Reply to where you wanna start purging from.")
        await asyncio.sleep(3)
        await message.delete()
        return

    start_msg_id = message.reply_to_message.id
    end_msg_id = message.id
    chat_id = message.chat.id

    msg_ids = list(range(start_msg_id, end_msg_id + 1))
    
    await message.edit_text("🧹 **Nuking messages...**")

    # Pyrogram can delete up to 100 messages at a time
    chunk_size = 100
    for i in range(0, len(msg_ids), chunk_size):
        chunk = msg_ids[i:i + chunk_size]
        await client.delete_messages(chat_id=chat_id, message_ids=chunk)

    done_msg = await client.send_message(chat_id, f"🗑️ **Purged {len(msg_ids)} messages cleanly!**")
    await asyncio.sleep(3)
    await done_msg.delete()
