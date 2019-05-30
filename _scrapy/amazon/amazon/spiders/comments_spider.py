# -*- coding: utf-8 -*-
import scrapy, json, re
from urllib.parse import urljoin
from amazon.items import AmazonItem


class CommentsSpider(scrapy.Spider):
    name = 'comments_spider'
    allowed_domains = ['amazon.com']
    start_urls = ['http://amazon.com/']
    n_comment_pages = 1

    list_urls = []
    with open('../../outputs/first500products.json') as json_data:
        products = json.load(json_data)
        for i in range(len(products)):
            asin = products[i]['asin']
            for n in range(1, n_comment_pages + 1):
                list_urls.append(urljoin('https://www.amazon.com/','product-reviews/' + asin + '/ref=cm_cr_arp_d_paging_btm_next_2?pageNumber=' + str(n)))

        start_urls = list_urls
        
    def parse(self, response):

        item = AmazonItem()
        item['asin'] = re.search(r"/\w{10}/", response.url).group(0).strip('/')

        raw_comments = response.xpath("//*[contains(@class, 'a-row a-spacing-small review-data')]/span/span").extract()
        comment_list = []
        for i in raw_comments:
            comment_list.append(re.sub('<.*?>', '', i))     # Regular expression to delete all html tags
        item['comments'] = comment_list

        yield item
