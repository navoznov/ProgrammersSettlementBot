#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime


class Scheduler:

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

    def get_chat_ids_by_time(self, hours, minutes):
        key = self.__get_timetable_key(hours, minutes)
        return self.__timeTable.get(key, set())
