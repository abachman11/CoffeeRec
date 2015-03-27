# -*- coding: utf-8 -*-
from scraper.spiders.coffeescraper import CoffeeSpider

class IntelligentsiaSpider(CoffeeSpider):
    name = 'intelligentsia'

    def get_config(self):
        return {
            'name': 'intelligentsia',
            'allowed_domains': ['intelligentsiacoffee.com'],
            'start_urls': ['http://www.intelligentsiacoffee.com/products/coffee'],
            'page_rules': [
                {
                    'allow': "/product/coffee/*"
                }
            ],
            'content_rules': [
                {
                    'xpath':'//p[@class="coffeeDetailTitle"]/em/text()',
                    'field': {
                        'name': 'name'
                    }
                }, {
                    'xpath': '//div[@class="product-body"]/p/text()',
                    'field': {
                        'name': 'description'
                    }
                }, {
                    'xpath': '//ul[@id="coffeeStats"]/li',
                    'field': [{
                        'name': 'varietal',
                        'key': 'Cultivar'
                    }, {
                        'name': 'producer',
                        'key': 'Producer'
                    }, {
                        'name': 'elevation',
                        'key': 'Elevation'
                    }, {
                        'name': 'origin',
                        'key': 'Country'
                    }],
                    'nested_xpath': {
                        'key_xpath': 'b/text()',
                        'content_xpath': 'text()'
                    }
                }, {
                    'xpath': '/',
                    'field': {
                        'name': 'roaster'
                    },
                    'constant': 'Intelligentsia Coffee'
                }
            ]
        }
