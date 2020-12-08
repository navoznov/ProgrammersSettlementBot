#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from TelegramBot import TelegramBot
from MqttTemperatureProvider import MqttTemperatureProvider


telegramBot = TelegramBot()
mqttTemperatureProvider = MqttTemperatureProvider()

while True:
    temperature = mqttTemperatureProvider.getActualTemperature()

    telegramBot.broadcastTemperature(temperature)

    time.sleep(1)
