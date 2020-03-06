# -*- coding: utf-8 -*-
#File from https://github.com/michalmiki/scrapy
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class OtomotoPipeline(object):
    def process_item(self, item, spider):
        return item
