# -*- coding: utf-8 -*-
import scrapy
from lianjia.settings import USER_AGENT_LIST
import random
import re
from lianjia.items import LianjiaItem


class LianjiaZufangSpider(scrapy.Spider):
    name = 'lianjia_zufang'
    allowed_domains = ['lianjia.com']
    base_url = "https://sz.lianjia.com/zufang/pg"
    page = 0
    start_urls = [base_url + str(page)]

    def parse(self, response):
        referer = self.base_url + str(self.page)
        headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                   "Accept-Encoding": "gzip, deflate, br",
                   "Accept-Language": "zh-CN,zh;q=0.9",
                   "Connection": "keep-alive",
                   "Host": "sz.lianjia.com",
                   "Referer": referer,
                   "Upgrade-Insecure-Requests": "1",
                   "User-Agent": random.choice(USER_AGENT_LIST)}

        node_list = response.xpath('//div[@class="wrapper"]//ul[@id="house-lst"]/li')
        if not node_list:
            return

        for node in node_list:
            detail_url = node.xpath('./div[@class="info-panel"]/h2/a/@href').extract_first()
            yield scrapy.Request(url=detail_url, headers=headers, callback=self.parse_detail, meta={"detail_url": detail_url})

        self.page += 1
        yield scrapy.Request(url=self.base_url + str(self.page), headers=headers, callback=self.parse)

    def parse_detail(self, response):
        detail_html = response.body.decode("utf-8")
        node_list = response.xpath('//div[@class="content-wrapper"]/div[@class="overview"]/div[@class="content zf-content"]')
        for node in node_list:
            item = LianjiaItem()
            item["address"] = node.xpath('./div[@class="zf-room"]/p[7]/a[1]/text()').extract_first() + "-" + node.xpath('./div[@class="zf-room"]/p[7]/a[2]/text()').extract_first()
            item['price'] = re.compile(r'<span class="total">(.*?)</span>', re.S).findall(detail_html)[0]
            item["address_detail"] = node.xpath('./div[@class="zf-room"]/p[6]/a/text()').extract_first()
            item["detail_url"] = response.meta["detail_url"]
            item["area"] = node.xpath('./div[@class="zf-room"]/p[1]/text()').extract_first()
            item["floor"] = node.xpath('./div[@class="zf-room"]/p[3]/text()').extract_first()
            item["house_type"] = node.xpath('./div[@class="zf-room"]/p[2]/text()').extract_first()
            item["release_time"] = node.xpath('./div[@class="zf-room"]/p[8]/text()').extract_first()
            item["content"] = response.xpath(
                '//div[@class="content-wrapper"]//div[@class="title"]/h1/text()').extract_first()
            yield item
