#!/usr/bin/env python
# -*- coding: utf-8 -*-

import secret_data
import time
import datetime
from TelegramBot import TelegramBot
from MqttTemperatureProvider import MqttTemperatureProvider
from Scheduler import Scheduler
from StatisticsService import StatisticsService

scheduler = Scheduler()
mqttTemperatureProvider = MqttTemperatureProvider(secret_data.mqtt_broker_url, secret_data.mqtt_topic)
telegramBot = TelegramBot(secret_data.bot_id, secret_data.bot_api_key, mqttTemperatureProvider, scheduler)
statisticsService = StatisticsService(mqttTemperatureProvider)

now = datetime.datetime.now()
last_hours, last_minutes = now.hour, now.minute

while True:
    telegramBot.processUpdates()
    statisticsService.tick()
    telegramBot.processSubscribers()
    time.sleep(20)
