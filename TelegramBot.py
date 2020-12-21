#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import re
import datetime


class TelegramBot:
    # telegram bot settings
    last_update_id = 0
    start_message = '{} Я могу сообщать текущую температуру в Поселке Программистов в ответ на любое сообщение.'
    schedule_question_message = 'Во сколько вам присылать температуру? Ответить можно в таком формате: 9:11, 913, 15-34, 09:20, 0745 и тп'
    schedule_success_message = 'Отлично! Теперь вы будете получать сообщения каждый день в {}:{}'
    schedule_parsing_fail_message = 'Не понятно. :( Во сколько вам присылать температуру? Ответьте в одном из форматов: 9:11, 913, 15-34, 09:20, 0745 и тп'
    schedule_fail_message = 'Не удалось запланировать. Произошла какая-то ошибка! Но это не точно.'

    def __init__(self, bot_id, bot_api_key, temperature_provider, scheduler):
        self.__temperature_provider = temperature_provider
        self.__scheduler = scheduler
        self.__subscribers_last_notification_time = datetime.datetime.now().time()
        self.__schedule_awaiting_chat_ids = set()
        self.__bot_url = "https://api.telegram.org/bot{}:{}/".format(bot_id, bot_api_key)

    def __send_message(self, chat, text):
        params = {'chat_id': chat, 'text': text}
        response = requests.post(self.__bot_url + 'sendMessage', data=params)
        return response

    def __broadcast(self, chat_ids, message):
        for chat_id in chat_ids:
            self.__send_message(chat_id, message)

    def __get_updates(self):
        offset = self.last_update_id + 1
        params = {'timeout': 30, 'offset': offset}
        response = requests.get(self.__bot_url + 'getUpdates', params)
        response_json = response.json()

        updates = response_json['result']
        if len(updates) > 0:
            update_ids = [update['update_id'] for update in updates]
            self.last_update_id = max(update_ids)
        return updates

    def __parseTime(self, timeStr):
        regex = r'^(?P<hours>\d{1,2}?)[:\-/\\]?(?P<minutes>\d{1,2})$'
        result = re.search(regex, timeStr)
        if result == None:
            return (False, None)
        hours = result.group('hours')
        minutes = result.group('minutes')
        return (True, (int(hours), int(minutes)))

    def __get_actual_temperature_message_text(self):
        temperature = self.__temperature_provider.getActualTemperature()
        temperature_message = 'Сейчас в поселке ' + \
            str(temperature) + ' градусов'
        return temperature_message

    def processUpdates(self):
        temperature_message = self.__get_actual_temperature_message_text()
        notified_chat_ids = set()

        updates = self.__get_updates()
        for update in updates:
            message = update['message']
            chat_id = message['chat']['id']

            # Список команд с описаниями для BotFather
            # subscribe - Запланировать уведомление
            # list - Вывести список запланированных уведомлений
            # clear - Удалить все запланированные уведомления

            text = message['text']
            if text == '/start':
                # TODO: поля username может не быть
                name = message['from'].get('username', None)
                if name == None:
                    name = message['from'].get('first_name', None)
                welcomeText = 'Привет!' if name == None else 'Привет, {}!'.format(name)
                reply = self.start_message.format(welcomeText)
                self.__send_message(chat_id, reply)
            elif text == '/schedule' or text == '/plan' or text == '/subscribe':
                self.__send_message(chat_id,  self.schedule_question_message)
                self.__schedule_awaiting_chat_ids.add(chat_id)
            elif chat_id in self.__schedule_awaiting_chat_ids:
                is_success, time = self.__parseTime(text)
                if is_success:
                    hours, minutes = time
                    if self.__scheduler.schedule(chat_id, hours, minutes):
                        reply = self.schedule_success_message.format(
                            str(hours).zfill(2), str(minutes).zfill(2))
                        self.__send_message(chat_id, reply)
                        self.__schedule_awaiting_chat_ids.remove(chat_id)
                    else:
                        self.__send_message(
                            chat_id, self.schedule_fail_message)
                else:
                    self.__send_message(
                        chat_id, self.schedule_parsing_fail_message)
            elif text == '/list':
                times = self.__scheduler.get_timetable_by_chat_id(chat_id)
                timetable = sorted([str(t.hour).zfill(2) + ':' + str(t.minute).zfill(2) for t in times])
                timesStr = ', '.join(timetable)
                reply = 'У вас нет подписок на увдомления о температуре.'
                if len(times) > 0:
                    reply = 'Вы узнаете температуру ежедневно в {}.'.format(timesStr)
                self.__send_message(chat_id, reply)
            elif text == '/clear':
                self.__scheduler.clear_subscriptions(chat_id)
            elif not chat_id in notified_chat_ids:
                self.__send_message(chat_id, temperature_message)
                notified_chat_ids.add(chat_id)

    def processSubscribers(self):
        now = datetime.datetime.now().time()
        chat_ids = self.__scheduler.get_chat_ids_by_time_range(self.__subscribers_last_notification_time, now)
        temperature_message = self.__get_actual_temperature_message_text()
        self.__broadcast(chat_ids, temperature_message)
        self.__subscribers_last_notification_time = now
        return True
