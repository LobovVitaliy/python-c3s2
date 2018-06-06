from scrapy import Spider
from ..items import FreedeliveryData


# scrapy crawl freedelivery
class FreedeliverySpider(Spider):
    name = 'freedelivery'

    start_urls = ['https://freedelivery.com.ua/arduino-100/']

    custom_settings = {
        'ITEM_PIPELINES': {
            'lab1.pipelines.FreedeliveryXmlExportPipeline': 300
        }
    }

    def parse(self, response):
        for product in response.css('div.product-layout')[:20]:
            item = FreedeliveryData()
            item['image'] = product.css('img::attr(src)').extract_first()
            item['price'] = product.css('.price::text').extract_first()
            item['text'] = product.css('h4 a::text').extract_first()
            yield item
