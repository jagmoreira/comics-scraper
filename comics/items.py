"""
File: items.py
Author: Joao Moreira
Creation Date: Jan 5, 2014

Description:
Models for the scraped comics items.
See documentation in:
http://doc.scrapy.org/en/latest/topics/items.html
"""

from scrapy.item import Item, Field

class ComicsItem(Item):
    title = Field()         # comics title
    cur_date = Field()      # release date
    orig_date = Field()      # release date
    covers = Field()    # number of covers