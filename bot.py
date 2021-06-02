import requests
import json
import time

token = '1833113848:AAFEJ2jhJn1nBw2D-pg4Wo61IQSJZtjVwek'
url = 'https://api.telegram.org/bot{}/'.format(token)


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
    params = {'chat_id': chat, 'text': text, }
    response = requests.post(url + 'sendMessage', data=params)
    return response


def send_keyboard(chat, text, keyboard):
    reply_markup = {"keyboard": keyboard,
                    "one_time_keyboard": True,
                    "resize_keyboard": True,
                    "selective": True}

    params = {'chat_id': chat, 'text': text, 'reply_markup': json.dumps(reply_markup)}
    response = requests.post(url + 'sendMessage', data=params)
    return response


chat_id = get_chat_id(last_update(get_updates_json(url)))
last_chat_text = get_last_message(last_update(get_updates_json(url)))

keyboard_alcohol = [["Вино", "Пиво", "Крепкие напитки", "Мартини/Текила"]]
keyboard_state = [["Мужчина", "Женщина"]]
keyboard_amount = [["100","250","500"],["750","1000","1 литр и больше"]]
keyboard_weight = [["50 ", "60","70"],["80","90","100"]]

def main():
    send_keyboard(chat_id, 'Укажите ваш пол:', keyboard_state)
    time.sleep(5)
    state = get_last_message(last_update(get_updates_json(url)))

    send_keyboard(chat_id, 'Что вы упортебляли?', keyboard_alcohol)
    time.sleep(5)
    alco = get_last_message(last_update(get_updates_json(url)))
    send_message(chat_id, ' Вижу вам нравится {}'.format(alco))
    time.sleep(1)

    send_keyboard(chat_id, 'Сколько грамм?', keyboard_amount)
    time.sleep(5)
    grams = get_last_message(last_update(get_updates_json(url)))

    send_keyboard(chat_id, 'Укажите , пожалуйтса , ваш вес',keyboard_weight)
    time.sleep(5)
    weight = get_last_message(last_update(get_updates_json(url)))

    if alco == 'Вино':
        spirt = int(grams)/10
    if alco == "Пиво":
        spirt = int(grams)/20
    if alco == "Крепкие напитки":
        spirt = int(grams)/(100/40)
    if alco == "Мартини/Текила":
        spirt = int(grams)/(100/12)


    if state == "Мужчина":
        kf = 0.7
    if state == "Женщина":
        kf = 0.6


    promile = round(spirt/(int(weight)*kf),2)
    send_message(chat_id, 'calculating')
    time.sleep(3)
    send_message(chat_id, 'promile is {}'.format(promile))
    
    if promile < 0.2:
        send_message(chat_id,"Садитесь за руль , но будьте аккуратны")
    else :
        send_message(chat_id, 'Пьяний за кермо не сiдай')
main()