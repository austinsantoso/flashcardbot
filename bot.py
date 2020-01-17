from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

import sys
import os
import logging
import json
import mysql.connector

# logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# config vars
# TOKEN = os.environ.get("telegram_bot_key")
# hostname = os.environ.get("database_hostname")
# username = os.environ.get("database_username")
# password = os.environ.get("database_password")

hostname = "remotemysql.com"
username = "VSzmsnRiHr"
password = "7bOTlzuZei"
TOKEN = '947178391:AAGFuTPrQ2gT0ZtJ3ziAJVVgih-dbI2Oybo'

# setting up database connection
db = mysql.connector.connect(
    host= hostname,
    user = username,
    passwd = password,
    database = username
)
db_cursor = db.cursor()

# drops the data base, and then recreates it
# use only when necessary
def resetDatabase():
    db_cursor.execute("DROP TABLE IF EXISTS Users")
    db_cursor.execute("CREATE TABLE Users(id INTEGER PRIMARY KEY AUTO_INCREMENT, userid INTEGER, current_source TEXT, current_question TEXT, current_answer TEXT, sources TEXT)")
    logger.debug("Reset database successful")

######################################################################################
# helper functions

# Gets the user id from the update
# or call back query
def getUserId(update):
    return update.message.chat.id

# retreives the given user data with selected value, default is * (all)
def getSelectedUserData(userID, value="*"):
    db_cursor.execute("SELECT " + value + " FROM Users WHERE userid=userID")
    return db_cursor.fetchall()

######################################################################################
# Command Handlers
def handleHelp(update, context):
    logger.info("handling help for userid " + str(getUserId(update)))

    helpMsg = "Here are the command available:\n"
    helpMsg += "/help - displays the help message"
    helpMsg += "/register - registers the user to use this bot"
    update.message.reply_text(helpMsg)

def handleRegister(update, context):
    userID = getUserId(update)
    logger.info("Handling register for userid " + str(userID))

    result = getSelectedUserData(userID)
    if len(result) != 0:
        logger.info("userid " + str(userID) + " already registered\nStart a session using /start")
        update.message.reply_text("You are already Registered")
    else:
        logger.info("registering new user " + str(userID))

        currentSource = ""
        currentQuestion = ""
        currentAnswer = ""
        newSources = json.dumps({})

        sql = "INSERT INTO Users (userid, current_source, current_question, current_answer, sources) " 
        sql += "VALUES (%s, %s, %s, %s, %s)"
        val = (userID, currentSource, currentQuestion, currentAnswer, newSources)
        db_cursor.execute(sql, val)
        db.commit()
        update.message.reply_text("You are now registered\nstart a session using /start")
        logger.info("new user " + str(userID) + " has been registered")

# clears all data of the user from the database
# doesn't check if the user exists
def handleUnregister(update, context):
    userID = getUserId(update)
    sql = "DELETE FROM customers WHERE userid=" + str(userID)
    db_cursor.execute(sql)
    db.commit()

    reply = "You are now Unregistered\n"
    reply += "All your data has been deleted\n\n"
    reply += "register using /register"
    update.message.reply_text(reply)

def handleAddSource(update, context):
    text = update.message.text
    textSplit = text.split(" ", 1)
    if len(textSplit) < 2:
        update.message.reply_text("Please insert a name as well\nExpected fromat:\n/addsource NAME")
    else:
        newName = textSplit[1]
        userID = getUserId(update)
        result = getSelectedUserData(userID, "sources")
        allSources = json.loads(result[0][0])
        allSourceKeys = allSources.keys()

        if newName in allSourceKeys:
            update.message.reply_text("Source name already exists, try a different name")
        else:
            allSources[newName] = []
            
            sql = "UPDATE Users SET sources = %s WHERE userid=%s"
            val = (json.dumps(allSources), str(userID))
            db_cursor.execute(sql, val)
            db.commit()

            update.message.reply_text("Successfully added source " + newName)

def handleRemoveSource(update, context):
    userID = getUserId(update)
    result = getSelectedUserData(userID, "sources")
    # sources = [("{}", )]
    allSources = json.loads(result[0][0])
    if len(allSources) == 0:
        update.message.reply_text("You have no sources to remove\nCreate a source using /addsource")
    else:
        allSourceKeys = allSources.keys()
        keyboard = [list(map(lambda x: InlineKeyboardButton(x, callback_data="1-"+x), allSourceKeys))]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text("Select a source to remove:\n", reply_markup=reply_markup)


