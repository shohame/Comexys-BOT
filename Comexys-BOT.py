import telebot
import cv2
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
import requests
import os
import glob
import qrcode

from pyzbar import pyzbar
from PIL import Image


class database:
    lat = 0
    long = 0



db = database()

TELEGRAM_TOKEN = '5153464758:AAGr4ylPuoakXy0TrzcKDHxeVsB5kdxNDb8'
bot = telebot.TeleBot(TELEGRAM_TOKEN)

def main():

    print ('Starting BOT...')
    bot.polling(none_stop=True)


def gen_markup2():

    reply_markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
    location_keyboard = KeyboardButton(text="Send location", request_location=True)
    send_keyboard = KeyboardButton('Send File', request_contact=True)
    reply_markup.add(location_keyboard)

    reply_markup.add('Done, Send File...')
#    reply_markup.add(location_keyboard)
    return reply_markup


@bot.message_handler(commands=['start'])
def start(message):
        bot.send_message(message.chat.id,"Share yore location", reply_markup=gen_markup2())

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    print (f'got: {message}')
@bot.message_handler(content_types=['location'])
def handle_location(message):
    db.lat = message.location.latitude
    db.long = message.location.longitude
    print(f"Location = {db.lat}, {db.long}")


@bot.message_handler(content_types=['photo'])
def photo(message):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)

    with open("image.jpg", 'rb') as image_file:
        image = Image.open(image_file)
        image.load()
    #   image = downloaded_file
#    codes = zbarlight.scan_codes(['qrcode'], image)

    codes = pyzbar.decode(image)[0].data

    msg = 'QR codes: %s' % codes
    print(message.location)
    print(msg)
    bot.send_message(message.chat.id, msg)


if __name__=='__main__':
    main()