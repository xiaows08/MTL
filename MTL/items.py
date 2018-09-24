# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MtlItem(scrapy.Item):
    # define the fields for your item here like:
    no = scrapy.Field()
    img_num = scrapy.Field()
    user_name = scrapy.Field()
    img_date = scrapy.Field()

    img_urls = scrapy.Field()

    pass
