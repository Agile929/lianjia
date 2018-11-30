# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from lianjia.items import  LianjiaItem
import json
import os


class LianjiaPipeline(object):
    def __init__(self):
        dir_name = os.path.dirname(os.path.dirname(__file__))
        new_path = os.path.join(dir_name, "data")
        if not os.path.exists(new_path):
            os.mkdir(new_path)

        self.file = open(new_path + "/lianjia_zufang.json", "w")

    def process_item(self, item, spider):
        if isinstance(item, LianjiaItem):
            content = json.dumps(dict(item), ensure_ascii=False) + ",\n"
            self.file.write(content)
        return item

    def close_spider(self, spider):
        self.file.close()
