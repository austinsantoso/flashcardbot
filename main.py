#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from html import unescape

from src.spreadsheet import Sheet
from src.triviaBackend import get_trivia

import os
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# state
curState = 0
# 0 is inet, 1 is sheet
questionSource = 1
curQuestion = ""
curAnswer = ""
curSheet = Sheet("flashcardData")

stateDic = {"START": 0, "QUESTION": 1}

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

# handles help commands
# shows commands available with some descriptions
def handle_help(update, context):
    """Send a message when the command /help is issued."""
    print("help")
    helpMessage = "Available Commands:\n"
    helpMessage += "/start - starts a session\n"
    helpMessage += "/next - next question\n"
    helpMessage += "/stop - stops a session\n"
    print(update.callback_query)

    update.message.reply_text(helpMessage)



def show_question_inet(update, context):
    global curQuestion
    global curAnswer
    q, a = get_trivia()

    # to handle random html remarks like &quot
    curQuestion = unescape(q)
    curAnswer = a

    print("setting question")
    print("Question: ", curQuestion)
    print("Answer: ", curAnswer)

    keyboard = [[InlineKeyboardButton("True", callback_data='1'),
             InlineKeyboardButton("False", callback_data='0')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(curQuestion, reply_markup=reply_markup)

def show_question_sheet(update, context):
    global curQuestion
    global curAnswer
    q, a = curSheet.get_question()
    curQuestion = q
    curAnswer = a

    print("setting question")
    print("Question: ", curQuestion)
    print("Answer: ", curAnswer)

    keyboard = [[InlineKeyboardButton("Show Answer", callback_data='1')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(curQuestion, reply_markup=reply_markup)

def show_question(update, context):
    if questionSource == 0:
        show_question_inet(update, context)
    elif questionSource == 1:
        show_question_sheet(update, context)
    else:
        pass

# handles start command
# tells the users to select a source
# then starts showing the questions
def start_question(update, context):
    # get_data()
    update.message.reply_text("starting session")
    show_question(update, context)

# handles next command
# shows the users the next command
def next_question(update, context):
    if curQuestion == "":
        update.message.reply_text("start a session using /start")
    else:
        show_question(update, context)

# handles stop command
# stop giving questions
def stop_question(update, context):
    if curQuestion == "":
        update.message.reply_text("start a session using /start")
    else:
        resetState()
        update.message.reply_text("stopping session from " + "flashcardData")

def resetState():
    global curQuestion
    global curAnswer
    curQuestion = ""
    curAnswer = ""

def handle_text(update, context):
    print("handling text")
    if curState == 1:
        update.message.reply_text(curAnswer)


# To handle inine keyboard
def handleAnswerButton(update, context):
    print("Handling response")
    query = update.callback_query

    newText = curQuestion
    newText += "\nYour Answer = {}".format(query.data == "1")
    if questionSource == 0:
        newText += "\nCorrent Answer = " + curAnswer
    newText += "\n/next - for next question"

    query.edit_message_text(newText)
    # query.edit_message_reply_markup(InlineKeyboardMarkup([[]]))


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
    logger.info("Starting flashcardbot")
    main()
else:
    print("not starting")
