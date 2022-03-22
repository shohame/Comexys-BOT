import telebot
import cv2
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
import requests
import os
import glob
class database:
    mac_address = ''
    rf_id = 0

db = database()

TELEGRAM_TOKEN = '5153464758:AAGr4ylPuoakXy0TrzcKDHxeVsB5kdxNDb8'
bot = telebot.TeleBot(TELEGRAM_TOKEN)

def main():

    print ('Starting BOT...')
    bot.polling(none_stop=True)


import qrcode


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 8
    markup.add(InlineKeyboardButton("New QRC", callback_data="new_qr_code"))
    return markup


def gen_markup2():
    keyboard = ['aa', 'bb']

    reply_markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
    location_keyboard = KeyboardButton(text="Send location", request_location=True)
    send_keyboard = KeyboardButton('Send File', request_contact=True)

    reply_markup.add('try', 'help')
    reply_markup.add(location_keyboard)
#    reply_markup.add(location_keyboard)
    return reply_markup


@bot.message_handler(commands=['start'])
def start(message):
    if False:
        location_keyboard = KeyboardButton(text="send_location")
        bot.send_message(message.chat.id, f'Wellcome {message.from_user.first_name} {message.from_user.last_name}',
                         reply_markup=gen_markup())
    else:
        bot.send_message(message.chat.id,"Share yore location", reply_markup=gen_markup2())
     #   message.reply_markup("Share yore location",  reply_markup=gen_markup2())

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "new_qr_code":
        start_new_qr_code(call)


def start_new_qr_code(call):
    sent = bot.send_message(call.message.chat.id, 'Enter MAC address (e.g - A0-04-FB-D3-7E-0C):')
    bot.register_next_step_handler(sent, verify_mac_address)


def verify_mac_address(message):
    db.mac_address = message.text

    bot.send_message(message.chat.id, f'You have entered MAC adress: {db.mac_address}')

    sent = bot.send_message(message.chat.id, 'Enter RF ID (1 - 245):')
    bot.register_next_step_handler(sent, verify_rf_id)


def verify_rf_id(message):
    db.rf_id = int(message.text)
    bot.send_message(message.chat.id, f'You have entered RF ID: {db.rf_id}')

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(f'Comexys,ZD2239868,{db.mac_address},{db.rf_id}')
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save('qrcode001.png')
    Ie2 = open("qrcode001.png", 'rb')
    bot.send_photo(message.chat.id, Ie2)
    bot.send_message(message.chat.id, 'Done...', reply_markup=gen_markup())


@bot.message_handler(content_types=['location'])
def handle_location(message):
    print("{0}, {1}".format(message.location.latitude, message.location.longitude))

from pyzbar import pyzbar
from PIL import Image


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