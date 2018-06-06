from scrapy import signals
from xml.dom.minidom import parseString
from io import open
from lxml import etree


class XmlExportPipeline(object):
    document = '<?xml version="1.0" ?><data></data>'

    def __init__(self, filename):
        self.xml = None
        self.root = None
        self.filename = filename

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.xml = parseString(self.document)
        self.root = self.xml.getElementsByTagName('data')[0]

    def spider_closed(self, spider):
        with open('%s.xml' % self.filename, 'w', encoding='utf-8') as f:
            f.write(self.xml.toprettyxml())


class DorogaXmlExportPipeline(XmlExportPipeline):
    def __init__(self):
        super(DorogaXmlExportPipeline, self).__init__('doroga')
        self.count_list = []

    def spider_closed(self, spider):
        super(DorogaXmlExportPipeline, self).spider_closed(spider)

        print('#' * 44)
        print('Minimal number of graphical fragments', min(self.count_list))
        print('#' * 44)

    def process_item(self, item, spider):
        page_element = self.xml.createElement('page')
        page_element.setAttribute('url', item['url'])

        for image in item['images']:
            image_element = self.xml.createElement('fragment')
            image_element.setAttribute('type', 'image')
            text_node = self.xml.createTextNode(image)
            image_element.appendChild(text_node)
            page_element.appendChild(image_element)

        for text in item['texts']:
            if not text.isspace():
                text_element = self.xml.createElement('fragment')
                text_element.setAttribute('type', 'text')
                text_node = self.xml.createTextNode(text.strip())
                text_element.appendChild(text_node)
                page_element.appendChild(text_element)

        self.root.appendChild(page_element)

        self.count_list.append(len(item['images']))

        return item


class FreedeliveryXmlExportPipeline(XmlExportPipeline):
    def __init__(self):
        super(FreedeliveryXmlExportPipeline, self).__init__('freedelivery')

    def spider_closed(self, spider):
        super(FreedeliveryXmlExportPipeline, self).spider_closed(spider)
        self.create_xhtml()

    def create_xhtml(self):
        dom = etree.parse('%s.xml' % self.filename)
        xslt = etree.parse('%s.xsl' % self.filename)
        transform = etree.XSLT(xslt)
        new_dom = transform(dom)

        with open('%s.html' % self.filename, 'w') as f:
            f.write(etree.tostring(new_dom, pretty_print=True).decode('utf-8'))

    def process_item(self, item, spider):
        item_element = self.xml.createElement('item')

        image_element = self.xml.createElement('image')
        text_node = self.xml.createTextNode(item['image'])
        image_element.appendChild(text_node)
        item_element.appendChild(image_element)

        text_element = self.xml.createElement('text')
        text_node = self.xml.createTextNode(item['text'].strip())
        text_element.appendChild(text_node)
        item_element.appendChild(text_element)

        price_element = self.xml.createElement('price')
        text_node = self.xml.createTextNode(item['price'].strip())
        price_element.appendChild(text_node)
        item_element.appendChild(price_element)

        self.root.appendChild(item_element)

        return item
