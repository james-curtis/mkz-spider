# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# 漫画数据
class Comic(scrapy.Item):
    # define the fields for your item here like:
    """漫画名"""
    name = scrapy.Field()

    """漫画作者"""
    author= scrapy.Field()

    """评分"""
    score = scrapy.Field()

    """题材"""
    theme = scrapy.Field()

    """介绍"""
    intro = scrapy.Field()

    """封面图"""
    cover = scrapy.Field()

    """漫画ID"""
    id = scrapy.Field()

    """漫画状态，连载中还是已完结"""
    status = scrapy.Field()


# 章节数据
class Chapter(scrapy.Item):
    """章节ID"""
    id = scrapy.Field()

    """漫画数据"""
    comic = scrapy.Field()

    """章节名"""
    name = scrapy.Field()

    pic_list = scrapy.Field()

    """章节封面图"""
    cover = scrapy.Field()


class Page(scrapy.Item):
    """图片链接"""
    img = scrapy.Field()

    """页面id"""
    id = scrapy.Field()
