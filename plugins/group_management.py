import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
import config

SETTINGS = {
    "antilink": {},
    "antiforward": {},
    "welcome": {},
    "goodbye": {},
    "filters": {},
    "pdm": {}
}

# Command: .lock / .unlock - Lock permissions in group chat
@Client.on_message(filters.me & filters.command("lock", prefixes=config.CMD_HANDLER))
async def lock_chat(client: Client, message: Message):
    if message.chat.type.value in ["private"]:
        return
    try:
        await client.set_chat_permissions(message.chat.id, ChatPermissions())
        await message.edit_text("🔒 **Chat locked down. Nobody typing till further notice.**")
    except Exception as e:
        await message.edit_text(f"❌ **Couldn't lock chat:** `{e}`")

@Client.on_message(filters.me & filters.command("unlock", prefixes=config.CMD_HANDLER))
async def unlock_chat(client: Client, message: Message):
    if message.chat.type.value in ["private"]:
        return
    try:
        await client.set_chat_permissions(
            message.chat.id,
            ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        await message.edit_text("🔓 **Chat unlocked. Chat away.**")
    except Exception as e:
        await message.edit_text(f"❌ **Couldn't unlock chat:** `{e}`")

# Command: .antilink - Toggle auto-deleting links
@Client.on_message(filters.me & filters.command("antilink", prefixes=config.CMD_HANDLER))
async def toggle_antilink(client: Client, message: Message):
    chat_id = message.chat.id
    current = SETTINGS["antilink"].get(chat_id, False)
    SETTINGS["antilink"][chat_id] = not current
    status = "ON 🛡️ (No promo links allowed)" if SETTINGS["antilink"][chat_id] else "OFF 🔓"
    await message.edit_text(f"⚡ **Anti-Link is now {status}**")

# Command: .antiforward - Toggle auto-deleting forwarded messages
@Client.on_message(filters.me & filters.command("antiforward", prefixes=config.CMD_HANDLER))
async def toggle_antiforward(client: Client, message: Message):
    chat_id = message.chat.id
    current = SETTINGS["antiforward"].get(chat_id, False)
    SETTINGS["antiforward"][chat_id] = not current
    status = "ON 🛡️ (No forwarded spam)" if SETTINGS["antiforward"][chat_id] else "OFF 🔓"
    await message.edit_text(f"⚡ **Anti-Forward is now {status}**")

# Command: .pdm - Toggle Promote/Demote Monitor alert
@Client.on_message(filters.me & filters.command("pdm", prefixes=config.CMD_HANDLER))
async def toggle_pdm(client: Client, message: Message):
    chat_id = message.chat.id
    current = SETTINGS["pdm"].get(chat_id, False)
    SETTINGS["pdm"][chat_id] = not current
    status = "ON 📢 (Tracking admin changes)" if SETTINGS["pdm"][chat_id] else "OFF 🔕"
    await message.edit_text(f"👑 **PDM Radar is now {status}**")

# Command: .welcome / .goodbye - Set custom welcome/goodbye messages
@Client.on_message(filters.me & filters.command("welcome", prefixes=config.CMD_HANDLER))
async def set_welcome(client: Client, message: Message):
    if len(message.command) < 2:
        await message.edit_text("Usage: `.welcome Welcome to the squad, {user}!`")
        return
    text = message.text.split(maxsplit=1)[1]
    SETTINGS["welcome"][message.chat.id] = text
    await message.edit_text("✅ **Custom welcome message set fr.**")

@Client.on_message(filters.me & filters.command("goodbye", prefixes=config.CMD_HANDLER))
async def set_goodbye(client: Client, message: Message):
    if len(message.command) < 2:
        await message.edit_text("Usage: `.goodbye Later {user}, stay safe 💀`")
        return
    text = message.text.split(maxsplit=1)[1]
    SETTINGS["goodbye"][message.chat.id] = text
    await message.edit_text("✅ **Goodbye message set!**")

# Command: .filter - Custom trigger auto-response
@Client.on_message(filters.me & filters.command("filter", prefixes=config.CMD_HANDLER))
async def add_filter(client: Client, message: Message):
    if "|" not in message.text:
        await message.edit_text("Usage: `.filter trigger | response`")
        return
    content = message.text.split(maxsplit=1)[1]
    trigger, response = [x.strip() for x in content.split("|", 1)]
    chat_id = message.chat.id
    if chat_id not in SETTINGS["filters"]:
        SETTINGS["filters"][chat_id] = {}
    SETTINGS["filters"][chat_id][trigger.lower()] = response
    await message.edit_text(f"🎯 **Auto-reply set for:** `{trigger}`")

# Command: .ginfo - Display full group info
@Client.on_message(filters.me & filters.command("ginfo", prefixes=config.CMD_HANDLER))
async def group_info(client: Client, message: Message):
    if message.chat.type.value in ["private"]:
        return
    chat = await client.get_chat(message.chat.id)
    info = (
        f"📊 **Group Breakdown:**\n\n"
        f"📛 **Name:** `{chat.title}`\n"
        f"🆔 **ID:** `{chat.id}`\n"
        f"👥 **Squad Size:** `{chat.members_count} members`\n"
        f"💬 **Type:** `{chat.type.value}`\n"
    )
    if chat.username:
        info += f"🔗 **Handle:** @{chat.username}\n"
    await message.edit_text(info)

# Command: .tag - Tag group members cleanly
@Client.on_message(filters.me & filters.command("tag", prefixes=config.CMD_HANDLER))
async def tag_members(client: Client, message: Message):
    if message.chat.type.value in ["private"]:
        return
    text = message.text.split(maxsplit=1)[1] if len(message.command) > 1 else "Wake up team! 👋"
    mentions = ""
    count = 0
    await message.delete()
    async for member in client.get_chat_members(message.chat.id, limit=50):
        if not member.user.is_bot:
            mentions += f"[{member.user.first_name}](tg://user?id={member.user.id}) "
            count += 1
            if count % 5 == 0:
                await client.send_message(message.chat.id, f"{text}\n\n{mentions}")
                mentions = ""
                await asyncio.sleep(1)
    if mentions:
        await client.send_message(message.chat.id, f"{text}\n\n{mentions}")

# Command: .vote - Quick poll generator
@Client.on_message(filters.me & filters.command("vote", prefixes=config.CMD_HANDLER))
async def create_vote(client: Client, message: Message):
    if "|" not in message.text:
        await message.edit_text("Usage: `.vote Question | Option 1 | Option 2`")
        return
    parts = [x.strip() for x in message.text.split(maxsplit=1)[1].split("|")]
    question = parts[0]
    options = parts[1:]
    if len(options) < 2:
        await message.edit_text("⚠️ Need at least 2 options for a poll.")
        return
    await message.delete()
    await client.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=options,
        is_anonymous=False
    )

