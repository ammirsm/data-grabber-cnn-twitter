# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.utils.project import get_project_settings


class TwitterSpider(scrapy.Spider):
    name = 'twitter'
    settings = get_project_settings()
    start_urls = [
        'https://mobile.twitter.com/' + settings.get('TWITTER'),
    ]

    def parse(self, response):
        datas = response.css('.tweet')
        for data in datas:
            yield {
                "type": "tweet",
                "tweet": ' '.join([text.strip() for text in data.css('.tweet-text').css("::text").extract()]).strip(),
                "time": ' '.join([text.strip() for text in data.css('.timestamp').css("::text").extract()]).strip(),
                "link": "https://twitter.com" + data.css('.metadata a').xpath('@href').extract_first(),
                "user": "https://twitter.com" + data.css('.user-info a').xpath('@href').extract_first(),
                "user_name": ' '.join(data.css('.user-info a').css("::text").extract()).strip(),
                "user_picture": data.css('.avatar a img').xpath('@src').extract_first(),
            }

