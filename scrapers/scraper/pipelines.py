# -*- coding: utf-8 -*-

import rethinkdb as r
from pymongo import MongoClient
import os
import hashlib
from scrapy.exceptions import DropItem
import unicodedata
import urllib

class MongoPipeline(object):

    coffee_table = 'coffees'

    def __init__(self):
        self.client = MongoClient('localhost', 3001)
        self.db = self.client.meteor
        #self.db = self.client.brewbetter_meteor_com

    def process_item(self, item, spider):
        m = hashlib.sha1();
        m.update(item['name'].encode('ascii', 'ignore'))
        m.update(item['roaster'].encode('ascii', 'ignore'))
        item['_id'] = m.hexdigest()
        item['verified'] = True
        coffees = self.db.coffees
        result = coffees.insert(item.__dict__['_values'])
        return item

class RethinkPipeline(object):

    db_config = dict(
        host='localhost',
        port='28015',
        db='CoffeeApp'
    )

    coffee_table = 'coffees'

    def __init__(self):
        if 'RETHINK_AUTH_KEY' in os.environ:
            self.db_config['auth_key'] = os.environ['RETHINK_AUTH_KEY']
        if 'RETHINK_HOST' in os.environ:
            self.db_config['host'] = os.environ['RETHINK_HOST']

    def process_item(self, item, spider):
        m = hashlib.sha1();
        m.update(item['name'].encode('ascii', 'ignore'))
        m.update(item['roaster'].encode('ascii', 'ignore'))
        item['_id'] = m.hexdigest()
        item['verified'] = True
        conn = r.connect(**self.db_config)
        value = item.__dict__['_values']
        value['id'] = value['_id']
        del value['_id']
        result = r.table(self.coffee_table).insert(item.__dict__['_values']).run(conn)
        if result['inserted'] == 0:
            raise DropItem("Coffee Already Inserted")
        conn.close()
        return item
