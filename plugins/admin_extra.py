import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, ChatPrivileges
import config

# Command: .setpp - Change account profile picture by replying to an image
@Client.on_message(filters.me & filters.command("setpp", prefixes=config.CMD_HANDLER))
async def set_profile_photo(client: Client, message: Message):
    reply = message.reply_to_message
    if not reply or not (reply.photo or reply.document):
        await message.edit_text("⚠️ Reply to a fire pic to set it as your pfp.")
        await asyncio.sleep(3)
        await message.delete()
        return

    await message.edit_text("🖼️ **Updating the pfp...**")
    try:
        photo_path = await client.download_media(reply)
        await client.set_profile_photo(photo=photo_path)
        await message.edit_text("🔥 **New pfp unlocked! Looking clean.**")
        if os.path.exists(photo_path):
            os.remove(photo_path)
    except Exception as e:
        await message.edit_text(f"❌ **Failed to set pfp:** `{e}`")

# Command: .promote - Promote a user to admin
@Client.on_message(filters.me & filters.command("promote", prefixes=config.CMD_HANDLER))
async def promote_user(client: Client, message: Message):
    if message.chat.type.value in ["private"]:
        return

    reply = message.reply_to_message
    target_user = reply.from_user if reply else None

    if not target_user and len(message.command) > 1:
        try:
            target_user = await client.get_users(message.command[1])
        except Exception:
            pass

    if not target_user:
        await message.edit_text("⚠️ Tag someone or reply to their msg: `.promote @username`")
        await asyncio.sleep(3)
        await message.delete()
        return

    try:
        await client.promote_chat_member(
            message.chat.id,
            target_user.id,
            privileges=ChatPrivileges(
                can_manage_chat=True,
                can_delete_messages=True,
                can_restrict_members=True,
                can_invite_users=True,
                can_pin_messages=True
            )
        )
        await message.edit_text(f"👑 **Promoted** [{target_user.first_name}](tg://user?id={target_user.id}) **to Admin. Big moves.**")
    except Exception as e:
        await message.edit_text(f"❌ **Couldn't promote:** `{e}`")

# Command: .demote - Demote an admin back to regular member
@Client.on_message(filters.me & filters.command("demote", prefixes=config.CMD_HANDLER))
async def demote_user(client: Client, message: Message):
    if message.chat.type.value in ["private"]:
        return

    reply = message.reply_to_message
    target_user = reply.from_user if reply else None

    if not target_user and len(message.command) > 1:
        try:
            target_user = await client.get_users(message.command[1])
        except Exception:
            pass

    if not target_user:
        await message.edit_text("⚠️ Tag someone or reply to their msg: `.demote @username`")
        await asyncio.sleep(3)
        await message.delete()
        return

    try:
        await client.promote_chat_member(
            message.chat.id,
            target_user.id,
            privileges=ChatPrivileges(
                can_manage_chat=False,
                can_delete_messages=False,
                can_restrict_members=False,
                can_invite_users=False,
                can_pin_messages=False
            )
        )
        await message.edit_text(f"📉 **Demoted** [{target_user.first_name}](tg://user?id={target_user.id}). **Back to member status.**")
    except Exception as e:
        await message.edit_text(f"❌ **Couldn't demote:** `{e}`")

# Command: .add / .invite - Add a user to current group
@Client.on_message(filters.me & filters.command(["add", "invite"], prefixes=config.CMD_HANDLER))
async def add_user(client: Client, message: Message):
    if len(message.command) < 2:
        await message.edit_text("Usage: `.add @username`")
        await asyncio.sleep(3)
        await message.delete()
        return

    target = message.command[1]
    await message.edit_text(f"➕ **Pulling {target} into the chat...**")
    try:
        await client.add_chat_members(message.chat.id, target)
        await message.edit_text(f"🎉 **Added {target} to the squad!**")
    except Exception as e:
        await message.edit_text(f"❌ **Couldn't add user:** `{e}`")

# Command: .join - Join a group by replying to an invite link or passing it as an argument
@Client.on_message(filters.me & filters.command("join", prefixes=config.CMD_HANDLER))
async def join_chat(client: Client, message: Message):
    link = None
    if message.reply_to_message and message.reply_to_message.text:
        link = message.reply_to_message.text
    elif len(message.command) > 1:
        link = message.command[1]

    if not link:
        await message.edit_text("⚠️ Reply to a link or pass one: `.join <link>`")
        await asyncio.sleep(3)
        await message.delete()
        return

    await message.edit_text("🚀 **Hopping in...**")
    try:
        chat = await client.join_chat(link)
        await message.edit_text(f"⚡ **In! Joined:** `{chat.title}`")
    except Exception as e:
        await message.edit_text(f"❌ **Failed to join:** `{e}`")
