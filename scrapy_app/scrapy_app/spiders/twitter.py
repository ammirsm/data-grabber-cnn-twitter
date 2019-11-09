# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.utils.project import get_project_settings


class TwitterSpider(scrapy.Spider):
    name = 'twitter'
    settings = get_project_settings()
    start_urls = [
        'https://mobile.twitter.com/Microsoft'
    ]

    def parse(self, response):
        datas = response.css('.tweet')
        for data in datas:
            yield {
                "type": "tweet",
                "tweet": ' '.join([text.strip() for text in data.css('.tweet-text').css("::text").extract()]),
                "time": ' '.join([text.strip() for text in data.css('.timestamp').css("::text").extract()])
            }