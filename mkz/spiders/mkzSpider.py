import scrapy
from mkz.items import *


class MkzspiderSpider(scrapy.Spider):
    name = 'mkzSpider'
    allowed_domains = ['www.mkzhan.com']
    start_urls = ['https://www.mkzhan.com/category/?page=1']

    def parse(self, response, **kwargs):
        yield from self.parseList(response)

    def parseList(self, response):
        node_list = response.xpath("//div[@class='common-comic-item']/a/@href")
        for comic in node_list:
            yield from response.follow(comic, callback=self.parseComicDetail)

    def parseComicDetail(self, response):
        print(response)
        comicItem = Comic()
        comicItem.name = response.xpath("//p[@class='comic-title j-comic-title']/text()")
        comicItem.score = response.xpath("//div[@class='rate-handle layui-inline']/span[@class='layui-inline']/text()")
        comicItem.theme = response.xpath("//div[@class='comic-status']/span[@class='text'][1]/b/text()")
        comicItem.intro = response.xpath("//p[contains(@class, 'intro')]/text()")
        comicItem.cover = response.xpath("//div[@class='de-info__cover']/img[@class='lazy']/@src")

        pass
