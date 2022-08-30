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
# 后续更新的话重新执行下面这一条命令就可以了
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

使用监控

![](https://tva1.sinaimg.cn/large/008d89Swgy1h5oufnd84fj31hc0ps46l.jpg)

注册 [scrapeops](https://scrapeops.io/) 拿到 `SCRAPEOPS_API_KEY`

然后在执行抓取命令后面加上 `-s SCRAPEOPS_API_KEY=这里是你的key` 即可。就像下面一样
```shell
scrapy crawl mkzSpider -s COMIC_PUBLISH_URL="http://chshcms.cc/index.php/api/receive/comic" -s CHAPTER_PUBLISH_URL="http://chshcms.cc/index.php/api/receive/chapter" -s PUBLISH_PWD="111111" -s SCRAPEOPS_API_KEY="4948e297-23ea-4f50-a670-0cf52c32a8dd" 
```