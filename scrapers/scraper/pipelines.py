# -*- coding: utf-8 -*-

import rethinkdb as r
from pymongo import MongoClient
import os
import hashlib
from scrapy.exceptions import DropItem
import unicodedata
import urllib

class CoffeePipeline(object):

    coffee_table = 'coffees'

    def __init__(self):
        self.client = MongoClient('localhost', 3001)
        self.db = self.client.meteor
        #self.db = self.client.brewbetter_meteor_com

    def process_item(self, item, spider):
        m = hashlib.sha1();
        m.update(item['name'].encode('ascii', 'ignore'))
        m.update(item['roaster']['name'].encode('ascii', 'ignore'))
        item['_id'] = m.hexdigest()
        item['verified'] = True
        coffees = self.db.coffees
        result = coffees.insert(item.__dict__['_values'])
        return item
