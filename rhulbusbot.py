from telegram.ext import *
import logging, telegram

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi! RHUL Bus Bot will let you know when bus 441 is coming! Use /here so I can get your location to find the nearest busstop and /when to see when the bus is coming!')

def help(bot, update):
    update.message.reply_text('RHUL Bus Bot -\n /here -get location and select busstop \n /when to get the time the bus would arrive')

def here(bot, update):
    location_keyboard = telegram.KeyboardButton(text="Send Location", request_location=True)
    reply_markup = telegram.ReplyKeyboardMarkup([[location_keyboard]])
    bot.sendMessage(chat_id=update.message.chat_id, 
                text="Would you mind sharing your location with me?", 
                reply_markup=reply_markup)

def when(bot, update):
    update.message.reply_text('RHUL Bus Bot -\n /here -get location and select busstop \n /when to get the time the bus would arrive')

def location(bot, update):
    reply_markup = telegram.ReplyKeyboardRemove()
    bot.sendMessage(chat_id=update.message.chat_id, text="Thanks!", reply_markup=reply_markup)

def echo(bot, update):
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("303464706:AAGHlyIH1htjdwaRuKESG07Qlv-nrdp77lA")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("here", here))
    dp.add_handler(CommandHandler("when", when))

    # on noncommand i.e message - Wecho the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_handler(MessageHandler(Filters.location, location))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
