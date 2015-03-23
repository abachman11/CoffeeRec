from scrapy.contrib.spiders import Rule
from scraper.items import Coffee
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
class ParseUtils:

    def __init__(self, class_name, config, item_callback):
        self.config = config
        self.callback = item_callback

    def parse_config(self, current):
        ''' parse_config
            params: self
                    current - The Class that is being used as the base scraper
            return: void
        '''
        current.name = self.config['name']
        current.allowed_domains = self.config['allowed_domains']
        current.rules = self.parse_rules
        current.mConfig = config

    def _parse_rules(self):
        ''' _parse_rules
            Helper method that parses the rules for which pages will be parsed
            for links and which pages will be parsed to extract objects
        '''
        link_rules = self.config['list_rules']
        page_rules = self.config['coffee_rules']
        for rule in coffee_rules:
            rule['callback'] = self.callback
        return [ Rule(SgmlLinkExtractor(**rule)) for rule in list_rules.extend(rule) ]

    def _parse_content_rules(self):
        content_rules = self.config['content_rules']

    def _parse_content_rule(self, rule):
        parse_function
        for field in rule['field']:
            if not 'key' in field:
                field['key'] = field['name']
