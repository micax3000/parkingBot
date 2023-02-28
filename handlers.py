import telegram

import services as s
from telegram.ext import ContextTypes,ConversationHandler
from telegram import Update, ReplyKeyboardMarkup,ReplyKeyboardRemove, KeyboardButton


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #reply_keyboard = [["/parking", "Lokacija"]]

    custom_keyboard = [[KeyboardButton('/parking'),KeyboardButton('lokacija',request_location=True)]]

    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard,resize_keyboard=True, one_time_keyboard=False)
    await context.bot.send_message(chat_id=update.effective_chat.id,text = '/parking - Slobodna mesta po parkingu\nPosalji svoju lokaciju ako zelis da pronadjes najblize parkiraliste sa slobodnim mestima',reply_markup=reply_markup)
    # await update.message.reply_text("Parking bot",
    #     reply_markup=ReplyKeyboardMarkup(
    #         reply_keyboard,resize_keyboard=True, one_time_keyboard=False, input_field_placeholder="Izaberi komandu"
    #     ),
    # )
    #await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Zdravo {update.effective_chat.first_name}')


async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Nepoznata komanda. Pokusaj ponovo.")


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    parking_info = await s.calculateDistances(update.message.location.latitude, update.message.location.longitude)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Najblizi parking je: {parking_info[0]}\n na adresi: {parking_info[1]}\n sa: {parking_info[2]} slobodnih mesta')
    parking_info = parking_info[3].split(',')
    await context.bot.send_location(chat_id=update.effective_chat.id, latitude=parking_info[0],
                                    longitude=parking_info[1])


async def freeSlots(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Slobodna mesta po garazama:\n\n" + '\n'.join(s.findSlots()))

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END