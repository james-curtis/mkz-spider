from mkz.items import *
from mkz.config import *

spider_name = 'mkzSpider'


class MkzspiderSpider(scrapy.Spider):
    name = spider_name
    start_urls = ['https://www.mkzhan.com/category/?page=1']

    def parse(self, response, **kwargs):
        node_list = response.xpath("//div[@class='common-comic-item']/a/@href")
        for comic in node_list:
            comic_id = comic.get().strip('/')
            comic_data = Comic()
            comic_data['id'] = comic_id
            # print("parse {}".format(self.comic_id))
            yield scrapy.Request(response.urljoin(comic.get()), callback=self.parseComicInfo,
                                 cb_kwargs={'comic_data': comic_data, 'comic_id': comic_id})
        if response.xpath("//a[@class='next']/@href").get() is not None:
            yield response.follow(response.xpath("//a[@class='next']/@href").get(), callback=self.parse)

    def parseComicInfo(self, response, comic_id, comic_data):
        comic_data['name'] = response.xpath("//p[@class='comic-title j-comic-title']/text()").get()
        comic_data['author'] = response.xpath("//div[@class='comic-author']/span[@class='name']/a/text()").get()
        comic_data['status'] = response.xpath(
            "//div[@class='de-chapter']/div[@class='de-chapter__title']/span[1]/text()").get()
        comic_data['score'] = response.xpath("//div/@data-score").get()
        comic_data['theme'] = response.xpath("//div[@class='comic-status']/span[@class='text'][1]/b/text()").get()
        comic_data['intro'] = response.xpath("//p[contains(@class, 'intro')]/text()").get().strip()
        comic_data['cover'] = response.xpath("//div[@class='de-info__cover']/img[@class='lazy']/@data-src").get()

        yield {
            'type': 'comic',
            'data': comic_data
        }

        yield scrapy.Request(ApiConfig.chapterList(comic_id), callback=self.parseChapterList,
                             cb_kwargs={'comic_data': comic_data, 'comic_id': comic_id})

        # chapter_list = response.xpath("//li[contains(@class,'j-chapter-item')]")
        # for chapter in chapter_list:
        #     self.chapter_data = Chapter()
        #     self.chapter_data['name'] = chapter.xpath('//a/text()').get()
        #     self.chapter_data['comic'] = self.comic_data
        #     self.chapter_id = chapter.xpath('//a/@data-chapterid').get()
        #     # print("parseComicInfo {} {}".format(self.comic_id, self.chapter_id))
        #     # yield response.follow(chapter.xpath('//a/@href').get(),
        #     #                       callback=self.parseChapterContent)
        #     yield response.follow(ApiConfig.chapterContent(self.comic_id, self.chapter_id),
        #                           callback=self.parseChapterContent)

    def parseChapterList(self, response, comic_id, comic_data):
        data = response.json()
        try:
            for datum in data['data']:
                chapter_id = datum['chapter_id']
                chapter_data = Chapter()
                chapter_data['id'] = chapter_id
                chapter_data['comic'] = comic_data
                chapter_data['name'] = datum['title']
                chapter_data['cover'] = datum['cover']
                if datum['is_vip'] != '1':
                    # print(ApiConfig.chapterContent(comic_id, chapter_id))
                    yield scrapy.Request(ApiConfig.chapterContent(comic_id, chapter_id),
                                         callback=self.parseChapterContent,
                                         cb_kwargs={'comic_data': comic_data, 'comic_id': comic_id,
                                                    'chapter_id': chapter_id, 'chapter_data': chapter_data})
        except AttributeError:
            self.logger.warning('无法找到章节目录')

    def parseChapterContent(self, response, comic_id, comic_data, chapter_id, chapter_data):
        image_list = []
        json_data = response.json()
        # print('parseChapterContent {} comic_id:{} chapter_id:{}'.format(response.text, comic_id, chapter_id))
        # return Chapter()
        if json_data['code'] != '200':
            self.logger.warning(json_data['message'])
            return
        try:
            for page in json_data['data']['page']:
                page_item = Page()
                page_item['img'] = page['image']
                page_item['id'] = page['page_id']
                image_list.append(page_item)
            chapter_data['pic_list'] = image_list
        except AttributeError:
            self.logger.warning('无法找到图片：' + response.text)
        else:
            yield {
                'type': 'chapter',
                'data': chapter_data
            }
