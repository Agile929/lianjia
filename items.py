# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    address = scrapy.Field()  # 地址
    price = scrapy.Field()  # 价格
    address_detail = scrapy.Field()  # 详细地址
    detail_url = scrapy.Field()  # 链接
    area = scrapy.Field()  # 面积
    floor = scrapy.Field()  # 楼层
    house_type = scrapy.Field()  # 户型
    release_time = scrapy.Field()  # 发布时间
    content = scrapy.Field()  # 内容描述
