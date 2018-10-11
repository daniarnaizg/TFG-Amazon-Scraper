# -*- coding: utf-8 -*-
import scrapy, json


class TestSpiderSpider(scrapy.Spider):
    name = 'test_spider'
    allowed_domains = ['amazon.com']

    with open('./urls.json') as json_data:
    	urls = json.load(json_data)
    	list_urls = list(urls)[0]['urls']

    start_urls = list_urls

    # start_urls = ['https://www.amazon.com/Hanes-Beefy-T-Adult-Short-Sleeve-T-Shirt/dp/B019D425HE/', 'https://www.amazon.com/Next-Level-Premium-N6210-WHITE-L/dp/B006LDYEX4', 'https://www.amazon.com/Dickies-Sleeve-Heavyweight-T-Shirt-X-Large/dp/B00B6EEHI0', 'https://www.amazon.com/Incredibles-Basicon-T-Shirt-Size/dp/B004TCSFXY', 'https://www.amazon.com/Under-Armour-T-Shirt-Graphite-X-Large/dp/B078BBZJ79']


    def parse(self, response):
        item = response.xpath('//span[contains(@class, "a-size-large")]/text()').extract()
        price = response.xpath('//*[@id="priceblock_ourprice"]/text()').extract()
        img = response.xpath('//img[@id="landingImage"]/@data-old-hires').extract()
        rating = response.xpath('//span[contains(@class, "a-icon-alt")]/text()').extract()
        review_count = response.xpath('//span[contains(@data-hook, "total-review-count")]/text()').extract()
        reviews = response.xpath('//span[contains(@data-hook, "review-body")]/text()').extract()

        yield {
        'item'			: item[0].strip(),
        'price'			: price[0],
        'img'			: img[0],
        'rating'		: rating[0][:3],
        'review_count'	: review_count[0],
        'reviews'		: reviews
        }
