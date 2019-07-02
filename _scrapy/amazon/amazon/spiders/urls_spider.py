# -*- coding: utf-8 -*-
import scrapy
import re
from urllib.parse import urljoin


class UrlsSpider(scrapy.Spider):
    name = 'urls_spider'
    allowed_domains = ['amazon.com']
    n_pages = 1

    men_urls = [
        'https://www.amazon.com/s?rh=n%3A7141123011%2Cn%3A7147445011%2Cn%3A12035955011%2Cn%3A9103696011%2Cn%3A9056985011%2Cn%3A9056986011&page={}&qid=1562069588&ref=lp_9056986011_pg_2' .format(i) for i in range(1, n_pages+1)]

    women_urls = [
        'https://www.amazon.com/s?rh=n%3A7141123011%2Cn%3A7147445011%2Cn%3A12035955011%2Cn%3A9103696011%2Cn%3A9056921011%2Cn%3A9056922011&page={}&qid=1562070225&ref=lp_9056922011_pg_2' .format(i) for i in range(1, n_pages+1)]

    start_urls = men_urls + women_urls

    def parse(self, response):

        # ENLACE
        urls = response.xpath(
            '//a[@class="a-link-normal a-text-normal"]/@href').extract()

        url_list = []

        for i in urls:
            asin = re.search(r"/\w{10}/", i) # Se extrae el ASIN de la URL por medio de una expresión regular.

            # Se añade al final de la url un campo para identificar si el producto proviene de la página para hombres
            # o para mujeres. Este campo no influye en la redirección y nos sirve para sacar el campo 'sexo'
            # en el siguiente spider.
            if asin is not None:
                if asin is not '/slredirect/':
                    if response.url in self.women_urls:
                        url_list.append(
                            urljoin('https://www.amazon.com/', 'dp/' + asin.group(0).strip('/') + '/F'))
                    else:
                        url_list.append(
                            urljoin('https://www.amazon.com/', 'dp/' + asin.group(0).strip('/') + '/M'))

        # OUTPUT
        yield{
            'page_urls': list(set(url_list))  # Para quitar duplicados
        }
