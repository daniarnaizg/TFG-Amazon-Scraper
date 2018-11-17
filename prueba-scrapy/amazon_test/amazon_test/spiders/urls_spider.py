# -*- coding: utf-8 -*-
import scrapy


class UrlsSpiderSpider(scrapy.Spider):
    name = 'urls_spider'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/Mens-Novelty-T-Shirts/b/ref=dp_bc_7&node=9056987011&page={}' .format(i) for i in range(1)]

    def parse(self, response):
        urls = response.xpath('//a[contains(@class, "a-link-normal s-access-detail-page s-overflow-ellipsis s-color-twister-title-link a-text-normal")]/@href').extract()
        
        yield{
        'page_urls' : urls
        }
