from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scraper.items import Coffee
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

class BluebottleSpider(CrawlSpider):
    name = 'bluebottlecoffee'
    allowed_domains = ['bluebottlecoffee.com']
    start_urls = ['https://bluebottlecoffee.com/store/coffee']
    roaster = dict(
        name="Blue Bottle Coffee",
        id="xxxx-xxxx"
    )

    # allow=("/store/*"), deny=("/store/brewing", "*/store/merchandise", "/store")
    rules = (Rule(SgmlLinkExtractor(allow=("/store/*",),
                                    restrict_xpaths=('//*[@class="span3 product"]/child::*')),
                                    callback='parse_item'),)

    def parse_item(self, response):
        self.log("Scraping %s" % response.url)

        sel = Selector(response)

        item = Coffee()
        item['name'] = sel.xpath('//h2/text()').extract().pop()
        item['tasting_notes'] = sel.xpath('//h2/following-sibling::*/text()').extract().pop()
        item['price'] = sel.xpath('//h3[@class="your-price"]/text()').extract().pop()
        item['price_unit'] = sel.xpath('//h3[@class="your-price"]/div[@class="variant-description"]/text()').extract()
        item['description'] = sel.xpath('//*[@class="long-overview hidden"]/text()').extract()
        if not 'description' in item or not item['description']:
            item['description'] = sel.xpath('//*[@class="long-overview"]/text()').extract()
        item['roaster'] = self.roaster
        return item
