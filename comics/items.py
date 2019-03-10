# -*- coding: utf-8 -*-
"""Models for the scraped comics items."""
import scrapy

class ComicsItem(scrapy.Item):
    title = scrapy.Field()         # comics title
    cur_date = scrapy.Field()      # release date
    orig_date = scrapy.Field()      # release date
    covers = scrapy.Field()    # number of covers
