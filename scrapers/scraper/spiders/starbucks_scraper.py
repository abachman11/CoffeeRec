from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scraper.items import Coffee
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

class StarbucksSpider(CrawlSpider):
    name = 'starbucks'
    allowed_domains = ['store.starbucks.com']
    start_urls = ['http://store.starbucks.com/coffee/coffee,default,sc.html?start=1&sz=1000']
    roaster = dict(
        name="Starbucks",
        id="xxxx-xxxx"
    )

    # allow=("/store/*"), deny=("/store/brewing", "*/store/merchandise", "/store")
    rules = (Rule(SgmlLinkExtractor(
                                    restrict_xpaths=('//*[@class="product_info"]')),
                                    callback='parse_item'),)

    def parse_item(self, response):
        self.log("Scraping %s" % response.url)

        sel = Selector(response)

        item = Coffee()
        item['name'] = sel.xpath('//h1[@class="pdp-prodname"]/text()').extract().pop().strip()
        notes = sel.xpath('//span[@class="pdp-label" and text()="Tasting Notes"]/following-sibling::*[@class="pdp-value"]/text()').extract()
        if len(notes) > 0:
            item['tasting_notes'] = notes.pop()

        item['price'] = sel.xpath('//*[@itemprop="price"]/text()').extract().pop().strip()
        price_unit = sel.xpath('//*[@itemprop="weight"]/text()').extract()
        if len(price_unit) > 0:
            item['price_unit'] = price_unit.pop().strip()
        item['description'] = reduce((lambda x, y: x + y),
            sel.xpath('//*[@id="longdesc"]/p/text()').extract(), u'')
        origin = sel.xpath('//span[@class="pdp-label" and text()="Region"]/following-sibling::*[@class="pdp-value amrdot"]/text()').extract()
        if len(origin) > 0:
          item['origin'] = origin.pop();
        item['roaster'] = self.roaster
        return item
