import telebot
import cv2
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
import requests
import os
import glob
import qrcode
import pandas as pd

from pyzbar import pyzbar
from PIL import Image
from datetime import datetime

date_format = '%d/%m/%Y'
time_format = '%H:%M:%S'

class database:
    user_name = ''
    loc_time = '00:00:00'
    lat = 0
    long = 0
    qr_time = '00:00:00'
    qr_code = ''


db = database()

TELEGRAM_TOKEN = '5153464758:AAGr4ylPuoakXy0TrzcKDHxeVsB5kdxNDb8'
bot = telebot.TeleBot(TELEGRAM_TOKEN)

def main():

    print ('Starting BOT...')
    bot.polling(none_stop=True)


def save_csv(lines):
    with open('try.csv', 'w') as f:
        for line in lines:
            f.write(line)
            f.write('\n')

def gen_markup2():

    reply_markup = ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True,
                                       row_width=7)
    location_keyboard = KeyboardButton(text="Send location", request_location=True)
   # send_keyboard = KeyboardButton('Send File', request_contact=True)
    reply_markup.add(location_keyboard)

  #  reply_markup.add('Send File')
#    reply_markup.add(location_keyboard)
    return reply_markup


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,"Share yore location", reply_markup=gen_markup2())

@bot.message_handler(commands=['download'])
def download(message):
    print (tbl)
    print ('Done...')
    save_csv(tbl)
    fid = open('try.csv','r')
    bot.send_document(message.chat.id, fid)
    fid.close()

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    print(f'got: {message}')


@bot.message_handler(content_types=['location'])
def handle_location(message):
    db.user_name = f'{message.chat.first_name} {message.chat.last_name}'
    db.loc_time = datetime.now().strftime(time_format)
    db.lat = message.location.latitude
    db.long = message.location.longitude
    print(f"Got location : {db.lat}, {db.long}")


@bot.message_handler(content_types=['photo'])
def photo(message):

    time_str = datetime.now().strftime(time_format)
    tdelta = datetime.strptime(time_str, time_format) - datetime.strptime(db.loc_time, time_format)
    if tdelta.seconds > (3 * 60):
        bot.send_message(message.chat.id, "You have to send your location first!", reply_markup=gen_markup2())
        return

    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)

    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)

    with open("image.jpg", 'rb') as image_file:
        image = Image.open(image_file)
        image.load()

#    codes = zbarlight.scan_codes(['qrcode'], image)
    decoded_img = pyzbar.decode(image)
    if decoded_img:
        codes = decoded_img[0].data.decode()
        bot.send_message(message.chat.id, f'QR codes: {codes}' )
        print (f'Got code: {codes}')
        if codes[:7] == 'Comexys':
            db.qr_code = codes
            db.qr_time = time_str
            update_table(db)
        else:
            bot.send_message(message.chat.id, 'Unknown QR code, scan only Comexys QR code.')
    else:
        bot.send_message(message.chat.id, 'Can''t read the QR code, please scan again')

tbl = ['Contractor Name, Installation Date, Send Location time, Location X, Location Y,'+
       'Send QR Time, Producer, Product Name, RF Number, Mac Address, Frequency MHz,'+
       'RF Channel, Production date, Remarks']


def update_table(db):
    date = datetime.now().strftime(date_format)
    line = f'{db.user_name},{date}, {db.loc_time},{db.lat},{db.long},{db.qr_time},{db.qr_code}'
    tbl.append(line)


@bot.message_handler(content_types=['document'])
def document(message):
    pass



if __name__=='__main__':
    main()