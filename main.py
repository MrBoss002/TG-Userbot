import os
import sys
import importlib
import requests
from pyrogram import Client, filters
import config

app = Client(
    "my_userbot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=config.SESSION_STRING,
)

# Function to dynamically load a plugin file
def load_plugin(plugin_name):
    try:
        importlib.import_module(f"plugins.{plugin_name}")
        print(f"Successfully loaded plugin: {plugin_name}")
    except Exception as e:
        print(f"Failed to load plugin {plugin_name}: {e}")

# Load all existing plugins on startup
def load_all_plugins():
    if not os.path.exists("plugins"):
        os.makedirs("plugins")
    for file in os.listdir("plugins"):
        if file.endswith(".py") and not file.startswith("__"):
            plugin_name = file[:-3]
            load_plugin(plugin_name)

# Built-in command: Install plugin directly from a raw Gist link
@app.on_message(filters.me & filters.command("install", prefixes=config.CMD_HANDLER))
async def install_gist_plugin(client, message):
    if len(message.command) < 2:
        await message.edit_text("Usage: `.install <raw_gist_url>`")
        return

    url = message.command[1]
    await message.edit_text("📥 Downloading plugin...")

    try:
        response = requests.get(url)
        if response.status_code != 200:
            await message.edit_text("❌ Failed to fetch Gist. Make sure it's a raw URL.")
            return

        # Extract filename from URL or assign a default
        plugin_name = url.split("/")[-1].replace(".py", "")
        file_path = os.path.join("plugins", f"{plugin_name}.py")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(response.text)

        # Load the newly saved plugin
        load_plugin(plugin_name)
        await message.edit_text(f"✅ Plugin `{plugin_name}` installed and loaded successfully!")

    except Exception as e:
        await message.edit_text(f"❌ Error installing plugin: {e}")

if __name__ == "__main__":
    print("Starting Userbot...")
    load_all_plugins()
    app.run()
