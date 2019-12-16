#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from random import randint
from html import unescape

from src.spreadsheet import sheet
from src.triviaBackend import get_trivia

import os

curQuestion = ""
curAnswer = ""
curSheet = ""

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hewo!')


def handle_help(update, context):
    """Send a message when the command /help is issued."""
    print("help")
    helpMessage = "Available Commands:\n"
    helpMessage += "/start - starts a session\n"
    helpMessage += "/next - next question\n"
    helpMessage += "/stop - stops a session\n"
    print(update.callback_query)

    update.message.reply_text(helpMessage)


def get_data():
    ss = sheet("flashcardData")
    global curSheet
    curSheet = ss.get_all_values()


def get_question2(update, context):
    dataLength = len(curSheet)  # header
    if dataLength < 2:
        print("no data found")
        update.message.reply_text("No Data found")
    else:
        index = randint(1, dataLength - 1)

        global curQuestion
        global curAnswer
        print("getting question at index " + str(index))
        question, answer = curSheet[index]
        curQuestion = question
        curAnswer = answer
        update.message.reply_text(curQuestion)


def set_question():
    global curQuestion
    global curAnswer
    q, a = get_trivia()

    # to handle random html remarks like &quot
    curQuestion = unescape(q)
    curAnswer = a

    print("setting question")
    print("Question: ", curQuestion)
    print("Answer: ", curAnswer)


def show_question(update, context):
    set_question()
    print("showing a question")
    keyboard = [[InlineKeyboardButton("True", callback_data='1'),
             InlineKeyboardButton("False", callback_data='0')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(curQuestion, reply_markup=reply_markup)


def start_question(update, context):
    # get_data()
    update.message.reply_text("starting session")
    show_question(update, context)


def stop_question(update, context):
    if curQuestion == "":
        update.message.reply_text("start a session using /start")
    else:
        resetState()
        update.message.reply_text("stopping session from " + "flashcardData")


def next_question(update, context):
    if curQuestion == "":
        update.message.reply_text("start a session using /start")
    else:
        show_question(update, context)


def resetState():
    global curQuestion
    global curAnswer
    curQuestion = ""
    curAnswer = ""

def handle_text(update, context):
    print("handling text")
    if curAnswer == "":
        resetState()
    else:
        update.message.reply_text(curAnswer)


def handleAnswerButton(update, context):
    print("Handling response")
    query = update.callback_query

    newText = curQuestion
    newText += "\nYour Answer = {}".format(query.data == "1")
    newText += "\nCorrent Answer = " + curAnswer
    newText += "\n/next - for next question"

    query.edit_message_text(text=newText)
    query.edit_message_reply_markup(reply_makrup=[])


def main():
    TOKEN = os.environ.get("telegram_bot_key")

    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Handles the inline button 
    dp.add_handler(CallbackQueryHandler(handleAnswerButton))

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("help", handle_help))
    dp.add_handler(CommandHandler("start", start_question))
    dp.add_handler(CommandHandler("next", next_question))
    dp.add_handler(CommandHandler("stop", stop_question))


    # dp.add_handler(MessageHandler(Filters.text, handle_text))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    print("Starting austinFirstBot")
    main()
else:
    print("not starting")
