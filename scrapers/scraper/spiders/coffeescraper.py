from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scraper.items import Coffee
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scraper.parseutils import ParseUtils


class CoffeeSpider(CrawlSpider):
    name = 'CoffeeScraper'
    allowed_domains = []
    start_urls = []
    roaster = ''
    rules = ()

    def __init__(self, *a, **kw):
        self.parse_utils = ParseUtils(CoffeeSpider, self.get_config(), 'parse_item')
        super(CoffeeSpider, self).__init__(*a, **kw)

    def get_config(self):
        raise Exception("Config Error", "get_config should be overriden")
        return

    def parse_item(self, response):
        self.log("Scraping %s" % response.url)

        sel = Selector(response)
        results = self.parse_utils.process_response(sel)
        print "results: ", results

        item = Coffee()
        for key, content in results:
            if isinstance(key, basestring) and key != '':
                item[key] = content
        return item
