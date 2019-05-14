# -*- coding: utf-8 -*-
import scrapy
from music.items import MusicItem

class HtqyySpider(scrapy.Spider):
    name = 'htqyy'
    allowed_domains = ['htqyy.com']

    # 分析目标网站，爬取热播榜音乐到本地
    # http://www.htqyy.com/top/musicList/hot?pageIndex=0 目标起始链接
    # http://f2.htqyy.com/play7/57/mp3/5 音乐文件地址

    # 构造起始url
    url = 'http://www.htqyy.com/top/musicList/hot?pageIndex='
    page = 0
    start_urls = [url+str(page)]

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,'
                  'image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'www.htqyy.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
                }

    def parse(self, response):
        nums = response.xpath('//ul/li/span[@class="num"]/text()').extract()    # 获取音乐序号列表
        titles = response.xpath('//ul/li/span[@class="title"]/a/@title').extract()  # 获取音乐名字列表
        sids = response.xpath('//ul/li/span[@class="title"]/a/@sid').extract()  # 获取音乐地址sid列表
        artists = response.xpath('//ul/li/span[@class="artistName"]/a/@title').extract()    # 获取艺术家列表

        # 循环遍历存入item信息
        for i in range(len(titles)):
            link = 'http://f2.htqyy.com/play7/' + sids[i] + '/mp3/5'    # 构造音乐地址完整链接

            item = MusicItem()  # item实例化
            item['num'] = nums[i]
            item['title'] = titles[i]
            item['artist'] = artists[i]
            item['link'] = link
            yield item

        # 设置自动翻页
        while self.page <= 2:
            self.page += 1
            url = self.url + str(self.page)
            yield scrapy.Request(url, callback=self.parse, headers=self.headers)


