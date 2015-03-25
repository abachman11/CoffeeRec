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
        return list(itertools.chain(response_chain))

    def _parse_config(self, class_name):
        ''' parse_config
            params: self
                    class_name - The Class that is being used as the base scraper
            return: void
        '''
        class_name.name = self.config['name']
        class_name.allowed_domains = self.config['allowed_domains']
        class_name.start_urls = self.config['start_urls']
        class_name.rules = self._parse_following_rules()
        class_name.mConfig = self.config
        self.content_rules = self._parse_content_rules()

    def _parse_following_rules(self):
        ''' _parse_following_rules
            Helper method that parses the rules for which pages will be parsed
            for links and which pages will be parsed to extract objects
        '''
        if 'link_rules' in self.config:
            link_rules = self.config['link_rules']
        else:
            link_rules = list()
        if 'page_rules' in self.config:
            page_rules = self.config['page_rules']
        else:
            page_rules = ()
        link_rules = [
            Rule(SgmlLinkExtractor(**rule)) for rule in link_rules
        ]
        link_rules.extend([
            Rule(SgmlLinkExtractor(**rule), callback=self.callback) for rule in page_rules
        ])
        return tuple(link_rules)

    def _parse_content_rules(self):
        return [ self._parse_content_rule(rule) for rule in self.config['content_rules'] ]

    def _parse_content_rule(self, rule):
        ''' _parse_content_rule
            params:
                rule - rule for parsing content provided by subclass of web crawler
            returns - a rule entry containing the necessary information to process
                a selector of the given type using the function stored in the parse
                attribute function
        '''
        key_dict = dict()
        if isinstance(rule['field'], basestring):
            key_dict[rule['field']] = rule['field']
        elif type(rule['field']) is dict:
            if not 'key' in rule['field']:
                rule['field']['key'] = rule['field']['name']
            key_dict[rule['field']['key']] = rule['field']['name']
        else:
            for field in rule['field']:
                if not 'key' in field:
                    field['key'] = field['name']
                key_dict[field['key']] = field['name']
        result = dict(key_dict=key_dict, xpath=rule['xpath'])
        if 'parse_function' in rule:
            result['parse_function'] = rule['parse_function']
        elif 'split' in rule:
            rule['split'].setdefault('key_index', -1),
            result['parse_function'] = Generators.split_scrape_generator(
                rule['split']['split_character'],
                rule['split']['content_index'],
                key_index = rule['split']['key_index'],
                field = self._get_single_field(rule)
            )
        elif 'nested_xpath' in rule:
            result['parse_function'] = Generators.nested_xpath_scrape_generator(
                rule['nested_xpath']['content_xpath'],
                rule['nested_xpath']['key_xpath']
            )
        elif 'constant' in rule:
            field = self._get_single_field(rule)
            result['parse_function'] = Generators.constant_scrape_generator(
                field,
                rule['constant']
            )
        else:
            field = self._get_single_field(rule)
            result['parse_function'] = Generators.clean_scrape_generator(
                field
            )
        return result

    def _get_single_field(self, rule):
        ''' _get_field - If a rule has a single field name, the field name is
            returned. If multiple field names are found, or the field is blank,
            an exception is raised
        '''
        if type(rule['field']) is dict and 'name' in rule['field']:
            field = rule['field']['name']
        elif isinstance(rule['field'], basestring):
            field = rule['field']
        elif type(rule['field']) is list and len(rule['field']) == 1:
            field = rule['field'].pop()['name']
        else:
            field = ''
        return field

    def _evaluate_rule(self, response, rule):
        ''' _process_rule takes a downloaded page and a parsed rule (with fields xpath, key_dict
            and parse_function) and returns a list of dictionary with the field
            name and the content that was parsed for that field
        '''
        selector = response.xpath(rule['xpath'])
        result = rule['parse_function'](selector)
        if isinstance(result, list):
            return [(rule['key_dict'][key], content) for key, content in result]
        else:
            key, content = result
            print "key, content", key, content
            if isinstance(key, basestring) and key != "":
                return [(rule['key_dict'][key], content)]
            else:
                return [(None, None)]
