#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getopt
import secret_data
import time
import datetime
from TelegramBot import TelegramBot
from MqttTemperatureProvider import MqttTemperatureProvider
from Scheduler import Scheduler
from StatisticsService import StatisticsService


def get_options():
    bot_id = secret_data.bot_id
    bot_api_key = secret_data.bot_api_key
    mqtt_broker_url = secret_data.mqtt_broker_url
    mqtt_topic = secret_data.mqtt_topic

    try:
        longopts = ["bot-id=", "bot_key=", "mqtt-server=", "mqtt-topic="]
        argv = sys.argv[1:]
        opts, args = getopt.getopt(argv, "i:k:u:t", longopts)
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

scheduler = Scheduler()
mqttTemperatureProvider = MqttTemperatureProvider(mqtt_broker_url, mqtt_topic)
telegramBot = TelegramBot(bot_id, bot_api_key, mqttTemperatureProvider, scheduler)
statisticsService = StatisticsService(mqttTemperatureProvider)

now = datetime.datetime.now()
last_hours, last_minutes = now.hour, now.minute

TICK_INTERVAL_SEC = 5
while True:
    telegramBot.processUpdates()
    statisticsService.tick()
    telegramBot.processSubscribers()
    time.sleep(TICK_INTERVAL_SEC)
