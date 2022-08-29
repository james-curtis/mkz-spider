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

    """评分"""
    score = scrapy.Field()

    """题材"""
    theme = scrapy.Field()

    """介绍"""
    intro = scrapy.Field()

    """封面图"""
    cover = scrapy.Field()


# 章节数据
class Chapter(scrapy.Item):
    """漫画数据"""
    comic = scrapy.Field()

    """章节名"""
    name = scrapy.Field()

    pic_list = scrapy.Field()

    """章节封面图"""
    cover = scrapy.Field()
