#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3


class DataBaseProvider:

    # Схема таблицы подписок
    # CREATE TABLE Subscriptions (Id integer PRIMARY KEY AUTOINCREMENT NOT NULL, ChatId integer, Time text, Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL)

    def __init__(self, db_filename):
        self.__filename = db_filename

    def get_all_subscriptions(self):
        try:
            connection = sqlite3.connect(self.__filename)
            sql = 'select Time, ChatId from Subscriptions'
            cursor = connection.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            connection.close()

    def get_subscriptions(self, chat_id):
        try:
            connection = sqlite3.connect(self.__filename)
            # sql injection possible
            sql = 'select Time from Subscriptions where ChatId=?'
            cursor = connection.cursor()
            cursor.execute(sql, [(chat_id)])
            return [r[0] for r in cursor.fetchall()]
        finally:
            connection.close()

    def add_subscription(self, chat_id, timeStr):
        try:
            connection = sqlite3.connect(self.__filename)
            # sql injection possible
            sql = 'insert into Subscriptions (ChatId, Time) values (?, ?)'.format(
                chat_id, timeStr)
            cursor = connection.cursor()
            cursor.execute(sql, (chat_id, timeStr))
            connection.commit()
            return True
        finally:
            connection.close()

    def delete_subscriptions(self, chat_id):
        try:
            connection = sqlite3.connect(self.__filename)
            # sql injection possible
            sql = 'delete from Subscriptions where ChatId=?'
            cursor = connection.cursor()
            cursor.execute(sql, [(chat_id)])
            connection.commit()
            return True
        finally:
            connection.close()
