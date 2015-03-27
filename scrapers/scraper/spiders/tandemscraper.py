# -*- coding: utf-8 -*-
from scraper.spiders.coffeescraper import CoffeeSpider

class TandemSpider(CoffeeSpider):
    name = 'tandem'

    def get_config(self):
        return {
            'name': 'tandem',
            'allowed_domains': ['tandemcoffee.com'],
            'start_urls': ['http://www.tandemcoffee.com/category/coffees'],
            'page_rules': [
                {
                    'allow': "/product/*"
                }
            ],
            'content_rules': [
                {
                    'xpath':'//h2[@class="entry_title"]/span/text()',
                    'field': {
                        'name': 'name'
                    }
                }, {
                    'xpath': '//div[@class="info"]/p',
                    'field': [{
                        'name': 'description',
                        'key': 'We Think:'
                    }, {
                        'name': 'varietal',
                        'key': 'Varietals:'
                    }, {
                        'name': 'elevation',
                        'key': 'Elevation:'
                    }, {
                        'name': 'producer',
                        'key': 'Sourced by:'
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
                    'constant': 'Tandem Coffee'
                }
            ]

        }
