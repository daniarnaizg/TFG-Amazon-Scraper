# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

class AmazonPipeline(object):

    def __init__(self):
        self.setupDBConn()
        self.createTables()

    def setupDBConn(self):
        self.conn = sqlite3.connect('../../databases/prueba-prices.db')
        self.curr = self.conn.cursor()

    def createTables(self):
        # self.dropAmazonTables()
        self.createAmazonTable()
        self.createImagesTable()
        self.createCommentsTable()

    def dropAmazonTables(self):
        # drop tables if it exists
        # self.curr.execute("DROP TABLE IF EXISTS PRODUCTOS")
        # self.curr.execute("DROP TABLE IF EXISTS IMAGENES")
        self.curr.execute("DROP TABLE IF EXISTS COMENTARIOS")

    def closeDB(self):
        self.conn.close()

    def __del__(self):
        self.closeDB()

    def createAmazonTable(self):
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


    def createImagesTable(self):
        self.curr.execute("""CREATE TABLE IF NOT EXISTS IMAGENES(
                        asin TEXT FOREING KEY NOT NULL,
                        url TEXT
                        )""")


    def createCommentsTable(self):
        self.curr.execute("""CREATE TABLE IF NOT EXISTS COMENTARIOS(
                        asin TEXT FOREING KEY NOT NULL,
                        comment TEXT
                        )""")

    def process_item(self, item):
        # Para saber si se trata de un producto
        if 'description' in item:
            self.storeProductInDb(item)
            self.storeImagesInDb(item)
            print ('--------------------------')
            print ('Product stored in Database')
            print ('--------------------------')

        # Para saber si se trata de un comentario
        if 'comments' in item:
            self.storeCommentsInDb(item)
            print ('--------------------------')
            print ('Comment stored in Database')
            print ('--------------------------')


        # self.conn.commit()

        return item

    def storeProductInDb(self, item):
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

    def storeImagesInDb(self, item):
        for i in range(len(item['image_urls'])):
            self.curr.execute("""INSERT INTO IMAGENES VALUES( ?, ?)""",(
                item['asin'],
                item['image_urls'][i]
            ))
            self.conn.commit()

    def storeCommentsInDb(self, item):
        for i in range(len(item['comments'])):
            self.curr.execute("""INSERT INTO COMENTARIOS VALUES( ?, ?)""",(
                item['asin'],
                item['comments'][i]
            ))
            self.conn.commit()
