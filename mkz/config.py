class ApiConfig:
    @staticmethod
    def comicInfo(comic_id):
        return 'https://comic.mkzcdn.com/comic/info/?comic_id={}'.format(comic_id)

    @staticmethod
    def chapterList(comic_id):
        return 'https://comic.mkzcdn.com/chapter/v1/?comic_id={}'.format(comic_id)

    @staticmethod
    def chapterInfo(comic_id, chapter_id):
        return 'https://comic.mkzcdn.com/chapter/info/?chapter_id={chapter_id}&comic_id={comic_id}'.format(
            comic_id=comic_id,
            chapter_id=chapter_id)

    @staticmethod
    def chapterContent(comic_id, chapter_id):
        return 'https://comic.mkzcdn.com/chapter/content/v1/?chapter_id={chapter_id}&comic_id={comic_id}&format=1&quality=1&type=1'.format(
            comic_id=comic_id,
            chapter_id=chapter_id)
