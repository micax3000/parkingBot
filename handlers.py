import logging
import telegram

import services as serv
from telegram.ext import ContextTypes
from telegram import Update, KeyboardButton

introductionText = 'Parking bot je dizajniran da pomogne korisnicima da pronađu dostupna parking mesta u Beogradu.' \
                   ' Bot ima dve komande: /slobodna_mesta i slanje lokacije. Komanda /slobodna_mesta pruža korisniku listu svih dostupnih parking mesta u oblasti i' \
                   ' trenutni broj slobodnih mesta u svakom parkingu.\n' \
                    'Klikom na dugme `pronadji parking` korisnik salje svoju lokaciju botu,a bot će izračunati najbliže parking mesto sa slobodnim mestima. Klikom na dobijenu lokaciju moze se pronaci putanja od Vase lokacije do najblizeg parkinga.' \

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    custom_keyboard = [[KeyboardButton('/slobodna_mesta'), KeyboardButton('pronadji parking', request_location=True)]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=introductionText,
                                   reply_markup=reply_markup)


async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Nepoznata komanda. Pokusaj ponovo.")


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f'calculate distances run for (lat:{update.message.location.latitude},long:{update.message.location.longitude})')
    parking_info = await serv.calculateDistances(update.message.location.latitude, update.message.location.longitude)
    if parking_info == None:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f'Bot je dostigao maksimum zahteva po danu')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f'Najblizi parking je: {parking_info[0]}\nna adresi: {parking_info[1]}\nsa: {parking_info[2]} slobodnih mesta')
        parking_info = parking_info[3].split(',')
        await context.bot.send_location(chat_id=update.effective_chat.id, latitude=parking_info[0],
                                        longitude=parking_info[1])


async def freeSlots(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info('freeSlots run')
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Slobodna mesta po garazama:\n\n" + '\n'.join([f'{item[1][0]}: {item[1][1]}' for item in serv.parking_slots_state.items()]))
