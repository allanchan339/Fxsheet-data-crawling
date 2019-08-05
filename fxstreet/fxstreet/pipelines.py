# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector
class FxstreetPipeline(object):
    def __init__( self ):
        self.create_connection()
        self.create_table()

    def create_connection( self ):
        self.conn = mysql.connector.connect(
                host = 'localhost',
                user = 'allanchan339',
                passwd = '33715882aAB',
                database = 'fxstreet'
                )
        self.curr = self.conn.cursor()

    def create_table( self ):
        self.curr.execute("""DROP TABLE IF EXISTS NFP_TCH_tb""") #TODO : del this line to save permenantly
        self.curr.execute("""create table NFP_TCH_tb(
                        name text,
                        country text,
                        real_data text,
                        consensus_data text,
                        previous_data text,
                        date_release_GMT0 text,
                        next_release_GMT0 text,
                        next_release_time_GMT0 text,
                        links text
                       )""")

    def process_item( self, item, spider ):

        name_fixed = item['name'][0].strip(' -')

        item['next_release'] = " ".join(item['next_release'].split())
        item['next_release_time'] = item['next_release_time'].split()[0]
        #item['next_release_time'].strip(' GMT')

        self.store_db(item , name_fixed)
      #  print("Pipeline: " + item['title'][0])
        return item

    def store_db( self, item , name_fixed):
        self.curr.execute("""insert into NFP_TCH_tb values (%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (
                name_fixed,
                item['country'][0],
                item['real_data'][0],
                item['consensus_data'][0],
                item['previous_data'][0],
                item['date_release'][0],
                item['next_release'],
                item['next_release_time'],
                item['links']
                ))
        self.conn.commit()

