# -*- coding: utf-8 -*-

import rethinkdb as r
import os
import hashlib
from scrapy.exceptions import DropItem
import unicodedata

class CoffeePipeline(object):

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
        m.update(item['roaster']['name'].encode('ascii', 'ignore'))
        item['id'] = m.hexdigest()
        item['verified'] = True
        conn = r.connect(**self.db_config)
        result = r.table(self.coffee_table).insert(item.__dict__['_values']).run(conn)
        if result['inserted'] == 0:
            raise DropItem("Coffee Already Inserted")
        conn.close()
        return item
