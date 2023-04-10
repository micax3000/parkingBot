import os
import logging
import handlers as hl
import services as s
import threading
from dotenv import load_dotenv
from telegram.ext import filters, ApplicationBuilder, CommandHandler, MessageHandler

load_dotenv()
telegram_api = os.getenv("TELEGRAM_API")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    f_stop = threading.Event()
    # start calling refreshTable every 30 sec
    s.refreshTable(f_stop)
    application = ApplicationBuilder().token(telegram_api).build()

    start_handler = CommandHandler('start', hl.start)
    parking_handler = CommandHandler('slobodna_mesta', hl.freeSlots)
    text_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), hl.start)
    location_handler = MessageHandler(filters.LOCATION, hl.location)

    application.add_handler(location_handler)
    application.add_handler(start_handler)
    application.add_handler(text_handler)
    application.add_handler(parking_handler)

    application.run_polling()



