# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class AmazontutorialPipeline(object):
    def __init__( self ):
        self.create_connection()
        self.create_table()

    def create_connection( self ):
        self.conn = mysql.connector.connect(
                host = 'localhost',
                user = 'allanchan339',
                passwd = '33715882aAB',
                database = 'amazon'
                )
        self.curr = self.conn.cursor()

    def create_table( self ):
        self.curr.execute("""DROP TABLE IF EXISTS amazon_tb""")
        self.curr.execute("""create table amazon_tb(
                       product_name text,
                       product_author text,
                       price float,
                       image_link text
                       )""")

    def process_item( self, item, spider ):
        self.store_db(item)
        print("Pipeline: " + item['title'][0])
        return item

    def store_db( self, item ):
        self.curr.execute("""insert into quotes_tb values (%s,%s,%s,%s)""", (
                item['title'][0],
                item['author'][0],
                item['tag'][0]
                ))

        self.conn.commit()
