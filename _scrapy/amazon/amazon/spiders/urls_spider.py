# -*- coding: utf-8 -*-
import scrapy, re
from urllib.parse import urljoin


class UrlsSpiderSpider(scrapy.Spider):
    name = 'urls_spider'
    allowed_domains = ['amazon.com']
    n_pages = 1

    men_urls = [
        'https://www.amazon.com/s/ref=sr_pg_2?fst=as%3Aoff&rh=n%3A16225019011%2Cn%3A1040658%2Cn%3A15697821011%2Cn%3A1045624&bbn=16225019011&ie=UTF8&qid=1548234697&ajr=3&page={}' .format(i) for i in range(1, n_pages+1)]
    
    women_urls = [
        'https://www.amazon.com/s?rh=n%3A7141123011%2Cn%3A7147445011%2Cn%3A12035955011%2Cn%3A9103696011%2Cn%3A9056921011%2Cn%3A9056922011%2Cn%3A9056923011&page={}' .format(i) for i in range(1, n_pages+1)]
    
    start_urls = men_urls + women_urls

    def parse(self, response):
        # urls = response.xpath('//a[@class="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal"]/@href').extract()
        urls = response.xpath(
            '//a[@class="a-link-normal a-text-normal"]/@href').extract()

        url_list = []

        for i in urls:
            # url = urljoin(response.url, i)
            asin = re.search(r"/\w{10}/", i)
            if asin is not None:
                if response.url in self.women_urls:               
                    url_list.append(urljoin('https://www.amazon.com/','dp/' + asin.group(0).strip('/') + '/w'))
                else:
                    url_list.append(urljoin('https://www.amazon.com/','dp/' + asin.group(0).strip('/') + '/m'))

        # print(url_list)

        yield{
            'page_urls': list(set(url_list)) # PARA QUITAR DUPLICADOS
        }
