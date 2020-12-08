#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import random
import datetime

class MqttTemperatureProvider:
    # mqtt
    mqtt_broker_url = "broker.hivemq.com"
    topic = "navoznov/outside/temperature"

    temperature_update_interval_sec = 10
    temperature_update_interval = datetime.timedelta(seconds=temperature_update_interval_sec)
    temperature_last_update_datetime = datetime.datetime.now() - datetime.timedelta(days=1)
    temperature = 999


    def getActualTemperature(self):
        now = datetime.datetime.now()
        if now > self.temperature_last_update_datetime + self.temperature_update_interval:
            self.temperature_last_update_datetime = now

            topics = [self.topic]
            mqtt_message = subscribe.simple(topics, hostname=self.mqtt_broker_url, msg_count=1)
            # payload format is "b'-11.9'"
            self.temperature = str(mqtt_message.payload)[2:-1]

        return self.temperature

