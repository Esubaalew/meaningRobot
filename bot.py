import logging
import os
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ChatMember
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
import requests
from bs4 import BeautifulSoup

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

CHANNEL_USERNAME = "@esubalewbots"

async def check_user_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_id = update.effective_user.id
    try:
        chat_member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        user_status = chat_member.status
        return user_status
    except Exception as e:
        logger.error(f"Error: {e}")
        return "error"

async def send_join_channel_button(chat_id, context: ContextTypes.DEFAULT_TYPE):
    button = InlineKeyboardButton("Join Channel", url="https://t.me/esubalewbots")
    keyboard = [[button]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=chat_id, text="To use this bot, please join our channel:", reply_markup=reply_markup)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    userName = user.first_name
    await update.message.reply_text(f"Hey, {userName}! Send any word, and I will define it.")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_status = await check_user_status(update, context)

    if user_status == "error":
        await update.message.reply_text("An error occurred. Please try again later.")
        return

    if user_status not in [ChatMember.MEMBER, ChatMember.ADMINISTRATOR, ChatMember.CREATOR]:
        await update.message.reply_text(f"Please join {CHANNEL_USERNAME} before using the bot.\nYour current status: {user_status}")
        await send_join_channel_button(update.message.chat_id, context)
        return

    text = update.message.text.strip()

    if len(text) > 27:
        await update.message.reply_text(
            "Sorry! I can't find meanings for words having more than 27 letters."
        )
        return

    try:
        message = await update.message.reply_text(
            f'I am searching for {text}, Please wait....', quote=True)

        url = f'https://www.merriam-webster.com/dictionary/{text}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')

        meaning = soup.find('div', {'class': 'vg'})
        if meaning:
            await context.bot.edit_message_text(
                chat_id=update.message.chat_id,
                message_id=message.message_id,
                text=f'Meaning for {text}\n{meaning.text}')
        else:
            await context.bot.edit_message_text(
                chat_id=update.message.chat_id,
                message_id=message.message_id,
                text=f'Meaning not found for {text}!')
            return

        etymology = soup.find('p', {'class': 'et'})
        if etymology:
            await context.bot.send_message(chat_id=update.message.chat_id, text=f'Etymology\n{etymology.text}')
        
        examples = soup.find('div', {'class': 'in-sentences'})
        if examples:
            examples_text = examples.text.strip()
            await context.bot.send_message(chat_id=update.message.chat_id, text=f'Examples for {text}\n{examples_text}')

    except Exception as e:
        logger.error(f"Error: {e}")
        await context.bot.edit_message_text(chat_id=update.message.chat_id, message_id=message.message_id, text='Something went wrong...')

# Filter Handlers for Various Content Types

async def filter_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await search(update, context)

async def filter_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("You sent a URL! Here's what I can do with it later.")

async def filter_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("You sent a photo!")

async def filter_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("You sent a document!")

async def filter_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("You sent an audio file!")

async def filter_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("You sent a video!")

async def filter_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("You sent a sticker!")

async def filter_animation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("You sent an animation!")

def main() -> None:
    """Start the bot."""
    load_dotenv()

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.environ["TOKEN"]).build()

    application.add_handler(CommandHandler("start", start))

    # Detecting Text (non-command) and URLs
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_text))
    application.add_handler(MessageHandler(filters.Entity.URL, filter_url))

    # Detecting Media
    application.add_handler(MessageHandler(filters.PHOTO, filter_photo))
    application.add_handler(MessageHandler(filters.Document.All, filter_document))
    application.add_handler(MessageHandler(filters.AUDIO, filter_audio))
    application.add_handler(MessageHandler(filters.VIDEO, filter_video))
    application.add_handler(MessageHandler(filters.STICKER, filter_sticker))
    application.add_handler(MessageHandler(filters.ANIMATION, filter_animation))

    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
