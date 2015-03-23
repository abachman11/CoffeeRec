import itertools
from scrapy.contrib.spiders import Rule
from scraper.items import Coffee
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import parsefunctions as Generators
class ParseUtils:

    def __init__(self, class_name, config, item_callback):
        self.config = config
        self.callback = item_callback
        self._parse_config(class_name)

    def process_response(self, response):
        ''' process_response - evaluates a page based on the response from
            a downloaded web page based on the rules given.
            returns a list of tuples with each entry continaing the field name
            and the content that was parsed from the page
        '''
        response = [
            self._evaluate_rule(response, rule) for rule in self.content_rules
        ]

        # Flatten the list using method from StackOverflow
        # http://stackoverflow.com/questions/406121/flattening-a-shallow-list-in-python
        response_chain = itertools.chain.from_iterable(response)
        return list(itertoos.chain(response_chain))

    def _parse_config(self, class_name):
        ''' parse_config
            params: self
                    class_name - The Class that is being used as the base scraper
            return: void
        '''
        class_name.name = self.config['name']
        class_name.allowed_domains = self.config['allowed_domains']
        class_name.rules = self._parse_following_rules()
        class_name.mConfig = config
        self.content_rules = self._parse_content_rules()

    def _parse_following_rules(self):
        ''' _parse_following_rules
            Helper method that parses the rules for which pages will be parsed
            for links and which pages will be parsed to extract objects
        '''
        link_rules = self.config['list_rules']
        page_rules = self.config['coffee_rules']
        for rule in coffee_rules:
            rule['callback'] = self.callback
        return [ Rule(SgmlLinkExtractor(**rule)) for rule in list_rules.extend(rule) ]

    def _parse_content_rules(self):
        content_rules = [ self._parse_content_rule(rule) for rule in self.config['content_rules'] ]

    def _parse_content_rule(self, rule):
        ''' _parse_content_rule
            params:
                rule - rule for parsing content provided by subclass of web crawler
            returns - a rule entry containing the necessary information to process
                a selector of the given type using the function stored in the parse
                attribute function
        '''
        key_dict = dict()
        for field in rule['field']:
            if not 'key' in field:
                field['key'] = field['name']
            key_dict[field['key']] = field['name']
        result = dict(key_dict=key_dict, xpath=rule['xpath'])
        if 'parse_function' in rule:
            result['parse_function'] = rule['parse_function']
        elif 'split' in rule:
            result['parse_function'] = Generators.split_scrape_generator(
                rule['split']['split_character'],
                rule['split']['content_index'],
                key_index = rule['split'].setdefault('key_index', -1),
                field = rule['split'].setdefault('field', '')
            )
        elif 'nested_xpath' in rule:
            result['parse_function'] = Generators.nested_xpath_scrape_generator(
                result['nested_xpath']['content_xpath'],
                result['nested_xpath']['key_xpath']
            )
        else:
            if len(rule['field']) != 1 and not isinstance(rule['field'], basestring):
                raise Exception('Invalid Rule', rule)
            elif 'name' in rule['field']:
                name = rule['field']['name']
            else:
                name = rule['field']
            result['parse_function'] = Generators.clean_scrape_generator(
                name
            )

    def _process_rule(response, rule):
        ''' _process_rule takes a downloaded page and a parsed rule (with fields xpath, key_dict
            and parse_function) and returns a list of dictionary with the field
            name and the content that was parsed for that field
        '''
        selector = reponse.xpath(rule['xpath'])
        result = rule['parse_function'](selctor)
        if isinstance(result, list):
            return result
        else:
            return list(result)
