import requests

url = "https://api.telegram.org/bot542049341:AAHI3mmtjbP_w3Fi_mhLvFFPhbBf5Lp1rn0/"


def get_updates_json(request):
    response = requests.get(request + 'getUpdates')
    return response.json()


def last_update(data):
    results = data['result']
    total_updates = len(results) - 1
    return results[total_updates]

def get_chat_id(update):
    chat_id = update['message']['chat']['id']
    return chat_id

def send_mess(chat, text):
    params = {'chat_id': chat, 'text': text}
    response = requests.post(url + 'sendMessage', data=params)
    return response

chat_id = get_chat_id(last_update(get_updates_json(url)))

send_mess(chat_id, 'Your message goes here')

def main():
    update_id = last_update(get_updates_json(url))['update_id']
    while True:
        if update_id == last_update(get_updates_json(url))['update_id']:
           send_mess(get_chat_id(last_update(get_updates_json(url))), 'test')
           update_id += 1
    sleep(1)

if __name__ == '__main__':
    main()



import sys
import time
import random
import datetime
import requests
import telegram
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


bot = telegram.Bot(token='542049341:AAHI3mmtjbP_w3Fi_mhLvFFPhbBf5Lp1rn0')
greetings = ('hello', 'hi', 'greetings', 'sup')
now = datetime.datetime.now()

def parse_cmd_text(text):
    # Telegram understands UTF-8, so encode text for unicode compatibility
    # Handle /xxx@ABCBot 123
    text = text.encode('utf-8')
    cmd = None
    if '/' in text:
        try:
            index = text.index(' ')
        except ValueError as e:
            return (text, None)
        cmd = text[:index]
        text = text[index + 1:]
    if not cmd == None and '@' in cmd:
        cmd = cmd.replace(bot_name, '')
    return (cmd, text)


def handle_message(message):
    text = message.text
    if '/roll' in text:
        rollAdice()
    elif '/time' in text:
        showTime(message)
    if not '/' in text and '@' in text:
        echo(message)


def handle(msg):
    chat_id = msg['message']['chat']['id']
    command = msg['message']['text']

    if command == '/roll':
        n = random.randint(1,6)
        greet_bot.send_message(chat_id,n)
    elif command == '/time':
        d = str(datetime.datetime.now())
        greet_bot.send_message(chat_id,d)
        greet_bot.send_message(chat_id,now)
    else:
        greet_bot.send_message(chat_id, command)


def main():
    new_offset = None
    today = now.day
    hour = now.hour

    while True:
        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']

        handle(last_update)

        # if last_chat_text.lower() in greetings and today == now.day and 6 <= hour < 12:
        #     greet_bot.send_message(last_chat_id, 'Good Morning  {}'.format(last_chat_name))
        #     today += 1
        #
        # elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
        #     greet_bot.send_message(last_chat_id, 'Good Afternoon {}'.format(last_chat_name))
        #     today += 1
        #
        # elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
        #     greet_bot.send_message(last_chat_id, 'Good Evening  {}'.format(last_chat_name))
        #     today += 1
        #
        # greet_bot.send_message(last_chat_id, 'Test  {}'.format(last_chat_name))
        #
        # pip3 install python-telegram-bot
        new_offset = last_update_id + 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()