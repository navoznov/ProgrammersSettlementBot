#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import time
import datetime

# telegram bot settings
bot_url = "https://api.telegram.org/bot1356767647:AAGH3gR8YqxsFmzrbeIWhmlCsRLHlif5c_k/"
last_update_id = 0

# mqtt
mqtt_broker_url = "broker.hivemq.com"
topic = "navoznov/outside/temperature"
temperature_update_interval_sec = 10
temperature_update_interval = datetime.timedelta(seconds=temperature_update_interval_sec)
temperature_last_update_datetime = datetime.datetime.now() - datetime.timedelta(days=1)

print(temperature_last_update_datetime)

current_temperature = 999

def send_mess(chat, text):
    params = {'chat_id': chat, 'text': text}
    response = requests.post(bot_url + 'sendMessage', data=params)
    return response


def get_chat_id(update):
    return update['message']['chat']['id']


def get_update_id(update):
    return update['update_id']

while True:
    now = datetime.datetime.utcnow()
    if now > temperature_last_update_datetime + temperature_update_interval:
        topics = [topic]
        print("MQTT: Send request")
        mqtt_message = subscribe.simple(topics, hostname=mqtt_broker_url, msg_count=1)
        # payload format is b'11.9'
        current_temperature = str(mqtt_message.payload)[2:-1]
        print("MQTT: Response = " + current_temperature)
        temperature_last_update_datetime = now

    params = {'timeout': 30, 'offset': last_update_id + 1 }
    print("Telegram: Send request")
    response = requests.get(bot_url + 'getUpdates', params)
    responseJson = response.json()    
    results = responseJson['result']
    print("Telegram: " + str(len(results)) + " results")
    if len(results) > 0:
        last_update_id = max(map(get_update_id, results))
        chatIds = list(set(map(get_chat_id, results)))

        for chat_id in chatIds:
            send_mess(chat_id, 'Сейчас в поселке ' + current_temperature + ' градусов')
    
    time.sleep(10/1000)