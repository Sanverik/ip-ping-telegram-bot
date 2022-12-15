import os
import requests
import telebot


BOT_TOKEN = os.environ.get('BOT_TOKEN')
IP = os.environ.get('IP')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
KEY_VALUE_STORE_TOKEN = os.environ.get('KEY_VALUE_STORE_TOKEN')


def is_light_enabled():
    response = requests.get(f'https://keyvalue.immanuel.co/api/KeyVal/GetValue/{KEY_VALUE_STORE_TOKEN}/light')
    return True if response.json() == '1' else False


def update_light_status(value):
    requests.post(f'https://keyvalue.immanuel.co/api/KeyVal/UpdateValue/{KEY_VALUE_STORE_TOKEN}/light/{value}')


def ping_and_notify():
    response = os.system(f'ping -c 1 {IP}')
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


def lambda_handler(event, context):
    ping_and_notify()
