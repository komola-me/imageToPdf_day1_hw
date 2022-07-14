#!/usr/bin/env python
# pylint: disable=C0116,W0613

from email import message
from importlib.resources import path
from inspect import getfile
from io import BytesIO
import logging
from msilib.schema import File
from os import name
import os
from pydoc import Doc, doc
import tempfile
from tkinter import PhotoImage
from urllib import request
from xml.dom.minidom import Document
import requests
from telegram import Update, ForceReply, ReplyKeyboardMarkup, File
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import convertapi

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

token = '5423620003:AAFpTH-Ruzs4JTk9sKWHiFwKWhANDYxZWg4'
convertapi.api_secret = 'bELJODOJ9siIZspR'



def make_keyboard_for_start_command() -> ReplyKeyboardMarkup:
    buttons = [
        ['Rasm to PDF'],
        {'Aloqa', 'Manzil'},
        ['About']
    ]

    return ReplyKeyboardMarkup(buttons)

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_text(
        f'Welcome, {user.first_name} \n', reply_markup=make_keyboard_for_start_command()
    )

def receive_image(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Please send your photo in file form.')

def img_to_pdf(update: Update, context: CallbackContext) -> None:
    file = context.bot.get_file(update.message.document.file_id)
    #print(file)
    file_data = BytesIO(requests.get(f'{file.file_path}').content)
    #print(file_data)
    # file name
    file_name = update.message.document.file_name
    update.message.reply_text('Wait.. Converting..')
    upload = convertapi.UploadIO(file_data, filename=file_name)
    convert = convertapi.convert('pdf', {'File': upload})
    result = convert.save_files(tempfile.gettempdir())

    #update.message.reply_document(document='https://andonovicmilica.files.wordpress.com/2018/07/short-stories-for-children.pdf')

    for f in result:
        context.bot.send_document(update.message.chat.id, open(f, 'rb'))

def aloqa(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Savol va takliflar uchun komolaziya28@gmail.com maniziliga e-mail yuborishingiz mumkin.')

def about(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Bu bot orqali xohlagan rasmingizni pdf formatiga o\'tkazishingiz mumkin')

def manzil(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Bizning manzil: ')
    update.message.reply_location(longitude=49.779298, latitude=42.885564)

def rasm(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('I cannot convert your photo. Please send it as a FILE.')

def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text("Aloqa"), aloqa))
    dispatcher.add_handler(MessageHandler(Filters.text("About"), about))
    dispatcher.add_handler(MessageHandler(Filters.text("Manzil"), manzil))
    dispatcher.add_handler(MessageHandler(Filters.text("Rasm to PDF"), receive_image))
    dispatcher.add_handler(MessageHandler(Filters.document, img_to_pdf))
    dispatcher.add_handler(MessageHandler(Filters.photo, rasm))
    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, echo))



    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
