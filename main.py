import logging
import handlers as hl
import services as s
from telegram.ext import filters, ApplicationBuilder, CommandHandler, MessageHandler
from api import distance_api, telegram_api

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    s.findSlots()
    application = ApplicationBuilder().token(telegram_api).build()

    start_handler = CommandHandler('start', hl.start)
    parking_handler = CommandHandler('parking', hl.freeSlots)
    text_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), hl.text)
    location_handler = MessageHandler(filters.LOCATION, hl.location)

    application.add_handler(location_handler)
    application.add_handler(start_handler)
    application.add_handler(text_handler)
    application.add_handler(parking_handler)

    application.run_polling()



