#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime


class MemoryScheduler:

    def __init__(self):
        self.__timeTable = {}

    def __get_timetable_key(self, hours, minutes):
        key = datetime.time(hours, minutes)
        return key

    def __convertKeyToTime(self, key):
        return key

    def schedule(self, chat_id, hours, minutes):
        key = self.__get_timetable_key(hours, minutes)
        self.__timeTable[key] = self.__timeTable.get(key, set())
        self.__timeTable[key].add(chat_id)
        return True

    def get_timetable_by_chat_id(self, chat_id):
        return [self.__convertKeyToTime(t) for t, chat_ids in self.__timeTable.items() if chat_id in chat_ids]

    def __check_time_in_range(self, time, minTime, maxTime):
        return minTime < maxTime and minTime < time <= maxTime or minTime > maxTime and (time > minTime or time <= maxTime)

    def get_chat_ids_by_time_range(self, minTime, maxTime):
        result = set()
        result.update(*[chat_ids for key, chat_ids in self.__timeTable.items() if self.__check_time_in_range(key, minTime, maxTime)])
        return result

    def clear_subscriptions(self, chat_id):
        for _, item in self.__timeTable.items():
            item.remove(chat_id)