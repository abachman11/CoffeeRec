from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scraper.items import Coffee
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scraper.parseutils import ParseUtils


class CoffeeSpider(CrawlSpider):
    name = 'coffeescraper'
    allowed_domains = ['counterculturecoffee.com']
    start_urls = ['https://counterculturecoffee.com/store/coffee']
    roaster = dict(
        name="Counter Culture",
        id="xxxx-xxxx"
    )

    def __init__(self, *a, **kw):
        ParseUtils.parse_config(self.get_config())
        print CoffeeSpider.mConfig
        CoffeeSpider.rules = ();
        super(CoffeeSpider, self).__init__(*a, **kw)

    def get_config(self):
        print "SHOULD OVERRIDE GET CONFIG"
        return


    # allow=("/store/*"), deny=("/store/brewing", "*/store/merchandise", "/store")
    rules = (   Rule(SgmlLinkExtractor(allow=("/store/coffee\?p=\d+"))),
                Rule(SgmlLinkExtractor(allow=("/store/coffee/*"),
                                       restrict_xpaths=('//h2[@class="product-name"]')),
                                    callback='parse_item'))

    def parse_item(self, response):
        self.log("Scraping %s" % response.url)

        sel = Selector(response)

        item = Coffee()
        h1 = sel.xpath('//div[@class="product-name"]/h1/text()').extract().pop().split(u'\u2013 ')
        if len(h1) < 2:
          h1 = h1[0].split(u' - ')
        item['name'] = h1[0];
        item['tasting_notes'] = (sel.xpath('//*[@class="product-short-description"]/text()')
                                    .extract()
                                    .pop()
                                    .strip())

        item['description'] = reduce((lambda x, y: x + y),
            sel.xpath('//div[@id="accordion"]/div[1]/div/text()').extract(), u'')
        item['origin'] = reduce((lambda x, y: x + y),
            sel.xpath('//div[@id="accordion"]/h3[text()="Place"]/following-sibling::div/div/text()').extract(),
            u'').strip()
        item['roaster'] = self.roaster
        return item