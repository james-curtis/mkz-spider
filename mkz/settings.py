BOT_NAME = 'mkz'

SPIDER_MODULES = ['mkz.spiders']
NEWSPIDER_MODULE = 'mkz.spiders'
LOGSTATS_INTERVAL = 1

# DUPEFILTER_DEBUG = True
# SCHEDULER_DEBUG = True

LOG_LEVEL = 'INFO'

# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.70'
ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 99
CONCURRENT_REQUESTS_PER_DOMAIN = 99

COOKIES_ENABLED = False

TELNETCONSOLE_ENABLED = True
TELNETCONSOLE_USERNAME = 'scrapy'
TELNETCONSOLE_PASSWORD = 'scrapy'

DOWNLOADER_MIDDLEWARES = {
    # 'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550,
    # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'mkz.middlewares.CustomUserAgentMiddleware': 545,
    'mkz.middlewares.DownloadLoggerMiddleware': 555,
    # 'mkz.middlewares.HttpProxyMiddleware': 100,
}

EXTENSIONS = {
    # 'scrapy.extensions.telnet.TelnetConsole': None,
    # 'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500,
    # 'scrapy_jsonrpc.webservice.WebService': 501,
}

ITEM_PIPELINES = {
    'mkz.pipelines.MkzPipeline': 300,
    # 'mkz.pipelines.MongoPipeline': 301,
}

# MONGO_URI = 'mongodb://192.168.44.153:27017/'

COMIC_PUBLISH_URL = 'http://chshcms.cc/index.php/api/receive/comic'
CHAPTER_PUBLISH_URL = 'http://chshcms.cc/index.php/api/receive/chapter'
PUBLISH_PWD = '111111'
SCRAPEOPS_API_KEY = ''
