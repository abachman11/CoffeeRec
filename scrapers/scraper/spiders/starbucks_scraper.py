# -*- coding: utf-8 -*-
from scraper.spiders.coffeescraper import CoffeeSpider
class StarbucksSpider(CoffeeSpider):
    name = 'starbucks'

    def get_config(self):
        return {
            'name': 'starbucks',
            'allowed_domains': ['store.starbucks.com'],
            'start_urls': ['http://store.starbucks.com/coffee/coffee,default,sc.html?start=1&sz=1000'],
            'page_rules': [
                {
                    'restrict_xpaths': '//*[@class="product_info"]'
                }
            ],
            'content_rules': [
                {
                    'xpath':'//h1[@class="pdp-prodname"]/text()',
                    'field': {
                        'name': 'name'
                    }
                }, {
                    'xpath': '//span[@class="pdp-label" and text()="Tasting Notes"]/following-sibling::*[@class="pdp-value"]/text()',
                    'field': {
                        'name': 'description'
                    }
                }, {
                    'xpath': '//span[@class="pdp-label" and text()="Region"]/following-sibling::*[@class="pdp-value amrdot"]/text()',
                    'field': {
                        'name': 'origin'
                    }
                }, {
                    'xpath': '/',
                    'field': {
                        'name': 'roaster'
                    },
                    'constant': 'Starbucks Coffee'
                }
            ]
        }
