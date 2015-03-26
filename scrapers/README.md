# Scraping Framework
This framework is used to create scrapers for coffee roasters. The goal of this
framework is to reduce the amount of coding necessary to create scrapers.
Scrapers can be created by making a new class in the spiders directory that is
a subclass of CoffeeSpider, specifying the name in a class variable, and
overriding the get_config method. Future improvements could further generalize this
to allow for scraping different objects, configuring the pipeline, and adding
new field patterns. Additionally, objects could be created to decrease the reliance
of the package on properly formatted dictionaries.

The default pipeline takes the object that is parsed from the page and stores
it in RethinkDB. Therefore, to run the scraper with the default pipeline, rethinkdb
must be listening on the default port.

# Docs
This framework is designed to reduce scrapers to defining a set of rules, based
on a number of patterns that are common in displaying data on an HTML page of
a coffee.

## Creating a spider
To create a new spider, you must subclass the CoffeeSpider class. In the subclass
you must specify the name of the spider in a static variable holding a string, then specify a configuration by overriding the `get_config(self)` method. An example of this is seen below. The name will be used in running the scraper with the command `scrapy crawl <scraper_name>`
```python
# -*- coding: utf-8 -*-
from scraper.spiders.coffeescraper import CoffeeSpider

class CounterCultureSpider(CoffeeSpider):
  name='counterculture'
  def get_config(self):
    return {
          'name': 'examplescraper',
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
```
## Configuring Spiders
The configuration object that is used has 6 top level fields.
### Name
The name field is used to override the name of the base spider. It should be the same as the static variable that was specified.
### Allowed Domains (Required)
The allowed domain field is a list of domains that are allowed to be searched. For this use case it will generally be the main address for the roaster website
### start_urls (Required)
The start urls field is a list of strings that specify the address where the scraping should be started.
### link_urls
The link_urls field is a list of dictionaries that specifies the rules for which the current page should be searched looking for other lists of products. This is common when the product list is broken up into multiple pages. The allow field of this page specifies a regular expression of which links will be allowed. The restrict_xpath field limits the portion of the page that will be searched. The links that are found that match these parameters will be followed and searched for more link_urls and page_urls according to the same rules.
### page_rules (Required)
The page rules field is a list of dictionaries that of the same form as in the link_urls; however, the page_urls define the links that should be parsed as a coffee.
### content_rules (Required)
The coffee_rules field is a list of dictionaries specifying rules about how a coffee should be parsed from a web page. This is accomplished by specifying an xpath and one of the extraction methods. If no extraction method is specified, the xpath is assumed to exactly find the content for the field.
>#### Field (Required)
> A field should be one of three types, a string, a dictionary, or a list of dictionaries. If a string is specified, it should be one of the field names of a coffee object (see below).
> If a dictionary is specified it should have a name field and optionally a key field. The name field will be used to index into the Coffee item, so it must be available. The key is the value found of the page for a split object form or a nested xpath form. An example of this occurs how some pages call the coffees varietal field *cultivar* instead. in this case the field value would look as follows
> ```python
{
  'field': {
    'name': 'varietal',
    'key': 'cultivar'
  }
}
> ```
This mapping will be expained in greater detail in the split and nested_xpath explaination.
#### xpath (Required)
The xpath field is the xpath to extract the content from the page. If there are multiple fields listed, this xpath should be the xpath that results in a list of selectors with each row corresponding to one of the fields.
#### Extraction Methods
If the xpath specified by the content rule does not result in the exact content desired for the given field, extraction methods can be used to specify the desired content.
There are currently 3 extraction methods that have been implemented. These are formats that are commonly found on roaster websites, more can be added later if there is need.
##### split
split is used to extract data of the form
```html
<div id="my-div">
  <p>name: Coffee Name</p>
  <p>Origin: A location<p>
  <p>Variety - bourbon</p>
</div>
```
To extract the name, origin and varietal of this coffee, the content rule would look like this:
```python
{
  'field': [
    {
      'name': 'name',
    }, {
      'name': 'origin',
      'key': 'Origin'
    }, {
      'name': 'varietal',
      'key': 'Variety'
    }
  ],
  'xpath': '//some/xpath/to/my-div/p/text()',
  'split': {
      'split_character': [u' : ', u' - '],
      'key_index': 0,
      'content_index': 1
  }
}
```
If a single field is given the key_index can be ommited and the field name is
used to store the content that is extracted. An example of this can be seen for
the name field of the Counter Culture spider.
##### nested_xpath
The nested xpath method is used to extract key and content values when they can
be seperated using different xpaths applied to the parent selector.
```html
<div id="my-div">
  <p><strong>name</strong> Coffee Name</p>
  <p><strong>Origin</strong> A location<p>
  <p><strong>Variety</strong> bourbon</p>
</div>
```
The content rule used to extract the keys and values for this structure is shown
below.
```python
{
  'field': [
    {
      'name': 'name',
    }, {
      'name': 'origin',
      'key': 'Origin'
    }, {
      'name': 'varietal',
      'key': 'Variety'
    }
  ],
  'xpath': '//some/xpath/to/my-div/p',
  'nested_xpath': {
      'key_xpath': 'strong/text()',
      'content_xpath': 'text()'
  }
}
```

## Coffee Object
The fields available in the coffee object are as follows:
1. name - name of the coffee
1. roaster - name of the roaster
1. description - a description of the coffee
1. origin - the string representing the origin of the coffee we will convert this to a usuable origin later
1. varietal - the varietals used in the coffee
1. elevation - the elevationt the coffee is produced at
1. producer - producer of the coffee
