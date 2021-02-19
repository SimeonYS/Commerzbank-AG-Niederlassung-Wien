import scrapy
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from ..items import CommerzItem
pattern = r'(\r)?(\n)?(\t)?(\xa0)?'

class SpiderSpider(scrapy.Spider):
    name = 'spider'

    start_urls = ['https://www.commerzbank.com/de/hauptnavigation/presse/pressemitteilungen/archiv1/2021/1__quartal_1/presse_archiv_21_01.html']

    def parse(self, response):
        links = response.xpath('//a[@class="more"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)


    def parse_article(self, response):

        item = ItemLoader(CommerzItem())

        item.default_output_processor = TakeFirst()
        date = response.xpath('//div[@id="contentBody"]/div[@class="section"]/p[1]/text()').get()
        title = response.xpath('//div[@id="contentBody"]//h3//text()').get()
        content = response.xpath('//div[@class="section"]/ul//text()').getall()+response.xpath('//div[@class="section clearfix "]//text()').getall()
        content = [text.strip() for text in content if text.strip()][:-1]
        content = re.sub(pattern, "",' '.join(content))

        item.add_value('date', date)
        item.add_value('title', title)
        item.add_value('link', response.url)
        item.add_value('content', content)
        return item.load_item()