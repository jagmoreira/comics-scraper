# -*- coding: utf-8 -*-
"""Scrapy settings for comics project"""

from comics.user_settings import INCLUDE, EXCLUDE, COMPANIES, USER_AGENT

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

LOG_ENABLED = True
LOG_LEVEL = 'ERROR'
