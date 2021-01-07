#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import random
import datetime
import logging


class MqttTemperatureProvider:
    def __init__(self, mqtt_broker_url, mqtt_topic, mqtt_client_id = None, mqtt_username = None, mqtt_password = None):
        self.__mqtt_broker_url = mqtt_broker_url
        self.__mqtt_topic = mqtt_topic
        DEFAULT_CLIENT_ID = 'temperature_bot'
        self.__mqtt_client_id = DEFAULT_CLIENT_ID if mqtt_client_id == None else mqtt_client_id
        self.__mqtt_username = mqtt_username
        self.__mqtt_password = mqtt_password
        self.__temperature = -273.0
        TEMPERATURE_UPDATE_INTERVAL_SEC = 10
        self.__temperature_update_interval = datetime.timedelta(seconds=TEMPERATURE_UPDATE_INTERVAL_SEC)
        self.__temperature_last_update_datetime = datetime.datetime.now() - datetime.timedelta(days=1)

    def getActualTemperature(self):
        now = datetime.datetime.now()
        if now > self.__temperature_last_update_datetime + self.__temperature_update_interval:
            topics = [self.__mqtt_topic]
            try:
                auth = self.__get_mqtt_auth()
                mqtt_message = subscribe.simple(
                    topics, hostname=self.__mqtt_broker_url, msg_count=1, auth=auth, client_id=self.__mqtt_client_id)
                # payload format is "b'-11.9'"
                self.__temperature = str(mqtt_message.payload)[2:-1]
            except Exception as ex:
                logging.exception('Ошибка получения температуры')

        return self.__temperature

    def get_temperature_last_update_datetime(self):
        return self.__temperature_last_update_datetime

    def __get_mqtt_auth(self):
        if self.__mqtt_username == None:
            return None

        return {'username': self.__username, 'password': self.__mqtt_password}
