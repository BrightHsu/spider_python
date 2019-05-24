# -*- coding: utf-8 -*-
import scrapy
from maoyan.items import MaoyanItem


class MoviesSpider(scrapy.Spider):
    name = 'movies'  # 爬虫名称
    allowed_domains = ['maoyan.com']    # 爬取目标主机域名

    # 因为有多页 需要构造起始url
    url = 'https://maoyan.com/board/4?offset='
    offset = '0'
    start_urls = [url+offset]

    def parse(self, response):

        # 获取排名名词列表
        rank_list = response.xpath('//*[@class="board-wrapper"]/dd/i/text()').extract()

        # 获取单页电影名称列表
        titles = response.xpath('//*[@class="movie-item-info"]/p[@class="name"]/a/text()').extract()

        # 获取单页演员名称列表
        actors = response.xpath('//*[@class="movie-item-info"]/p[@class="star"]/text()').extract()

        # 获取单页详情页herf列表
        links = response.xpath('//*[@class="movie-item-info"]/p[@class="name"]/a/@href').extract()

        # 获取单页评分列表
        scores1 = response.xpath('//p/i[@class="integer"]/text()').extract()
        scores2 = response.xpath('//p/i[@class="fraction"]/text()').extract()
        scores = [scores1[i] + scores2[i] for i in range(len(scores2))]

        for i in range(len(links)):
            # 实例化item,并存入title actor score link 信息
            item = MaoyanItem()
            item['rank'] = rank_list[i].strip()
            item['title'] = titles[i].strip()
            item['actor'] = actors[i].strip()
            item['score'] = scores[i].strip()

            # 构造详情页内容完整链接,进行二级页面爬取
            url_link = 'https://maoyan.com'
            item['link'] = url_link + links[i].strip()

            # 发起内容页请求，并启动parse_content解析
            yield scrapy.Request(item['link'], callback=self.parse_content, meta={"item": item})
            # meta是response的一个成员变量，加入meta以后可以通过meta把额外一些内容添加到response中

        # 循环翻页
        for num in range(10):
            offset = str(num) + self.offset

            yield scrapy.Request(self.url+offset, callback=self.parse)

    def parse_content(self, response):

        # 一级内页item数据提取
        item = response.meta["item"]

        # 继续存入item数据
        content = response.xpath('//*[@class="mod-content"]/span/text()').extract()
        item['content'] = content[0].strip()

        yield item

