# mkzSpider

## 使用方法

开启抓取
```shell
# 下载代码
cd ~
git clone https://github.com/james-curtis/mkz-spider.git
cd mkz-spider
# 安装依赖
pip install -r requirements.txt
# 开始采集
# COMIC_PUBLISH_URL 替换成你对应的漫画发布地址
# CHAPTER_PUBLISH_URL 替换成你对应的章节发布地址
# PUBLISH_PWD 替换成你对应的发布密码
scrapy crawl mkzSpider -s COMIC_PUBLISH_URL="http://chshcms.cc/index.php/api/receive/comic" -s CHAPTER_PUBLISH_URL="http://chshcms.cc/index.php/api/receive/chapter" -s PUBLISH_PWD="111111"
```

暂停/恢复
```shell
telnet 127.0.0.1 6023
# 暂停
engine.pause()
# 恢复
engine.unpause()
```