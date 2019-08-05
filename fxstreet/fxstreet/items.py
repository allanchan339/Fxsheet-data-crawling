# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FxstreetItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    real_data = scrapy.Field()
    consensus_data = scrapy.Field()
    previous_data = scrapy.Field()
    next_release = scrapy.Field()
    name = scrapy.Field()
    country = scrapy.Field()
    date_release = scrapy.Field()
    links = scrapy.Field()
    next_release_time = scrapy.Field()