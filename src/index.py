import os
import time
import telebot

BOT_TOKEN = os.environ.get('BOT_TOKEN')
TARGET_IP = os.environ.get('TARGET_IP')
CHANNEL_ID = os.environ.get('CHANNEL_ID')


def init():
    if not os.path.exists('../efs/light_db'):
        with open('../efs/light_db', 'w') as f:
            # assumption
            f.write('1')


def is_light_enabled():
    with open('../efs/light_db', 'r') as f:
        return f.readline() == '1'


def update_light_status(value):
    with open('../efs/light_db', 'w') as f:
        f.write(value)


def ping_and_notify():
    response = os.system(f'ping -c 5 {TARGET_IP}')
    bot = telebot.TeleBot(BOT_TOKEN)
    if response == 0:
        if not is_light_enabled():
            message = bot.send_message(CHANNEL_ID, 'Світло й інтернет появилися!')
            bot.pin_chat_message(CHANNEL_ID, message.message_id)
            bot.send_message(CHANNEL_ID, '/dream_off')
            update_light_status('1')
    else:
        if is_light_enabled():
            message = bot.send_message(CHANNEL_ID, 'Світло й інтернет зникли!')
            bot.pin_chat_message(CHANNEL_ID, message.message_id)
            bot.send_message(CHANNEL_ID, '/dream_on')
            update_light_status('0')


def handler():
    while True:
        try:
            ping_and_notify()
            time.sleep(20)
        except Exception as e:
            print(e)
            time.sleep(5)


if __name__ == '__main__':
    init()
    handler()
