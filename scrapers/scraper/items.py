# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Coffee(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    name = scrapy.Field()
    roaster = scrapy.Field()
    description = scrapy.Field()
    origin = scrapy.Field();
    tasting_notes = scrapy.Field();
    varietal = scrapy.Field();
    elevation = scrapy.Field();
    producer = scrapy.Field();
    verified = scrapy.Field();
