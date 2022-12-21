import os
import time
import requests
import telebot


BOT_TOKEN = os.environ.get('BOT_TOKEN')
TARGET_IP = os.environ.get('TARGET_IP')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
KEY_VALUE_STORE_TOKEN = os.environ.get('KEY_VALUE_STORE_TOKEN')


def is_light_enabled():
    with open('light_db', 'r') as f:
        return f.readline() == '1'
    # response = requests.get(f'https://keyvalue.immanuel.co/api/KeyVal/GetValue/{KEY_VALUE_STORE_TOKEN}/light')
    # return response.json() == '1'


def update_light_status(value):
    with open('light_db', 'w') as f:
        f.write(value)
    # requests.post(f'https://keyvalue.immanuel.co/api/KeyVal/UpdateValue/{KEY_VALUE_STORE_TOKEN}/light/{value}')


def ping_and_notify():
    response = os.system(f'ping -c 1 {TARGET_IP}')
    bot = telebot.TeleBot(BOT_TOKEN)
    if response == 0:
        bot.send_message(CHANNEL_ID, '/dream_off')
        if not is_light_enabled():
            message = bot.send_message(CHANNEL_ID, 'light turned on')
            bot.pin_chat_message(CHANNEL_ID, message.message_id)
            update_light_status('1')
    else:
        bot.send_message(CHANNEL_ID, '/dream_on')
        if is_light_enabled():
            message = bot.send_message(CHANNEL_ID, 'light turned off')
            bot.pin_chat_message(CHANNEL_ID, message.message_id)
            update_light_status('0')


def handler():
    while True:
        try:
            ping_and_notify()
            time.sleep(60)
        except Exception as e:
            print(e)
            time.sleep(5)


if __name__ == '__main__':
    handler()
