from email.contentmanager import ContentManager
from turtle import update
import convertapi
import telebot
import tempfile
import requests
from io import BytesIO

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

token = '5423620003:AAFpTH-Ruzs4JTk9sKWHiFwKWhANDYxZWg4'
convertapi.api_secret = 'bELJODOJ9siIZspR'

bot = telebot.TeleBot(token)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_markdown_v2(
        f'Hi {user.mention_markdown_v2()}\! \n\n /convertToPdf \- to convert your files to pdf \n'
     )

async def convert_to_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_markdown_v2(
        f'Please send your file here'
     )

async def converting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    bot.get_file()

    await update.message.reply_markdown_v2(
        f'Wait. The file is being converted!'
     )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

  

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5423620003:AAFpTH-Ruzs4JTk9sKWHiFwKWhANDYxZWg4").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("convertToPdf", convert_to_pdf))
    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.PHOTO, converting))
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()