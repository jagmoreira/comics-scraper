# -*- coding: utf-8 -*-

"""Defines the item loaders to specify how to populate the Items"""

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

class ComicsLoader(ItemLoader):
    # store values instead of lists
    default_output_processor = TakeFirst()
