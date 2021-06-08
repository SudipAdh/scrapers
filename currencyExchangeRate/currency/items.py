# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CurrencyItem(scrapy.Item):
    # define the fields for your item here like:
    country = scrapy.Field()
    buying_rate = scrapy.Field()
    selling_rate = scrapy.Field()
    date  = scrapy.Field()

