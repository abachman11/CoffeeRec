# -*- coding: utf-8 -*-
from scraper.spiders.coffeescraper import CoffeeSpider

class GeorgeHowellSpider(CoffeeSpider):
    name = 'georgehowell'

    def get_config(self):
        return {
            'name': 'georgehowell',
            'allowed_domains': ['store.georgehowellcoffee.com'],
            'start_urls': ['http://store.georgehowellcoffee.com/coffees/all/'],
            'page_rules': [
                {
                    'allow': "/coffees/*",
                }
            ],
            'content_rules': [
                {
                    'xpath':'//h1[@class="page-title"]/text()',
                    'field': {
                        'name': 'name'
                    }
                }, {
                    'xpath': '//div[@class="product-description"]/strong/text()',
                    'field': {
                        'name': 'description'
                    }
                }, {
                    'xpath': '//p[@class="tasting-notes"]/text()',
                    'field': {
                        'name': 'tasting_notes'
                    }
                }, {
                    'xpath': '//div[@id="cDetails"]/table/tr',
                    'field': [{
                        'name': 'origin',
                        'key': 'Country:'
                    }, {
                        'name': 'varietal',
                        'key': 'Varietals:'
                    }, {
                        'name': 'elevation',
                        'key': 'Altitude:'
                    }, {
                    }],
                    'nested_xpath': {
                        'key_xpath': 'td[@class="infoLabel"]/text()',
                        'content_xpath': 'td[@class="infoLabel"]/following-sibling::td[1]'
                    }
                }, {
                    'xpath': '/',
                    'field': {
                        'name': 'roaster'
                    },
                    'constant': 'George Howell Coffee'
                }
            ]
        }
