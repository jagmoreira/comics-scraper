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

# Override default settings with any user-defined ones
from comics.user_settings import *
