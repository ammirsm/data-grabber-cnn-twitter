# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.utils.project import get_project_settings


class IcrawlerSpider(scrapy.Spider):
    name = "icrawler"
    settings = get_project_settings()
    url_unqiue = 'https://search.api.cnn.io/content?size=25&q=' + settings.get('KEYWORD') + '&page='
    page_limit = settings.get('PAGE_LIMIT')
    url = 'https://search.api.cnn.io/content?size=25&q=' + settings.get('KEYWORD') + '&page=1'
    start_urls = [
        'https://search.api.cnn.io/content?size=25&q=' + settings.get('KEYWORD') + '&page=1',
    ]


    def parse(self, response):
        number = int(response.url.split("=")[-1])
        number += 1

        response = json.loads(response.body)["result"]

        for news in response:
            yield {
                "type": "news",
                'headline': news["headline"],
                'body': news["body"],
                'url': news["url"]
            }

        next_page_url = self.url_unqiue + str(number)
        if next_page_url is not None and number <= self.page_limit:
            yield scrapy.Request(next_page_url)

