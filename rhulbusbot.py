from telegram.ext import *
from telegram import *
import logging, math, csv
import requests, json, simplejson, urllib

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# User Location Dictionary
user_location_db = {}

#  Load 441 busstops into the memory
stringdata = csv.reader(open('441.csv'))
#stringdata = re.findall('(.*), (.*), (.*)',open('441.csv').read())
data = [(l,float(x),float(y)) for l,x,y in stringdata]

print stringdata

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi! RHUL Bus Bot will let you know when bus 441 is coming!\n The bot uses the real time bus location to estimate the time required to reach the busstop\n  Use /here so I can get your location to find the nearest busstop and /when to see when the bus is coming!')

def help(bot, update):
    update.message.reply_text('RHUL Bus Bot -\n /here -get location and select busstop \n' +
					' /when to get the time the bus would arrive')

def here(bot, update):
    location_keyboard = KeyboardButton(text="Send Location", request_location=True)
    reply_markup = ReplyKeyboardMarkup([[location_keyboard]])
    bot.sendMessage(chat_id=update.message.chat_id, 
                text="Would you mind sharing your location with me?", 
                reply_markup=reply_markup)

def when(bot, update):

    data = {
      'ticketerservice': '441',
      'service': '441',
      'operatorRef': 'ABSU',
      'direction': 'inbound',
      'timestamp': 'Tue Jan 31 2017 14:25:26 GMT+0000 (GMT Standard Time)'
    }
    data = requests.post('http://absu.coachparks.com/widget/GetLiveBuses', data=data)
    jdata = json.loads(data.content)
    for bus in jdata['Buses']:
        orig_lat =  51.426634
        orig_lng =  -0.572648
        dest_lat = float(bus['Latitude'])
        dest_lng = float(bus['Longitude'])

        orig_coord = str(orig_lat) + "," +str(orig_lng)
        dest_coord = str(dest_lat)+"," +str(dest_lng)
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="+str(orig_coord)+"&destinations="+str(dest_coord)+"&mode=driving&key=AIzaSyBJz8a7fpvQ0-DPQa7aQvamU4wOlC6EKn0"
        result= simplejson.load(urllib.urlopen(url))
        print result
        driving_time = result['rows'][0]['elements'][0]['duration']['value']
        print driving_time
    update.message.reply_text('RHUL Bus Bot -\n /here -get location and select busstop \n /when to get the time the bus would arrive')

def location(bot, update):
    global user_location_db
    global data
    user_location = update.message.location
    user_location_db[update.message.chat_id] = user_location

    reply_markup = ReplyKeyboardRemove()
    bot.sendMessage(chat_id=update.message.chat_id, text="Thanks! Now select the busstop you are going!", reply_markup=reply_markup)

    p = [user_location.latitude, user_location.longitude]
    sorteddata = sorted(data, key=lambda d: dist(p,d[1:]))

    print data
    print sorteddata
    keyboard = [
                [InlineKeyboardButton(sorteddata[0][0], callback_data=sorteddata[0])],
                [InlineKeyboardButton(sorteddata[1][0], callback_data=sorteddata[1])],
                [InlineKeyboardButton(sorteddata[2][0], callback_data=sorteddata[2])],
                [InlineKeyboardButton(sorteddata[3][0], callback_data=sorteddata[3])],
                [InlineKeyboardButton(sorteddata[4][0], callback_data=sorteddata[4])],
                [InlineKeyboardButton(sorteddata[5][0], callback_data=sorteddata[5])]
               ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def button(bot, update):
    query = update.callback_query

    choicebusstop = query.data

    bot.editMessageText(text="Selected option: %s" % choicebusstop[0],
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)



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
    dp.add_handler(CallbackQueryHandler(button))
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


def dist(a,b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)



if __name__ == '__main__':
    main()
