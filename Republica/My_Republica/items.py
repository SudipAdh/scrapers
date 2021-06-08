# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyRepublicaItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    published_date = scrapy.Field()
    source = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    
