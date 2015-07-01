# Scrapy settings for comics project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'comics'

SPIDER_MODULES = ['comics.spiders']
NEWSPIDER_MODULE = 'comics.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'comics (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'comics.pipelines.ComicsFilterPipeline': 300,
    'comics.pipelines.InfoWriterPipeline' : 500,
}

LOG_ENABLED = True
LOG_LEVEL = 'ERROR'
