#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
from TelegramBot import TelegramBot
from MqttTemperatureProvider import MqttTemperatureProvider
from Scheduler import Scheduler

scheduler = Scheduler()
mqttTemperatureProvider = MqttTemperatureProvider()
telegramBot = TelegramBot(mqttTemperatureProvider, scheduler)

now = datetime.datetime.now()
last_hours, last_minutes = now.hour, now.minute
while True:
    telegramBot.processUpdates()


    # todo: реализовать проверку запланированных уведомлений
    now = datetime.datetime.now()
    hours, minutes = now.hour, now.minute
    # ?????? что со временем?
    if (last_hours, last_minutes) != (hours, minutes):
        chat_ids = scheduler.get_chat_ids_by_time(hours, minutes)
        telegramBot.broadcastTemperature()


    time.sleep(1)
