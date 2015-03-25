# -*- coding: utf-8 -*-
from scraper.spiders.coffeescraper import CoffeeSpider

class CounterCultureSpider(CoffeeSpider):
    name = 'counterculture'

    def get_config(self):
        return {
            'name': 'counterculture',
            'allowed_domains': ['counterculturecoffee.com'],
            'start_urls': ['https://counterculturecoffee.com/store/coffee'],
            'link_rules': [
                {
                    'allow': "/store/coffee\?p=\d+"
                }
            ],
            'page_rules': [
                {
                    'allow': "/store/coffee/*",
                    'restrict_xpaths': '//h2[@class="product-name"]'
                }
            ],
            'content_rules': [
                {
                    'xpath':'//div[@class="product-name"]/h1/text()',
                    'field': {
                        'name': 'name'
                    },
                    'split': {
                        'split_character': [u' – ', u' - '],
                        'content_index': 0
                    }
                }, {
                    'xpath': '//*[@class="product-short-description"]/text()',
                    'field': {
                        'name': 'description'
                    }
                }, {
                    'xpath': '//div[@id="accordion"]/h3[text()="Notes"]/following-sibling::*[1]',
                    'field': {
                        'name': 'varietal',
                        'key': 'Variety:'
                    },
                    'nested_xpath': {
                        'key_xpath': 'b[text()="Variety:"]/text()',
                        'content_xpath': 'b[text()="Variety:"]/parent::*/text()[2]'
                    }
                }, {
                    'xpath': '//div[@id="accordion"]/h3[text()="Place"]/following-sibling::*[1]//strong/text()',
                    'field': {
                        'name': 'origin'
                    }
                }, {
                    'xpath': '/',
                    'field': {
                        'name': 'roaster'
                    },
                    'constant': 'Counter Culture Coffee'
                }
            ]
        }
