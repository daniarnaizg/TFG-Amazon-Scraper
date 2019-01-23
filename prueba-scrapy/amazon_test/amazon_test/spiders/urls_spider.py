# -*- coding: utf-8 -*-
import scrapy


class UrlsSpiderSpider(scrapy.Spider):
    name = 'urls_spider'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/s/ref=sr_pg_2?fst=as%3Aoff&rh=n%3A16225019011%2Cn%3A1040658%2Cn%3A15697821011%2Cn%3A1045624&bbn=16225019011&ie=UTF8&qid=1548234697&ajr=3&page={}' .format(i) for i in range(1,25)]
    # start_urls = ['https://www.amazon.com/Mens-Novelty-T-Shirts/b/ref=dp_bc_7&node=9056987011&page={}' .format(i) for i in range(1)]
    # start_urls = ['https://www.amazon.com/s/ref=lp_1045624_pg_2?rh=n%3A7141123011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A2476517011%2Cn%3A1045624&ie=UTF8&qid=1543937727&page={}' .format(i) for i in range(1)]

    def parse(self, response):
        urls = response.xpath('//a[@class="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal"]/@href').extract()
        print(urls)
        yield{
        'page_urls' : urls
        }
