# -*- coding: utf-8 -*-
from anykeystore import create_store
import sqlite3

class DataStorage(object):

    def __init__(self, db_file):
        super(DataStorage, self).__init__()
        self.db_file = db_file
        self.store = create_store('sqla', url=db_file)

    def store_dict(self, key, value):
        self.store.store(key, value)

    def retrieve_dict(self, key):
        return self.store.retrieve(key)