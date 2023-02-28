import services as s
from telegram.ext import ContextTypes
from telegram import Update


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Zdravo {update.effective_chat.first_name}')


async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="not a command.Try again.")


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #await s.calculateDistances(update.message.location.latitude, update.message.location.longitude)
    parking_info = await s.calculateDistances(update.message.location.latitude, update.message.location.longitude)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Najblizi parking je: {parking_info[0]}\n na adresi: {parking_info[1]}\n sa: {parking_info[2]} slobodnih mesta')
    parking_info = parking_info[3].split(',')
    await context.bot.send_location(chat_id=update.effective_chat.id, latitude=parking_info[0],
                                    longitude=parking_info[1])


async def freeSlots(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Slobodna mesta po garazama:\n\n" + '\n'.join(s.findSlots()))
