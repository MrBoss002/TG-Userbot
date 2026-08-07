import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import Message
import config

# Active Tic-Tac-Toe games tracker: {chat_id: game_state}
TTT_GAMES = {}

# Active Word Games tracker: {chat_id: word_state}
WORD_GAMES = {}

# Word bank for WCG / Word Scramble
WORD_LIST = [
    "PYTHON", "TELEGRAM", "USERBOT", "GITHUB", "SERVER",
    "CODING", "DATABASE", "PLUGIN", "NETWORK", "CYBER"
]

# ---------------------------------------------------------
# 1. TELEGRAM EMOJI DICE & SPORTS GAMES
# ---------------------------------------------------------

@Client.on_message(filters.me & filters.command(["dice", "roll"], prefixes=config.CMD_HANDLER))
async def roll_dice(client: Client, message: Message):
    await message.delete()
    await client.send_dice(message.chat.id, emoji="🎲")

@Client.on_message(filters.me & filters.command(["basket", "basketball"], prefixes=config.CMD_HANDLER))
async def play_basket(client: Client, message: Message):
    await message.delete()
    await client.send_dice(message.chat.id, emoji="🏀")

@Client.on_message(filters.me & filters.command(["football", "goal"], prefixes=config.CMD_HANDLER))
async def play_football(client: Client, message: Message):
    await message.delete()
    await client.send_dice(message.chat.id, emoji="⚽")

@Client.on_message(filters.me & filters.command(["bowling"], prefixes=config.CMD_HANDLER))
async def play_bowling(client: Client, message: Message):
    await message.delete()
    await client.send_dice(message.chat.id, emoji="🎳")

@Client.on_message(filters.me & filters.command(["dart"], prefixes=config.CMD_HANDLER))
async def play_dart(client: Client, message: Message):
    await message.delete()
    await client.send_dice(message.chat.id, emoji="🎯")

@Client.on_message(filters.me & filters.command(["slots", "spin"], prefixes=config.CMD_HANDLER))
async def spin_slots(client: Client, message: Message):
    await message.delete()
    await client.send_dice(message.chat.id, emoji="🎰")


# ---------------------------------------------------------
# 2. TIC-TAC-TOE (.ttt)
# ---------------------------------------------------------

def render_board(board):
    return (
        f"🎮 **Tic-Tac-Toe**\n\n"
        f" {board[0]} | {board[1]} | {board[2]} \n"
        f"---+---+---\n"
        f" {board[3]} | {board[4]} | {board[5]} \n"
        f"---+---+---\n"
        f" {board[6]} | {board[7]} | {board[8]} \n\n"
        f"💡 **Play move:** `.ttt <1-9>`\n"
        f"❌ **Cancel game:** `.ttt end`"
    )

def check_winner(board):
    wins = [
        (0,1,2), (3,4,5), (6,7,8), # rows
        (0,3,6), (1,4,7), (2,5,8), # cols
        (0,4,8), (2,4,6)           # diagonals
    ]
    for a, b, c in wins:
        if board[a] == board[b] == board[c] and board[a] not in ["1","2","3","4","5","6","7","8","9"]:
            return board[a]
    if all(cell in ["❌", "⭕"] for cell in board):
        return "DRAW"
    return None

@Client.on_message(filters.me & filters.command("ttt", prefixes=config.CMD_HANDLER))
async def tictactoe_handler(client: Client, message: Message):
    chat_id = message.chat.id
    args = message.command[1:] if len(message.command) > 1 else []

    # Start new game
    if not args or args[0].lower() == "start":
        TTT_GAMES[chat_id] = {
            "board": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
            "turn": "❌"
        }
        await message.edit_text(render_board(TTT_GAMES[chat_id]["board"]))
        return

    # Cancel game
    if args[0].lower() == "end":
        if chat_id in TTT_GAMES:
            del TTT_GAMES[chat_id]
            await message.edit_text("🛑 **Tic-Tac-Toe game ended.**")
        else:
            await message.edit_text("⚠️ No active game in this chat. Start with `.ttt`")
        return

    # Process move
    if chat_id not in TTT_GAMES:
        await message.edit_text("⚠️ No active game! Start one with `.ttt`")
        return

    move_str = args[0]
    if not move_str.isdigit() or int(move_str) not in range(1, 10):
        await message.edit_text("⚠️ Pick a spot from 1 to 9 (e.g. `.ttt 5`)")
        return

    idx = int(move_str) - 1
    game = TTT_GAMES[chat_id]

    if game["board"][idx] in ["❌", "⭕"]:
        await message.edit_text("⚠️ That spot is already taken! Pick another.")
        return

    # Execute player move
    game["board"][idx] = game["turn"]
    winner = check_winner(game["board"])

    if winner:
        if winner == "DRAW":
            final_txt = render_board(game["board"]) + "\n\n🤝 **It's a draw! Well played.**"
        else:
            final_txt = render_board(game["board"]) + f"\n\n🏆 **Winner:** {winner}! GG WP."
        await message.edit_text(final_txt)
        del TTT_GAMES[chat_id]
        return

    # Switch turn (or bot auto-move if single player)
    game["turn"] = "⭕" if game["turn"] == "❌" else "❌"
    await message.edit_text(render_board(game["board"]))


# ---------------------------------------------------------
# 3. WORD SCRAMBLE / GUESSING GAME (.wcg)
# ---------------------------------------------------------

@Client.on_message(filters.me & filters.command(["wcg", "wordgame"], prefixes=config.CMD_HANDLER))
async def start_word_game(client: Client, message: Message):
    chat_id = message.chat.id
    target_word = random.choice(WORD_LIST)
    
    # Scramble the word
    scrambled = "".join(random.sample(target_word, len(target_word)))
    while scrambled == target_word:
        scrambled = "".join(random.sample(target_word, len(target_word)))

    WORD_GAMES[chat_id] = target_word

    text = (
        "🔤 **Word Scramble Challenge!**\n\n"
        f"🧩 **Unscramble this:** `{scrambled}`\n\n"
        "💡 **Guess using:** `.guess <word>`"
    )
    await message.edit_text(text)

@Client.on_message(filters.me & filters.command("guess", prefixes=config.CMD_HANDLER))
async def guess_word(client: Client, message: Message):
    chat_id = message.chat.id
    if chat_id not in WORD_GAMES:
        await message.edit_text("⚠️ No active word game! Start one with `.wcg`")
        return

    if len(message.command) < 2:
        await message.edit_text("Usage: `.guess <YOUR_GUESS>`")
        return

    user_guess = message.command[1].upper()
    correct_word = WORD_GAMES[chat_id]

    if user_guess == correct_word:
        await message.edit_text(f"🎉 **BINGO!** The word was indeed `{correct_word}`. Brain power 100! 🧠🔥")
        del WORD_GAMES[chat_id]
    else:
        await message.edit_text(f"❌ `{user_guess}` is wrong! Keep trying with `.guess <word>`")
