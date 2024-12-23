import logging
import random
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Set up logging to help with debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to load random messages from words.txt file
def load_random_messages():
    try:
        with open('words.txt', 'r', encoding='utf-8') as file:
            random_messages = [line.strip() for line in file.readlines() if line.strip()]
        return random_messages
    except Exception as e:
        logger.error(f"Error loading words from file: {e}")
        return []

# Load random messages from file
random_messages = load_random_messages()

# List of allowed user IDs (Replace with actual Telegram user IDs of people who are allowed to use the bot)
allowed_user_ids = [7238962247,7719248716,7137463942,6974330343]  # Replace with actual user IDs

# Function to send spam to a specific user in the group
async def send_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # Check if the user is allowed to use the bot
    if user_id not in allowed_user_ids:
        await update.message.reply_text("You are not authorized to use this bot.")
        return

    try:
        # Extract the number of spams and target username from the user's message (e.g., "/spam 5 @targetusername")
        num_spams = int(context.args[0]) if context.args else 1
        target_username = context.args[1] if len(context.args) > 1 else None

        # Ensure the number of spams is positive
        if num_spams <= 0:
            await update.message.reply_text("Please enter a positive number for spam.")
            return

        # Ensure the target username is provided
        if not target_username:
            await update.message.reply_text("Please provide a valid username to spam.")
            return

        # Remove '@' from the username (if provided)
        target_username = target_username.lstrip('@')

        # Get the chat ID where the command was issued (This is important to send the message to the group)
        chat_id = update.message.chat_id

        # Send spam message targeting the username (for group context)
        for _ in range(num_spams):
            random_message = random.choice(random_messages)
            spam_message = f"@{target_username} {random_message}"
            await context.bot.send_message(chat_id, spam_message)  # Send to the group chat
            time.sleep(1)  # Delay between spam messages (1 second)
    
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /spam <number_of_spams> <@username>")

# Command to start the bot and display a welcome message
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logger.info(f"User {user.id} started the conversation.")
    await update.message.reply_text(
        "Hello! I can spam messages to a specific user in the group.\n"
        "Use the command /raid <number_of_spams> <@username> to get spammed!\n"
        "Example: /raid 5 @targetusername"
    )

# Main function to run the bot
def main():
    # Your Telegram Bot Token
    bot_token = '7892011069:AAEnIuxHBcV2ty-p7yDwm6k7MkDpjUQSjl8'  # Replace with your bot's token

    # Create the application
    application = Application.builder().token('7892011069:AAEnIuxHBcV2ty-p7yDwm6k7MkDpjUQSjl8').build()

    # Command handler for /start command
    application.add_handler(CommandHandler("start", start))

    # Command handler for /spam command
    application.add_handler(CommandHandler("raid", send_spam))

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()
