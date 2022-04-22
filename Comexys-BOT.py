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
    d_users = {}

class user_data:
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


def save_csv(file_name, lines):
    with open(file_name, 'w') as f:
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

    date_format = '%d/%m/%Y'
    time_format = '%H:%M:%S'

    csv_file_name = datetime.now().strftime('%d-%m-%Y - %H-%M-%S.csv')

    save_csv(csv_file_name, tbl)


    fid = open(csv_file_name,'r')
    bot.send_document(message.chat.id, fid)
    fid.close()

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    print(f'got: {message}')


@bot.message_handler(content_types=['location'])
def handle_location(message):
    user_id = message.from_user.id
    if user_id in db.d_users:
        ud = db.d_users[user_id]
    else:
        ud = db.d_users[user_id] = user_data()

    ud.user_name = f'{message.chat.first_name} {message.chat.last_name}'
    ud.loc_time = datetime.now().strftime(time_format)
    ud.lat = message.location.latitude
    ud.long = message.location.longitude
    # bot.send_message(message.chat.id, f"Got location : {ud.lat}, {ud.long}")

    print(f"Got location : {ud.lat}, {ud.long}")


@bot.message_handler(content_types=['photo'])
def photo(message):
    location_needed = True
    user_id = message.from_user.id
    if user_id in db.d_users:
        ud = db.d_users[user_id]
        time_str = datetime.now().strftime(time_format)
        tdelta = datetime.strptime(time_str, time_format) - datetime.strptime(ud.loc_time, time_format)
        if tdelta.seconds < (3 * 60):
            location_needed = False

    if location_needed:
        bot.send_message(message.chat.id, "You have to send your location first!", reply_markup=gen_markup2())
        return

    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    jpg_file_name = f'{user_id}.jpg'
    with open(jpg_file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    with open(jpg_file_name, 'rb') as image_file:
        image = Image.open(image_file)
        image.load()

#    codes = zbarlight.scan_codes(['qrcode'], image)
    decoded_img = pyzbar.decode(image)
    if decoded_img:
        codes = decoded_img[0].data.decode()
        bot.send_message(message.chat.id, f'QR codes: {codes}' )
        print (f'Got code: {codes}')
        if codes[:7] == 'Comexys':
            ud.qr_code = codes
            ud.qr_time = time_str
            update_table(ud)
        else:
            bot.send_message(message.chat.id, 'Unknown QR code, scan only Comexys QR code.')
    else:
        bot.send_message(message.chat.id, 'Can''t read the QR code, please scan again')

tbl = ['Contractor Name, Installation Date, Send Location time, Location X, Location Y,'+
       'Send QR Time, Producer, Product Name, Frequency MHz, RF Channel, RF Number, Mac Address, '+
       'Production date, Remarks']


def update_table(ud):
    date = datetime.now().strftime(date_format)
    line = f'{ud.user_name},{date}, {ud.loc_time},{ud.lat},{ud.long},{ud.qr_time},{ud.qr_code}'
    tbl.append(line)


@bot.message_handler(content_types=['document'])
def document(message):
    pass



if __name__=='__main__':
    main()