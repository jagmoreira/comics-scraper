# -*- coding: utf-8 -*-
"""Scrapy settings for comics project"""

BOT_NAME = 'comics'

SPIDER_MODULES = ['comics.spiders']
NEWSPIDER_MODULE = 'comics.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'comics.pipelines.ComicsFilterPipeline': 300,
    'comics.pipelines.InfoWriterPipeline' : 500,
}
# Count comic covers by default
INFO_WRITER_COUNT_COVERS = True

LOG_ENABLED = True
LOG_LEVEL = 'ERROR'

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# Override default settings with any user-defined ones
from comics.user_settings import *
