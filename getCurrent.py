#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
from MqttTemperatureProvider import MqttTemperatureProvider

mqtt_broker_url = "broker.hivemq.com"
mqtt_topic = "navoznov/outside/temperature"
mqttTemperatureProvider = MqttTemperatureProvider(mqtt_broker_url, mqtt_topic)
temperature = mqttTemperatureProvider.getActualTemperature()
print(temperature)
