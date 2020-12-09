#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import datetime
from MqttTemperatureProvider import MqttTemperatureProvider


class StatisticsService:
    def __init__(self, mqtt_temperature_provider):
        self.__mqtt_temperature_provider = mqtt_temperature_provider
        print(1)

    def tick(self):
        actual_temperature = self.__mqtt_temperature_provider.getActualTemperature()
        # TODO: обработка температуры
        print(1)

    def saveTemperature(self, temperature):
        # TODO
        print(1)
