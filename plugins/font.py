import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
import config

# Unicode font mappings
FONT_MAPS = {
    "mono": lambda text: "".join(f"`{text}`"),
    "bold": lambda text: "".join(f"**{text}**"),
    "italic": lambda text: "".join(f"__{text}__"),
    "strike": lambda text: "".join(f"~~{text}~~"),
    "sans": lambda text: text.translate(str.maketrans(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        "𝖺𝖻𝖼𝖽𝖾𝖿𝗀𝗁𝗂爆𝗄𝗅𝗆𝗇𝗈𝗉𝗊𝗋𝗌𝗍𝗎𝗏𝗐𝗑𝗒𝗓𝖠𝖡𝖢transactions𝖤𝖥𝖭𝖮𝖯𝖰𝖱𝖲𝖳𝖴𝖵𝖶𝖷𝖸𝖹0123456789"
    )),
    "smallcaps": lambda text: text.translate(str.maketrans(
        "abcdefghijklmnopqrstuvwxyz",
        "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"
    )),
    "double": lambda text: text.translate(str.maketrans(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡"
    )),
    "bubble": lambda text: text.translate(str.maketrans(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ⓪①②③④⑤⑥⑦⑧⑨"
    )),
    "script": lambda text: text.translate(str.maketrans(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "𝒶𝒷𝒸𝒹ℯ𝒻ℊ𝒽𝒾𝒿𝓀𝓁𝓂𝓃ℴ𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵"
    ))
}

@Client.on_message(filters.me & filters.command(["font", "style"], prefixes=config.CMD_HANDLER))
async def style_text(client: Client, message: Message):
    args = message.text.split(maxsplit=2)
    
    # Show available styles if no args given
    if len(args) < 2:
        styles_list = "\n".join([f"• `{style}`" for style in FONT_MAPS.keys()])
        usage = (
            "✨ **Font Styles Available:**\n\n"
            f"{styles_list}\n\n"
            "💡 **Usage:**\n"
            "`.font <style> <text>`\n"
            "or reply to a message: `.font <style>`"
        )
        await message.edit_text(usage)
        return

    style_type = args[1].lower()

    if style_type not in FONT_MAPS:
        await message.edit_text(f"⚠️ Unknown style `{style_type}`. Type `.font` to see available styles.")
        await asyncio.sleep(3)
        await message.delete()
        return

    # Check if target text is from a reply or command args
    target_text = ""
    if len(args) > 2:
        target_text = args[2]
    elif message.reply_to_message and message.reply_to_message.text:
        target_text = message.reply_to_message.text
    else:
        await message.edit_text("⚠️ Provide text or reply to a message to convert.")
        await asyncio.sleep(3)
        await message.delete()
        return

    # Apply font transformer
    transformed_text = FONT_MAPS[style_type](target_text)
    await message.edit_text(transformed_text)
