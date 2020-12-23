#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getopt
import secret_data
import time
import datetime
from DataBaseProvider import DataBaseProvider
from DataBaseScheduler import DataBaseScheduler
from TelegramBot import TelegramBot
from MqttTemperatureProvider import MqttTemperatureProvider
from MemoryScheduler import MemoryScheduler
from StatisticsService import StatisticsService


def get_options():
    bot_id = secret_data.bot_id
    bot_api_key = secret_data.bot_api_key
    mqtt_broker_url = secret_data.mqtt_broker_url
    mqtt_topic = secret_data.mqtt_topic

    try:
        longopts = ["bot-id=", "bot_key=", "mqtt-server=", "mqtt-topic=", "db-filename="]
        argv = sys.argv[1:]
        opts, args = getopt.getopt(argv, "i:k:u:t:d", longopts)
        options = {}
        for a, v in opts:
            aa = a.replace('--', '')
            options[aa] = v
    except getopt.GetoptError:
        sys.exit(2)

    return options


options = get_options()

bot_id = options['bot-id']
bot_api_key = options['bot_key']
mqtt_broker_url = options['mqtt-server']
mqtt_topic = options['mqtt-topic']
db_filename = options['db-filename']

dataBaseProvider = DataBaseProvider(db_filename)
scheduler = DataBaseScheduler(dataBaseProvider)
mqttTemperatureProvider = MqttTemperatureProvider(mqtt_broker_url, mqtt_topic)
telegramBot = TelegramBot(bot_id, bot_api_key, mqttTemperatureProvider, scheduler)
statisticsService = StatisticsService(mqttTemperatureProvider)

TICK_INTERVAL_SEC = 5
while True:
    telegramBot.processUpdates()
    statisticsService.tick()
    telegramBot.processSubscribers()
    time.sleep(TICK_INTERVAL_SEC)
