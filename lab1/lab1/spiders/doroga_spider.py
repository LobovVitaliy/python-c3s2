from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import DorogaData


# scrapy crawl doroga
class DorogaSpider(CrawlSpider):
    name = 'doroga'

    start_urls = ['http://www.doroga.ua/']

    allowed_domains = ['doroga.ua']

    custom_settings = {
        'ITEM_PIPELINES': {
            'lab1.pipelines.DorogaXmlExportPipeline': 300
        }
    }

    rules = [
        Rule(LinkExtractor(), process_links=lambda l: l[:5], callback='parse_item')
    ]

    def parse_item(self, response):
        item = DorogaData()
        item['url'] = response.url
        item['images'] = response.xpath('//img/@src').extract()
        item['texts'] = response.xpath('//div/text()').extract()
        return item
