# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

class AmazonPipeline(object):

    def __init__(self):
        self.setup_db_conn()
        self.create_tables()

    def setup_db_conn(self):
        self.conn = sqlite3.connect('../../databases/database.db')
        self.curr = self.conn.cursor()

    def create_tables(self):
        self.create_amazon_table()
        self.create_images_table()
        self.create_comments_table()

    def close_db(self):
        self.conn.close()

    def __del__(self):
        self.close_db()

    def create_amazon_table(self):
        self.curr.execute("""CREATE TABLE IF NOT EXISTS PRODUCTOS(
                        asin TEXT PRIMARY KEY NOT NULL,
                        sex TEXT,
                        rating TEXT,
                        description TEXT,
                        reviews INTEGER,
                        brand TEXT,
                        min_price TEXT,
                        max_price TEXT
                        )""")


    def create_images_table(self):
        self.curr.execute("""CREATE TABLE IF NOT EXISTS IMAGENES(
                        asin TEXT FOREING KEY NOT NULL,
                        url TEXT
                        )""")


    def create_comments_table(self):
        self.curr.execute("""CREATE TABLE IF NOT EXISTS COMENTARIOS(
                        asin TEXT FOREING KEY NOT NULL,
                        comment TEXT
                        )""")

    def process_item(self, item, spider):
        # Para saber si se trata de un producto
        if 'description' in item:
            self.store_product_in_db(item)
            self.store_images_in_db(item)
            print ('--------------------------')
            print ('Product stored in Database')
            print ('--------------------------')

        # Para saber si se trata de un comentario
        if 'comments' in item:
            self.store_comments_in_db(item)
            print ('--------------------------')
            print ('Comment stored in Database')
            print ('--------------------------')


        # self.conn.commit()

        return item

    def store_product_in_db(self, item):
        self.curr.execute("""INSERT INTO PRODUCTOS VALUES( ?, ?, ?, ?, ?, ?, ?, ?)""",(
            item['asin'],
            item['sex'],
            item['rating'],
            item['description'],
            item['reviews'],
            item['brand'],
            item['min_price'],
            item['max_price']
        ))
        self.conn.commit()

    def store_images_in_db(self, item):
        for i in range(len(item['image_urls'])):
            self.curr.execute("""INSERT INTO IMAGENES VALUES( ?, ?)""",(
                item['asin'],
                item['image_urls'][i]
            ))
            self.conn.commit()

    def store_comments_in_db(self, item):
        for i in range(len(item['comments'])):
            self.curr.execute("""INSERT INTO COMENTARIOS VALUES( ?, ?)""",(
                item['asin'],
                item['comments'][i]
            ))
            self.conn.commit()
