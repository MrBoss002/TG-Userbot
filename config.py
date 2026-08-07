import os

API_ID = int(os.getenv("API_ID", 1234567))  # Replace with your API ID
API_HASH = os.getenv("API_HASH", "your_api_hash")
SESSION_STRING = os.getenv("SESSION_STRING", "your_pyrogram_session_string")
CMD_HANDLER = "."  # Command prefix, e.g., .ping
