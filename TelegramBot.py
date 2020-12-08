#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json


class TelegramBot:
    # telegram bot settings
    bot_url = "https://api.telegram.org/bot1356767647:AAGH3gR8YqxsFmzrbeIWhmlCsRLHlif5c_k/"
    last_update_id = 0

    def send_mess(self, chat, text):
        params = {'chat_id': chat, 'text': text}
        response = requests.post(self.bot_url + 'sendMessage', data=params)
        return response

    def getChatId(self, update):
        return update['message']['chat']['id']

    def getUpdates(self):
        offset = self.last_update_id + 1
        params = {'timeout': 30, 'offset': offset}
        response = requests.get(self.bot_url + 'getUpdates', params)
        responseJson = response.json()

        updates = responseJson['result']
        if len(updates) > 0:
            updateIds = [update['update_id'] for update in updates]
            self.last_update_id = max(updateIds)
        return updates

    def getChatIds(self, updates):
        chatIds = list(set([self.getChatId(update) for update in updates]))
        return chatIds

    def broadcastTemperature(self, temperature):
        updates = self.getUpdates()
        chatIds = self.getChatIds(updates)
        message = 'Сейчас в поселке ' + str(temperature) + ' градусов'
        for chat_id in chatIds:
            self.send_mess(chat_id, message)
