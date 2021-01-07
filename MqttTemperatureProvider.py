#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import random
import datetime
import logging

class MqttTemperatureProvider:
    def __init__(self, mqtt_broker_url, mqtt_topic):
        self.__mqtt_broker_url = mqtt_broker_url
        self.__mqtt_topic = mqtt_topic
        self.__temperature = -273
        TEMPERATURE_UPDATE_INTERVAL_SEC = 10
        self.__temperature_update_interval = datetime.timedelta(seconds=TEMPERATURE_UPDATE_INTERVAL_SEC)
        self.__temperature_last_update_datetime = datetime.datetime.now() - datetime.timedelta(days=1)

    def getActualTemperature(self):
        now = datetime.datetime.now()
        if now > self.__temperature_last_update_datetime + self.__temperature_update_interval:
            topics = [self.__mqtt_topic]
            try:
                mqtt_message = subscribe.simple(topics, hostname=self.__mqtt_broker_url, msg_count=1)
                # payload format is "b'-11.9'"
                self.__temperature = str(mqtt_message.payload)[2:-1]
                self.__temperature_last_update_datetime = now
            except Exception as ex:
                logging.exception('Ошибка получения температуры')

        return self.__temperature

