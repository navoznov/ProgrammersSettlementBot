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
import logging
from logging.handlers import TimedRotatingFileHandler

def get_options():
    bot_id = secret_data.bot_id
    bot_api_key = secret_data.bot_api_key
    mqtt_broker_url = secret_data.mqtt_broker_url
    mqtt_topic = secret_data.mqtt_topic

    try:
        longopts = ["bot-id=", "bot_key=", "mqtt-server=", "mqtt-topic=", "db-filename=", "use-subscriptions="]
        argv = sys.argv[1:]
        opts, args = getopt.getopt(argv, "i:k:u:t:d:s", longopts)
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
should_use_subscriptions = "use-subscriptions" in options and options['use-subscriptions'] == 'true'

dataBaseProvider = DataBaseProvider(db_filename)
scheduler = DataBaseScheduler(dataBaseProvider)
mqttTemperatureProvider = MqttTemperatureProvider(mqtt_broker_url, mqtt_topic)
telegramBot = TelegramBot(bot_id, bot_api_key, should_use_subscriptions, mqttTemperatureProvider, scheduler)
statisticsService = StatisticsService(mqttTemperatureProvider)

LOG_FILE = 'error.log'
file_logger = TimedRotatingFileHandler('log')

TICK_INTERVAL_SEC = 5
while True:
    try:
        telegramBot.processUpdates()
        # statisticsService.tick()
        telegramBot.processSubscribers()
    except Exception as e:
        file_logger.error()

    time.sleep(TICK_INTERVAL_SEC)