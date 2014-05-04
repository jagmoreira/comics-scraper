"""
File: itemloaders.py
Author: Joao Moreira
Creation Date: Jan 5, 2014

Description:
Defines the item loaders to specify how to populate the Items
"""

from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst

class ComicsLoader(ItemLoader):
    # store values instead of lists
    default_output_processor = TakeFirst()

