# -*- coding: utf-8 -*-
import scrapy
import json
import re
import js2xml
from urllib.parse import urljoin
from amazon.items import AmazonItem

class ProductsSpider(scrapy.Spider):
	name = 'products_spider'
	allowed_domains = ['amazon.com']
	
	list_urls = []

	try:
		with open('./urls_output.json') as json_data:
			urls = json.load(json_data)
			for i in range(len(urls)):
				list_urls = list_urls + urls[i]['page_urls']
			start_urls = list_urls
	except:
		print('Error con el archivo de entrada.')

	# Función que extrae el precio mínimo de un rango de precios aplicando expresion regular
	def get_min_price(self, price_range):
		min = re.findall(r'\$(.*?)\ ', price_range)
		if len(min) is 0:
			return re.findall(r'(?<=\$).+$', price_range)
		return min

	# Función que extrae el precio máximo de un rango de precios aplicando expresion regular
	def get_max_price(self, price_range):
		max = re.findall(r'(?<= \$).+$', price_range)
		if len(max) is 0:
			return re.findall(r'(?<=\$).+$', price_range)
		return max
	
	def parse(self, response):

		item = AmazonItem()
		
		# ASIN
		item['asin'] = re.search(r"/\w{10}/", response.url).group(0).strip('/')

		# Sexo
		item['sex'] = 'Female' if response.url[-1] is 'F' else 'Male'

		# Rango de precios
		try:
			pricerange = response.xpath('//*[@id="priceblock_ourprice"]/text()').extract()[0]
			item['min_price'] = self.get_min_price(pricerange)[0]
			item['max_price'] = self.get_max_price(pricerange)[0]
		except IndexError:
			item['min_price'] = 'N/A'
			item['max_price'] = 'N/A'

		# Valoración
		try:
			item['rating'] = response.xpath('//*[@id="acrPopover"]/span[1]/a/i[1]/span/text()').extract()[0][:3]
		except IndexError:
			item['rating'] = 'N/A'

		# Número de valoraciones
		try:
			item['reviews'] = int(response.xpath('//*[@id="acrCustomerReviewText"]/text()').extract()[0].split(' ')[0].replace(',',''))
		except IndexError:
			item['reviews'] = 'N/A'

		# Marca
		try:
			item['brand'] = response.xpath('//*[@id="bylineInfo"]/text()').extract()[0] 								# Nombre de la marca sin imagen
		except IndexError:
			try:
				item['brand'] = response.xpath('//*[@id="bylineInfo_feature_div"]/div/a/@href').extract()[0].split('/')[1]	# Nombre de la marca con imagen
			except:
				item['brand'] = 'N/A'

		# Descripción
		try:
			item['description'] = response.xpath('//*[@id="productDescription"]/p/text()').extract()[0]
		except IndexError:
			print('There is no description.')
			item['description'] = 'N/A'
		
		# Imágenes
		# Los enlaces a las imágenes se extraen con la ayuda de una librería llamada js2xml.
		# Esta librería facilita la extracción de elementos embebidos en código JavaScript usando XPath.
		js = response.xpath("//script[contains(text(), 'register(\"ImageBlockATF\"')]/text()").extract_first()
		xml = js2xml.parse(js)
		selector = scrapy.Selector(root=xml)
		item['image_urls'] = selector.xpath('//property[@name="colorImages"]//property[@name="hiRes"]/string/text()').extract()


		# OUTPUT
		yield item