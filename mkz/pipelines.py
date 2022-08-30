# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json.decoder

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .spiders.mkzSpider import spider_name
# import pymongo
from scrapeops_python_requests.scrapeops_requests import ScrapeOpsRequests


class MkzPipeline:
    file = None

    def __init__(self, comic_publish_url, chapter_publish_url, pwd, scrapeops_logger, requests):
        self.comic_publish_url = comic_publish_url
        self.chapter_publish_url = chapter_publish_url
        self.pwd = pwd
        self.scrapeops_logger = scrapeops_logger
        self.requests = requests

    @classmethod
    def from_crawler(cls, crawler):
        scrapeops_logger = ScrapeOpsRequests(
            scrapeops_api_key=crawler.settings.get('SCRAPEOPS_API_KEY'),
            spider_name=spider_name,
            job_name='漫画发布',
        )
        return cls(
            comic_publish_url=crawler.settings.get('COMIC_PUBLISH_URL'),
            chapter_publish_url=crawler.settings.get('CHAPTER_PUBLISH_URL'),
            pwd=crawler.settings.get('PUBLISH_PWD'),
            scrapeops_logger=scrapeops_logger,
            requests=scrapeops_logger.RequestsWrapper()
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
        data = {
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
        }
        response = self.requests.post(self.comic_publish_url, data)
        self.record_comic_log(spider, response, data, item)

    def record_comic_log(self, spider, response, data, item):
        def output_log(level, msg):
            log_msg = 'comic_id:{} comic_name:{} {msg}'.format(item.get('id'), item.get('name'), msg=msg)
            if level == 'error':
                spider.logger.error(log_msg)
            else:
                spider.logger.info(log_msg)

        try:
            if response.json()['code'] == 1:
                output_log('info', response.text)
            else:
                output_log('error', '漫画入库失败')
        except json.decoder.JSONDecodeError:
            output_log('error', '漫画入库失败')

        self.scrapeops_logger.item_scraped(
            item=data,
            response=response,
        )

    def chapter_publish(self, item, spider):
        adapter = ItemAdapter(item)
        pic_array = []
        for page_item in adapter.get('pic_list'):
            pic_array.append(page_item['img'])
        pic = '###'.join(pic_array)
        data = {
            'pass': self.pwd,
            'mname': ItemAdapter(adapter.get('comic')).get('name'),
            'name': adapter.get('name'),
            'vip': 0,
            'cion': 0,
            'yid': 0,
            'pic': pic,
            'xid': adapter.get('id'),
        }
        response = self.requests.post(self.chapter_publish_url, data)
        self.record_chapter_log(spider, response, data, item)

    def record_chapter_log(self, spider, response, data, item):
        def output_log(level, msg):
            log_msg = 'comic_id:{comic_id} chapter_id:{chapter_id} comic_name:{comic_name} chapter_name:{chapter_name} {msg}'.format(
                comic_id=item.get('comic')['id'],
                chapter_id=item.get('id'),
                comic_name=item.get('comic')['name'],
                chapter_name=item.get('name'),
                msg=msg)
            if level == 'error':
                spider.logger.error(log_msg)
            else:
                spider.logger.info(log_msg)

        try:
            if response.json()['code'] == 1:
                output_log('info', response.text)
            else:
                output_log('error', '章节入库失败')
        except json.decoder.JSONDecodeError:
            output_log('error', '章节入库失败')

        self.scrapeops_logger.item_scraped(
            item=data,
            response=response,
        )

# class MongoPipeline:
#
#     def __init__(self, mongo_uri, mongo_db):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mongo_uri=crawler.settings.get('MONGO_URI'),
#             mongo_db=crawler.settings.get('MONGO_DATABASE', 'spider')
#         )
#
#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]
#
#     def close_spider(self, spider):
#         self.client.close()
#
#     def process_item(self, item, spider):
#         adapter = ItemAdapter(item)
#         if item.get('type') == 'chapter':
#             collection_name = 'chapter'
#         else:
#             collection_name = 'comic'
#         self.db[collection_name].insert_one(ItemAdapter(adapter.get('data')).asdict())
#         return item
