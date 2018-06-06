from scrapy.item import Item, Field


class DorogaData(Item):
    url = Field()
    texts = Field()
    images = Field()


class FreedeliveryData(Item):
    image = Field()
    text = Field()
    price = Field()
