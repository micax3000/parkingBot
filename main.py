import logging
import handlers as hl
from telegram.ext import filters,ApplicationBuilder, CommandHandler, MessageHandler

with open('api.txt') as f:
    APIKEY = f.readline()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    application = ApplicationBuilder().token(APIKEY).build()

    start_handler = CommandHandler('start', hl.start)
    slots_handler = CommandHandler('slots',hl.freeSlots)
    text_handler = MessageHandler(filters.TEXT & (~filters.COMMAND),hl.text)

    application.add_handler(start_handler)
    application.add_handler(text_handler)
    application.add_handler(slots_handler)

    application.run_polling()