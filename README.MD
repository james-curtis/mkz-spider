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

## 速度

三万页面/分钟，三万章节/分钟

![](https://tva1.sinaimg.cn/large/008d89Swgy1h5p6ewlr8vj311w07sdvn.jpg)

## 发布报错

在这个文件中增加两行 `sys/apps/controllers/api/Receive.php` 

大概在302行左右
```diff
//更新TAGS主题
private function get_set_tags($tarr, $mid = 0)
{
    foreach ($tarr as $v) {
        $row = $this->mcdb->get_row('type', 'id', array('name' => $v, 'zd' => 'tags'));
        if (!$row) {
            //获取最大ID
            $row = $this->mcdb->get_row('type', 'id', array('zd' => 'tags'), 'xid DESC');
            $tid = $this->mcdb->get_insert('type', array('name' => $v, 'zd' => 'tags', 'fid' => 1, 'cid' => 1, 'xid' => ($row->id + 1)));
        } else {
            $tid = $row->id;
        }
+        $row = $this->mcdb->get_row('comic_type', 'id', array('tid' => $tid, 'mid' => $mid));
+         if (!$row)
            $this->mcdb->get_insert('comic_type', array('tid' => $tid, 'mid' => $mid));
    }
    return true;
}
```