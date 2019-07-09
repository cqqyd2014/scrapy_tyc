# -*- coding: utf-8 -*-
import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['sina.com']
    start_urls = ['http://sina.com/']

    def parse(self, response):
        pass
