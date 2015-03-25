# -*- coding: utf-8 -*-
from scraper.spiders.coffeescraper import CoffeeSpider

class BluebottleSpider(CoffeeSpider):
    name = 'bluebottle'

    def get_config(self):
        return {
            'name': 'bluebottle',
            'allowed_domains': ['bluebottlecoffee.com'],
            'start_urls': ['https://bluebottlecoffee.com/store/coffee'],
            'page_rules': [
                {
                    'allow': "/store/*",
                    'restrict_xpaths': '//*[@class="span3 product"]/child::*'
                }
            ],
            'content_rules': [
                {
                    'xpath':'//h2/text()',
                    'field': {
                        'name': 'name'
                    }
                }, {
                    'xpath': '//*[@class="long-overview hidden"]/text()',
                    'field': {
                        'name': 'description'
                    }
                }, {
                    'xpath': '/',
                    'field': {
                        'name': 'roaster'
                    },
                    'constant': 'Blue Bottle Coffee'
                }, {
                    'xpath': '//h2/following-sibling::*/text()',
                    'field': {
                        'name': 'tasting_notes'
                    }
                }
            ]
        }
