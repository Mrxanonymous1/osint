import logging
import random
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

USERS_FILE = 'users.json'

# Define the owner user ID (Replace with your own Telegram user ID)
OWNER_ID = 7238962247  # Replace with the actual Telegram user ID of the owner

def load_authorized_users():
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Return an empty list if the file does not exist
    except json.JSONDecodeError:
        return []  # Return an empty list if there's an issue with the file format

def save_authorized_users():
    with open(USERS_FILE, 'w', encoding='utf-8') as file:
        json.dump(AUTHORIZED_USERS, file, ensure_ascii=False, indent=4)

AUTHORIZED_USERS = load_authorized_users()  # Load authorized users from file

# Blocked usernames (case-insensitive check)
blocked_usernames = ['mrxanonymous', 'mrxanon', 'mrxanonymous1']
blocked_usernames = [username.lower() for username in blocked_usernames]

def is_authorized(user_id: int) -> bool:
    """Check if a user is authorized or the owner."""
    return user_id == OWNER_ID or user_id in AUTHORIZED_USERS

def add_authorized_user(user_id: int) -> str:
    """Add a new authorized user."""
    if user_id in AUTHORIZED_USERS:
        return f"User {user_id} is already authorized."
    AUTHORIZED_USERS.append(user_id)
    save_authorized_users()  # Save the updated list to the file
    return f"User {user_id} has been successfully added."

def remove_authorized_user(user_id: int) -> str:
    """Remove an authorized user."""
    if user_id not in AUTHORIZED_USERS:
        return f"User {user_id} is not in the authorized list."
    AUTHORIZED_USERS.remove(user_id)
    save_authorized_users()  # Save the updated list to the file
    return f"User {user_id} has been removed from the authorized list."

def load_random_messages():
    try:
        with open('words.txt', 'r', encoding='utf-8') as file:
            random_messages = [line.strip() for line in file.readlines() if line.strip()]
        return random_messages
    except Exception as e:
        logger.error(f"Error loading words from file: {e}")
        return []

random_messages = load_random_messages()

async def send_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if not is_authorized(user_id):
        await update.message.reply_text("You are not authorized to use this bot.")
        return
    try:
        num_spams = int(context.args[0]) if context.args else 1
        target_username = context.args[1] if len(context.args) > 1 else None
        if num_spams <= 0:
            await update.message.reply_text("Please enter a positive number for spam.")
            return
        if not target_username:
            await update.message.reply_text("Please provide a valid username to spam.")
            return

        target_username = target_username.lstrip('@').lower()
        if target_username in blocked_usernames:
            await update.message.reply_text(f"Why I spam my owner? You cannot spam @{target_username}.")
            return

        chat_id = update.message.chat_id
        for _ in range(num_spams):
            random_message = random.choice(random_messages)
            spam_message = f"@{target_username} {random_message}"
            await context.bot.send_message(chat_id, spam_message)
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /raid <number_of_spams> <@username>")

async def add_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if not is_authorized(user_id):
        await update.message.reply_text("You are not authorized to add new users.")
        return
    try:
        new_user_id = int(context.args[0])
        result = add_authorized_user(new_user_id)
        await update.message.reply_text(result)
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /adduser <user_id>")

async def remove_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if not is_authorized(user_id):
        await update.message.reply_text("You are not authorized to remove users.")
        return
    try:
        user_to_remove_id = int(context.args[0])
        result = remove_authorized_user(user_to_remove_id)
        await update.message.reply_text(result)
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /removeuser <user_id>")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logger.info(f"User {user.id} started the conversation.")
    await update.message.reply_text(
        "Hello! I can spam messages to a specific user in the group.\n"
        "Use the command /raid <number_of_spams> <@username> to get spammed!\n"
        "Example: /raid 5 @targetusername\n\n"
        "Authorized users can add or remove users using /adduser and /removeuser commands."
    )

def main():
    bot_token = '7892011069:AAEnIuxHBcV2ty-p7yDwm6k7MkDpjUQSjl8'  # Replace with your bot's token
    application = Application.builder().token("7892011069:AAEnIuxHBcV2ty-p7yDwm6k7MkDpjUQSjl8").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("raid", send_spam))
    application.add_handler(CommandHandler("adduser", add_user))
    application.add_handler(CommandHandler("removeuser", remove_user))
    application.run_polling()

if __name__ == '__main__':
    main()
