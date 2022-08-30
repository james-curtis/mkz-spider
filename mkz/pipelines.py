# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import pymongo
import requests


class MkzPipeline:
    file = None

    def __init__(self, comic_publish_url, chapter_publish_url, pwd):
        self.comic_publish_url = comic_publish_url
        self.chapter_publish_url = chapter_publish_url
        self.pwd = pwd

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            comic_publish_url=crawler.settings.get('COMIC_PUBLISH_URL'),
            chapter_publish_url=crawler.settings.get('CHAPTER_PUBLISH_URL'),
            pwd=crawler.settings.get('PUBLISH_PWD')
        )

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('type') == 'comic':
            self.comic_publish(adapter.get('data'), spider)
        elif adapter.get('type') == 'chapter':
            self.chapter_publish(adapter.get('data'), spider)
        return item

    def comic_publish(self, item, spider):
        adapter = ItemAdapter(item)
        requests.post(self.comic_publish_url, {
            'pass': self.pwd,
            'cid': adapter.get('theme').split()[0],
            'score': adapter.get('score'),
            'name': adapter.get('name'),
            'text': adapter.get('intro'),
            'content': adapter.get('intro'),
            'pic': adapter.get('cover'),
            'picx': adapter.get('cover'),
            'type': ','.join(adapter.get('theme').split()),
            'yid': 0,
            'author': adapter.get('author'),
            'serialize': adapter.get('status'),
        })

    def chapter_publish(self, item, spider):
        adapter = ItemAdapter(item)
        pic_array = []
        for page_item in adapter.get('pic_list'):
            pic_array.append(page_item['img'])
        pic = '###'.join(pic_array)
        requests.post(self.chapter_publish_url, {
            'pass': self.pwd,
            'mname': ItemAdapter(adapter.get('comic')).get('name'),
            'name': adapter.get('name'),
            'vip': 0,
            'cion': 0,
            'yid': 0,
            'pic': pic,
            'xid': adapter.get('id'),
        })

    class MongoPipeline:

        def __init__(self, mongo_uri, mongo_db):
            self.mongo_uri = mongo_uri
            self.mongo_db = mongo_db

        @classmethod
        def from_crawler(cls, crawler):
            return cls(
                mongo_uri=crawler.settings.get('MONGO_URI'),
                mongo_db=crawler.settings.get('MONGO_DATABASE', 'spider')
            )

        def open_spider(self, spider):
            self.client = pymongo.MongoClient(self.mongo_uri)
            self.db = self.client[self.mongo_db]

        def close_spider(self, spider):
            self.client.close()

        def process_item(self, item, spider):
            adapter = ItemAdapter(item)
            if item.get('type') == 'chapter':
                collection_name = 'chapter'
            else:
                collection_name = 'comic'
            self.db[collection_name].insert_one(ItemAdapter(adapter.get('data')).asdict())
            return item
