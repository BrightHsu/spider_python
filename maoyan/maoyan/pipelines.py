# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook

class MaoyanPipeline(object):
    workbook = Workbook()  # 创建Excel表格
    worksheet = workbook.active  # 切换到活跃的工作表
    worksheet.append(['排名', '电影', '主演', '评分', '剧情介绍', '详细链接'])  # 添加表头信息

    def process_item(self, item, spider):

        line = [item['rank'], item['title'], item['actor'], item['score'], item['content'], item['link']]
        self.worksheet.append(line)
        self.workbook.save('movies.xlsx')   # 保存到本地excel
        return item
