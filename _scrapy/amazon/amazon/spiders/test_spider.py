# -*- coding: utf-8 -*-
import scrapy
import json
import re
import js2xml

class TestSpiderSpider(scrapy.Spider):
	name = 'test_spider'
	allowed_domains = ['amazon.com']
	
	list_urls = []
	with open('../../outputs/first500urls.json') as json_data:
		urls = json.load(json_data)
		for i in range(len(urls)):
			list_urls = list_urls + urls[i]['page_urls']
			
		start_urls = list_urls
	
	def parse(self, response):

		item = dict()
		
		item['asin'] = re.search(r"/\w{10}/", response.url).group(0).strip('/')

		item['rating'] = response.xpath('//*[@id="acrPopover"]/span[1]/a/i[1]/span/text()').extract()[0][:3]

		item['description'] = response.xpath('//*[@id="productDescription"]/p/text()').extract()[0]

		item['reviews'] = int(response.xpath('//*[@id="acrCustomerReviewText"]/text()').extract()[0].split(' ')[0].replace(',',''))

		item['brand'] = response.xpath('//*[@id="brand"]/@href').extract()[0].split('/')[1]

		item['pricerange'] = response.xpath('//*[@id="priceblock_ourprice"]/text()').extract()[0]

		
		# Imagenes
		js = response.xpath("//script[contains(text(), 'register(\"ImageBlockATF\"')]/text()").extract_first()
		xml = js2xml.parse(js)
		selector = scrapy.Selector(root=xml)
		item['image_urls'] = selector.xpath('//property[@name="colorImages"]//property[@name="hiRes"]/string/text()').extract()
		
		yield item