# callback_data starts with '0-' to represent choosing source
def handleSelectSource(update, context):
    userID = getUserId(update)
    result = getSelectedUserData(userID, "sources")
    # sources = [("{}", )]
    allSources = json.loads(result[0][0])
    if len(allSources) == 0:
        update.message.reply_text("You have no sources to choose from\nMake a source using /addsource")
    else:
        allSourceKeys = allSources.keys()
        keyboard = [list(map(lambda x: InlineKeyboardButton(x, callback_data="0-"+x), allSourceKeys))]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text("Select a source:\n", reply_markup=reply_markup)

def handleShowSource(update, context):
    userID = getUserId(update)
    result = getSelectedUserData(userID, "current_source")
    # sources = [("{}", )]
    currentSource = result[0][0]
    if currentSource == "":
        update.message.reply_text("You have no sources to choose from\nSelect a source using /selectsource")
    else:
        update.message.reply_text("Your current source is:\n"+currentSource)

    pass

def handleAddQuestion(update, context):
    pass

# starts a session with a valid user.
# tells the user to select one of the chosen booklet
# Inline Keyboard starts with "0-"
def startSession(update, context):
    pass
    
def handleStart(update, context):
    userID = getUserId(update)
    result = getSelectedUserData(userID)
    if len(result) == 0:
        update.message.reply_text("Please register using /register first")
    else:
        startSession(update, context)

def handleInlineSelectSource(update, context):
    query = update.callback_query
    userID = getUserId(query)
    result = getSelectedUserData(userID)

    logger.info("handling inline keyboard in start for userid " + str(userID) + " query is " + query.data)

    querySplit = query.data.split("-", 1)
    if len(querySplit) <= 1:
        raise Exception("Invalid query callback " + query.data)
    else:
        selectedSource = querySplit[1]
        sql = "UPDATE Users SET current_source = %s WHERE userid=%s"
        val = (selectedSource, str(userID))
        db_cursor.execute(sql, val)
        db.commit()

        query.edit_message_text("you chose " + selectedSource)

def handleInlineRemoveSource(update, context):
    query = update.callback_query
    userID = getUserId(query)
    result = getSelectedUserData(userID)

    logger.info("handling inline keyboard for remove for userid " + str(userID) + " query is " + query.data)

    querySplit = query.data.split("-", 1)
    if len(querySplit) <= 1:
        raise Exception("Invalid query callback " + query.data)
    else:
        selectedSource = querySplit[1]
        sql = "UPDATE Users SET current_source = %s WHERE userid=%s"
        val = (selectedSource, str(userID))
        db_cursor.execute(sql, val)
        db.commit()

        query.edit_message_text("you chose " + selectedSource)
    pass

# To handle inine keyboard
def handleInlineKeyboardAll(update, context):
    query = update.callback_query
    userID = getUserId(query)

    logger.info("handling inline keyboard for userid " + str(userID) + " query is " + query.data)

    querySplit = query.data.split("-", 1)
    if len(querySplit) <= 1:
        raise Exception("query callback " + query.data +" is invalid")
    else:
        # select source
        if querySplit[0] == '0':
            handleInlineSelectSource(update, context)
        # remove source
        if querySplit[0] == '1':
            handleInlineRemoveSource(update, context)
# bot
def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Handles the inline button 
    dp.add_handler(CallbackQueryHandler(handleInlineKeyboardAll))

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("help", handleHelp))
    dp.add_handler(CommandHandler("register", handleRegister))
    dp.add_handler(CommandHandler("unregister", handleRegister))
    dp.add_handler(CommandHandler("showsource"), handleShowSource)
    dp.add_handler(CommandHandler("selectsource"), handleSelectSource)
    dp.add_handler(CommandHandler("addsource", handleAddSource))
    dp.add_handler(CommandHandler("removesource", handleRemoveSource))

    dp.add_handler(CommandHandler("start", handleStart))
    dp.add_handler(CommandHandler("next", handleNext))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
    pass

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'reset':
            resetDatabase()

    logger.info("flashcardBot starting")
    main()
else:
    logger.info("flashcardBot not starting")