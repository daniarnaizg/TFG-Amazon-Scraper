# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class AmazonItem(scrapy.Item):
    asin = scrapy.Field()
    sex = scrapy.Field()
    rating = scrapy.Field()
    description = scrapy.Field()
    reviews = scrapy.Field()
    brand = scrapy.Field()
    pricerange = scrapy.Field()
    image_urls = scrapy.Field()
    comments = scrapy.Field()
