import requests
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import time
import datetime

# telegram bot settings
bot_url = "https://api.telegram.org/bot1273100614:AAHERAdteuCzmsDbkTyuvq2cD3wALG4hX4k/"
last_update_id = 0

# mqtt
mqtt_broker_url = "broker.hivemq.com"
topic = "navoznov/outside/temperature"

current_temperature = 999

def send_mess(chat, text):
    params = {'chat_id': chat, 'text': text}
    response = requests.post(bot_url + 'sendMessage', data=params)
    return response


def get_chat_id(update):
    return update['message']['chat']['id']


def get_update_id(update):
    return update['update_id']


timeout = 30
while True:
    topics = [topic]
    mqtt_message = subscribe.simple(topics, hostname=mqtt_broker_url, msg_count=1)
    # температура приходит в таком формате: b'11.9'. поэтому с начала строки отрезаем два символа и с конца один символ
    current_temperature = str(mqtt_message.payload)[2:-1]

    # temperature_last_update_datetime = datetime.datetime.utcnow()

    params = {'timeout': timeout, 'offset': last_update_id + 1 }
    response = requests.get(bot_url + 'getUpdates', params)
    responseJson = response.json()
    results = responseJson['result']
    if len(results) > 0:
        last_update_id = max(map(get_update_id, results))
        chatIds = list(set(map(get_chat_id, results)))

        for chat_id in chatIds:
            send_mess(chat_id, 'Сейчас в поселке ' + current_temperature + ' градусов')
    
    time.sleep(50/1000)