# Automated Listeners
@Client.on_message(~filters.me & ~filters.service, group=3)
async def automated_moderator(client: Client, message: Message):
    chat_id = message.chat.id

    if SETTINGS["antilink"].get(chat_id) and message.text:
        if "http://" in message.text or "https://" in message.text or "t.me/" in message.text:
            try:
                await message.delete()
                return
            except Exception:
                pass

    if SETTINGS["antiforward"].get(chat_id) and message.forward_date:
        try:
            await message.delete()
            return
        except Exception:
            pass

    if chat_id in SETTINGS["filters"] and message.text:
        msg_text = message.text.lower()
        for trigger, response in SETTINGS["filters"][chat_id].items():
            if trigger in msg_text:
                await message.reply_text(response)
                break

@Client.on_message(filters.new_chat_members, group=4)
async def welcome_listener(client: Client, message: Message):
    chat_id = message.chat.id
    if chat_id in SETTINGS["welcome"]:
        for user in message.new_chat_members:
            text = SETTINGS["welcome"][chat_id].replace("{user}", user.first_name)
            await message.reply_text(text)

@Client.on_message(filters.left_chat_member, group=5)
async def goodbye_listener(client: Client, message: Message):
    chat_id = message.chat.id
    if chat_id in SETTINGS["goodbye"]:
        user = message.left_chat_member
        text = SETTINGS["goodbye"][chat_id].replace("{user}", user.first_name)
        await message.reply_text(text)
