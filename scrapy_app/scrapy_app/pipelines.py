# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from main.models import Quote, News


class ScrapyAppPipeline(object):
    def process_item(self, item, spider):
        quote = News(
            headline=item.get('headline'),
            body=item.get('body'),
            url=item.get('url')
        )
        quote.save()
        return item
