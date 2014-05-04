"""
File: comics_spider.py
Author: Joao Moreira
Creation Date: Jan 5, 2014

Description:
spider for the comics data.
"""

import re
import time
from collections import defaultdict
from operator import itemgetter

from scrapy.spider import Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from comics.items import ComicsItem
from comics.itemloaders import ComicsLoader
from comics.comics_list import companies


class ComicsSpider(Spider):
    """
    Basic comics spider. Processes a single url
    """
    
    # name of spider. must be unique
    # used from command line: `scrapy crawl [name]`
    name = "comics"

    allowed_domains = ["comiclist.com"]

    start_urls = [
        "http://www.comiclist.com/index.php/lists/marvel-comics-extended-forecast-for-03-26-2014",
        "http://www.comiclist.com/index.php/lists/image-comics-extended-forecast-for-03-26-2014"
    ]

    def parse(self, response):
        sel = Selector(response)
        # The website is not very well formatted, which is why we need to be
        # specific in the table selection.
        # The comics info is a simple <tr> element
        all_comics = sel.xpath('//table[@border="1" and @cellspacing="0" and @cellpadding="3"]//tr[position()>1]')

        for comic in all_comics:
            i_loader = ComicsLoader(item=ComicsItem(),
                                        selector=comic,
                                        response=response)

            i_loader.add_xpath('title', 'td[3]/a/text() | td[3]/text()')
            i_loader.add_xpath('cur_date', 'td[1]/text()')
            i_loader.add_xpath('orig_date', 'td[2]/text()')

            yield i_loader.load_item()


class AutomatedComicsSpider(CrawlSpider):
    """
    Advanced comics spider. Processes a page containing several links of
    interest.
    """

    name = "autocomics"

    allowed_domains = ["comiclist.com"]

    start_urls = [
        "http://www.comiclist.com/index.php/lists/ExtendedForecast/"
    ]

    rules = (
        Rule(SgmlLinkExtractor(
                allow=companies,
                restrict_xpaths="//h3[@class='bTitle']",
            ),
            callback='parse_items', follow=True,
            process_links='remove_old_links',
        ),
    )

    def remove_old_links(self, all_links):
        """
        Filter a list of links for more than one listing for the same company.
        Keeps the most recent listing.
        all_links - list of scrapy.link.Link objects
        """

        temp = defaultdict(list)
        for link in all_links:
            for company in companies:
                if company in link.url:
                    match = re.search("(\d{2}-\d{2}-\d{4})$",link.url)
                    date = time.strptime(match.group(0), "%m-%d-%Y")
                    temp[company].append((link,date))
        
        new_links = []
        for val in temp.itervalues():
            val.sort(key=itemgetter(1))
            # We want only the Link object of the latest entry
            new_links.append(val[-1][0])

        return new_links

    def parse_items(self, response):
        """
        Parses a page containing a table with individual comics information
        """
        sel = Selector(response)
        # The website is not very well formatted, which is why we need to be
        # specific in the table selection.
        # The comics info is a simple <tr> element
        all_comics = sel.xpath('//table[@border="1" and @cellspacing="0" and @cellpadding="3"]//tr[position()>1]')
 
        for comic in all_comics:
            i_loader = ComicsLoader(item=ComicsItem(),
                                        selector=comic,
                                        response=response)

            i_loader.add_xpath('title', 'td[3]/a/text() | td[3]/text()')
            i_loader.add_xpath('cur_date', 'td[1]/text()')
            i_loader.add_xpath('orig_date', 'td[2]/text()')

            yield i_loader.load_item()
