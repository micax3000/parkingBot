import logging
import handlers as hl
import services as s
from telegram.ext import filters, ApplicationBuilder, CommandHandler, MessageHandler,ConversationHandler
from api import telegram_api

KOMANDA, STANJE, LOKACIJA = range(3)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    s.findSlots()
    application = ApplicationBuilder().token(telegram_api).build()

    # conv_handler = ConversationHandler(
    #     entry_points=[CommandHandler("start", hl.start)],
    #     states={
    #         STANJE: [hl.freeSlots],
    #     },
    #     fallbacks=[CommandHandler("cancel", hl.cancel)],
    # )
    start_handler = CommandHandler('start', hl.start)
    parking_handler = CommandHandler('parking', hl.freeSlots)
    text_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), hl.start)
    location_handler = MessageHandler(filters.LOCATION, hl.location)


    #application.add_handler(conv_handler)
    application.add_handler(location_handler)
    application.add_handler(start_handler)
    application.add_handler(text_handler)
    application.add_handler(parking_handler)

    application.run_polling()



