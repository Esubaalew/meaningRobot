import logging
import os

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ChatMember, ForceReply
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from telegram.error import BadRequest
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
    except BadRequest as e:
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
    user_id = user.id

    if user_id == 1742717838:
        Name = "Azeb M"
        await update.message.reply_text(f"Hey, {Name}! I admire you very much!")
        await update.message.reply_text("Send any word, you want meaning for. I will define it.")
    elif user_id == 1648265210:
        Name = "Esubalew Chekol"
        await update.message.reply_text(f"Hey, {Name}!")
        await update.message.reply_text("Send any word, you want meaning for. I will define it.")
    elif user_id == 209435890:
        Name = "Amarson"
        await update.message.reply_text(f"Hey, {Name}!")
        await update.message.reply_text("Send any word, you want meaning for. I will define it.")
    elif user_id == 202048953:
        Name = "Dan"
        await update.message.reply_text(f"Hey, {Name}!")
        await update.message.reply_text("Send any word, you want meaning for. I will define it.")
    elif user_id == 50479002:
        Name = "Sime"
        await update.message.reply_text(f"Hey, {Name}!")
        await update.message.reply_text("Send any word, you want meaning for. I will define it.")
    elif user_id == 1517746484:
        Name = "Biniam"
        await update.message.reply_text(f"Hey, {Name}!")
        await update.message.reply_text("Send any word, you want meaning for. I will define it.")
    elif user_id == 964042292:
        Name = "Samson"
        await update.message.reply_text(f"Hey, {Name}!")
        await update.message.reply_text("Send any word, you want meaning for. I will define it.")
    else:
        await update.message.reply_text(f"Hey, {userName}!")
        await update.message.reply_text("Send any word, you want meaning for. I will define it.")

async def list_bots(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("TheBELAHbot", url="https://t.me/TheBELAHbot")],
        [InlineKeyboardButton("AAU_Robot", url="https://t.me/AAU_Robot")],
        [InlineKeyboardButton("AllFunctionsbot", url="https://t.me/AllFunctionsbot")],
        [InlineKeyboardButton("ResultsRobot", url="https://t.me/ResultsRobot")],
        [InlineKeyboardButton("Join @esubalewbots for more", url="https://t.me/esubalewbots")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Other bots:", reply_markup=reply_markup)

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
            "Sorry! I can't find meanings for words having letters greater than 27\nThe longest word I can define is electroencephalographically[27 letters]"
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

async def filter_photos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user.first_name
    await update.message.reply_text(f"Dear {user}, Currently, I don't search for Photos/Images!", quote=True)

async def filter_files(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user.first_name
    await update.message.reply_text(f"Dear {user}, Currently, I don't search for Files!", quote=True)

async def filter_videos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user.first_name
    await update.message.reply_text(f"Dear {user}, Currently, I don't search for Videos!", quote=True)

async def filter_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user.first_name
    await update.message.reply_text(f"Dear {user}, Currently, I don't search for Voice messages!", quote=True)

async def filter_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user.first_name
    await update.message.reply_text(f"Dear {user}, Currently, I don't search for Audio!", quote=True)

async def filter_stickers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user.first_name
    await update.message.reply_text(f"Dear {user}, Currently, I don't search for Stickers!", quote=True)

async def filter_documents(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user.first_name
    await update.message.reply_text(f"Dear {user}, Currently, I don't search for Documents!", quote=True)

async def filter_gifs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user.first_name
    await update.message.reply_text(f"Dear {user}, Currently, I don't search for GIFs!", quote=True)

def main() -> None:
    """Start the bot."""
    load_dotenv()

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.environ["TOKEN"]).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("list", list_bots))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))
    application.add_handler(MessageHandler(filters.PHOTO, filter_photos))
    application.add_handler(MessageHandler(filters.DOCUMENT, filter_documents))
    application.add_handler(MessageHandler(filters.VIDEO, filter_videos))
    application.add_handler(MessageHandler(filters.VOICE, filter_voice))
    application.add_handler(MessageHandler(filters.AUDIO, filter_audio))
    application.add_handler(MessageHandler(filters.STICKER, filter_stickers))
    application.add_handler(MessageHandler(filters.GIF, filter_gifs))

    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
