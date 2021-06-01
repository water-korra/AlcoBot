import requests
import json
import time

url = 'https://api.telegram.org/bot1833113848:AAFEJ2jhJn1nBw2D-pg4Wo61IQSJZtjVwek/'

def get_updates_json(request):
    response = requests.get(request + 'getUpdates')
    return response.json()


def last_update(data):
    results = data['result']
    total_updates = len(results) - 1
    print(total_updates)
    return results[total_updates]

def get_chat_id(update):
    chat_id = update['message']['chat']['id']
    return chat_id

def get_last_message(update):
    last_chat_text = update['message']['text']
    return last_chat_text

def send_message(chat, text):
    params = {'chat_id': chat, 'text': text,}
    response = requests.post(url + 'sendMessage', data=params)
    return response

def send_keyboard(chat, text):
    reply_markup = {"keyboard": [["1", "2"], ["3"]], "one_time_keyboard": True,
                "resize_keyboard": True}
    params = {'chat_id': chat, 'text': text, 'reply_markup' : json.dumps(reply_markup)}
    response = requests.post(url + 'sendMessage', data=params)
    return response

chat_id = get_chat_id(last_update(get_updates_json(url)))
last_chat_text = get_last_message(last_update(get_updates_json(url)))
