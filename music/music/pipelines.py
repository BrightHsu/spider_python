# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook
import requests


class MusicPipeline(object):
    workbook = Workbook()   # 创建Excel表格
    worksheet = workbook.active     # 切换到活跃的工作表
    worksheet.append(['序', '歌曲', '艺术家', '歌曲链接'])    # 添加表头信息

    def process_item(self, item, spider):
        # item信息写入Excel中
        line = [int(item['num']), item['title'], item['artist'], item['link']]
        self.worksheet.append(line)
        self.workbook.save('htqyy.xlsx')

        # 保存音乐到本地songs文件里
        reponse = requests.get(item['link']).content
        with open('songs/{}_{}_{}.mp3'.format(item['num'], item['title'], item['artist']), 'ab') as f:
            f.write(reponse)
        return item
