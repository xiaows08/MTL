# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

import scrapy
from scrapy.pipelines.images import ImagesPipeline

class MtlPipeline(object):
    def process_item(self, item, spider):
        return item

class MtlImgDownloadPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for img_url in item['img_urls']:
            # meta里面的数据是从spider获取，然后通过meta传递给下面方法：file_path
            yield scrapy.Request(img_url, meta={'name': item['user_name']})

    # 重命名下载本地路径及文件名
    def file_path(self, request, response=None, info=None):
        # img_guid = request.url.split('/')[-1]
        img_guid = "_".join(request.url.split('/')[-2:]).strip()
        path = request.meta['name']
        # 过滤windows字符串，不经过这么一个步骤，你会发现有乱码或无法下载
        path = re.sub(r'[？\\*|“<>:/]', '', path)
        # 分文件夹存储的关键：{0}对应着name；{1}对应着image_guid
        filename = u'{0}/{1}'.format(path, img_guid)
        return filename