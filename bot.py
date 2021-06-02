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

    params = {'chat_id': chat, 'text': text,
              'reply_markup': json.dumps(reply_markup)}
    response = requests.post(url + 'sendMessage', data=params)
    return response


chat_id = get_chat_id(last_update(get_updates_json(url)))
# last_chat_text = get_last_message(last_update(get_updates_json(url)))

keyboard_alcohol = [["Вино", "Пиво", "Крепкие напитки", "Мартини"]]
keyboard_state = [["Мужчина", "Женщина"]]
keyboard_amount = [["100", "250", "500"], ["750", "1000", "1 литр и больше"]]
keyboard_weight = [["50 ", "60", "70"], ["80", "90", "100"]]


def get_state():
    send_keyboard(chat_id, 'Укажите ваш пол:', keyboard_state)
    time.sleep(4)
    state = get_last_message(last_update(get_updates_json(url)))
    print('state = {}'.format(state))
    return state


def get_drink():
    send_keyboard(chat_id, 'Что вы упортебляли?', keyboard_alcohol)
    time.sleep(4)
    alco = get_last_message(last_update(get_updates_json(url)))
    print('alco = {}'.format(alco))
    send_message(chat_id, ' Вижу вам нравится {}'.format(alco))
    time.sleep(1)
    return alco


def get_amount():
    send_keyboard(chat_id, 'Сколько грамм?', keyboard_amount)
    time.sleep(4)
    grams = int(get_last_message(last_update(get_updates_json(url))))
    print('grams = {}'.format(grams))
    return grams


def get_weight():
    send_keyboard(chat_id, 'Укажите , пожалуйтса , ваш вес', keyboard_weight)
    time.sleep(4)
    weight = int(get_last_message(last_update(get_updates_json(url))))
    print('weight = {}'.format(weight))
    return weight


def calculate_promile(grams, alco, state, weight):
    alcohol_gradus = {'Вино': 12, "Пиво": 5,
                      "Крепкие напитки": 40, "Мартини": 13}
    states = {'Мужчина': 0.7, 'Женщина': 0.6}
    spirt = grams*(alcohol_gradus[alco]/100)
    kf = states[state]
    promile = round(spirt/(weight*kf), 2)
    return promile


def send_answer(promile):
    send_message(chat_id, 'calculating')
    time.sleep(2)
    send_message(chat_id, 'promile is {}'.format(promile))
    time.sleep(1)
    send_message(
        chat_id, 'По закону Украины , водить машину можно , если в крови\
         содержится +  до 0.2 промиле алкоголя ')

    if promile < 0.2:
        send_message(chat_id, "Садитесь за руль , но будьте аккуратны")
    else:
        send_message(chat_id, 'Пьяний за кермо не сiдай')


def main():
    state = get_state()
    alco = get_drink()
    grams = get_amount()
    weight = get_weight()
    promile = calculate_promile(grams, alco, state, weight)
    send_answer(promile)


while True:
    send_message(chat_id, 'Привет , бот показывает можно ли вам садиться\
         за руль . Просто введите свои парметры')
    time.sleep(3)
    main()
    break
