#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import re


class TelegramBot:
    # telegram bot settings
    bot_url = "https://api.telegram.org/bot1356767647:AAGH3gR8YqxsFmzrbeIWhmlCsRLHlif5c_k/"
    last_update_id = 0
    start_message = 'Приветствую тебя, {}! Я могу сообщать текущую температуру в Поселке Программистов в ответ на любое сообщение.'
    schedule_question_message = 'Во сколько вам присылать температуру? Ответить можно в таком формате: 9:11, 913, 15-34, 09:20, 0745 и тп'
    schedule_success_message = 'Отлично! Теперь вы будете получать сообщения каждый день в {}:{}'
    schedule_parsing_fail_message = 'Не понятно. :( Во сколько вам присылать температуру? Ответьте в одном из форматов: 9:11, 913, 15-34, 09:20, 0745 и тп'
    schedule_fail_message = 'Не удалось запланировать. Произошла какая-то ошибка! Но это не точно.'
    schedule_awaiting_chat_ids = set()

    def __init__(self, temperature_provider, scheduler):
        self.__temperature_provider = temperature_provider
        self.__scheduler = scheduler

    def __send_message(self, chat, text):
        params = {'chat_id': chat, 'text': text}
        response = requests.post(self.bot_url + 'sendMessage', data=params)
        return response

    def __get_updates(self):
        offset = self.last_update_id + 1
        params = {'timeout': 30, 'offset': offset}
        response = requests.get(self.bot_url + 'getUpdates', params)
        response_json = response.json()

        updates = response_json['result']
        if len(updates) > 0:
            update_ids = [update['update_id'] for update in updates]
            self.last_update_id = max(update_ids)
        return updates

    def __parseTime(self, timeStr):
        regex = r'(?P<hours>\d{1,2}?)[:\-/\\]?(?P<minutes>\d{1,2})'
        result = re.search(regex, timeStr)
        if result == None:
            return (False, None)
        hours = result.group('hours')
        minutes = result.group('minutes')
        return (True, (int(hours), int(minutes)))

    def __get_actual_temperature_message_text(self):
        temperature = self.__temperature_provider.getActualTemperature()
        temperature_message = 'Сейчас в поселке ' + str(temperature) + ' градусов'
        return temperature_message

    def processUpdates(self):
        temperature_message = self.__get_actual_temperature_message_text()
        notified_chat_ids = set()

        updates = self.__get_updates()
        for update in updates:
            message = update['message']
            chat_id = message['chat']['id']

            text = message['text']
            if text == '/start':
                username = message['from']['username']
                reply = self.start_message.format('@' + username)
                self.__send_message(chat_id, reply)
            elif text == '/schedule' or text == '/plan':
                self.__send_message(chat_id,  self.schedule_question_message)
                self.schedule_awaiting_chat_ids.add(chat_id)
            elif chat_id in self.schedule_awaiting_chat_ids:
                is_success, time = self.__parseTime(text)
                if is_success:
                    hours, minutes = time
                    if self.__scheduler.schedule(chat_id, hours, minutes):
                        reply = self.schedule_success_message.format(str(hours).zfill(2), str(minutes).zfill(2))
                        self.__send_message(chat_id, reply)
                        self.schedule_awaiting_chat_ids.remove(chat_id)
                    else:
                        self.__send_message(chat_id, self.schedule_fail_message)
                else:
                    self.__send_message(chat_id, self.schedule_parsing_fail_message)
            elif text == '/list':
                timetable = sorted([str(t.hour).zfill(2) + ':' + str(t.minute).zfill(2) for t in self.__scheduler.get_timetable_by_chat_id(chat_id)])
                reply = 'Вы узнаете температуру ежедневно в: ' + ', '.join(timetable) + '.'
                self.__send_message(chat_id, reply)
            elif not chat_id in notified_chat_ids:
                self.__send_message(chat_id, temperature_message)
                notified_chat_ids.add(chat_id)

    def broadcastTemperature(self, chat_ids):
        temperature_message = self.__get_actual_temperature_message_text()
        for chat_id in chat_ids:
            self.__send_message(chat_id, temperature_message)

