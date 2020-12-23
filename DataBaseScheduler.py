#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
from DataBaseProvider import DataBaseProvider


class DataBaseScheduler:

    def __init__(self, dataBaseProvider: DataBaseProvider):
        self.__dataBaseProvider = dataBaseProvider

    def __get_timetable_key(self, hours, minutes):
        key = '{}:{}'.format(str(hours).zfill(2), str(minutes).zfill(2))
        return key

    def __convertKeyToTime(self, key):
        hoursStr, minutesStr = key.split(':')
        hours, minutes = int(hoursStr), int(minutesStr)
        key = datetime.time(hours, minutes)
        return key

    def __check_time_in_range(self, time, minTime, maxTime):
        return minTime < maxTime and minTime < time <= maxTime or minTime > maxTime and (time > minTime or time <= maxTime)

    def schedule(self, chat_id, hours, minutes):
        timeStr = self.__get_timetable_key(hours, minutes)
        times = self.__dataBaseProvider.get_subscriptions(chat_id)
        if not timeStr in times:
            self.__dataBaseProvider.add_subscription(chat_id, timeStr)

        return True

    def get_timetable_by_chat_id(self, chat_id):
        times = self.__dataBaseProvider.get_subscriptions(chat_id)
        return [self.__convertKeyToTime(t) for t in times]

    def get_chat_ids_by_time_range(self, minTime, maxTime):
        minTime = '{}:{}'.format(minTime.hour, minTime.minute)
        maxTime = '{}:{}'.format(maxTime.hour, maxTime.minute)
        all_subscriptions = self.__dataBaseProvider.get_all_subscriptions()
        return set([chat_ids for key, chat_ids in all_subscriptions if self.__check_time_in_range(key, minTime, maxTime)])

    def clear_subscriptions(self, chat_id):
        self.__dataBaseProvider.delete_subscriptions(chat_id)
