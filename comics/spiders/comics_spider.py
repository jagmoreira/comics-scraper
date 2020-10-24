# -*- coding: utf-8 -*-
"""Spider for comics data."""
import re

from scrapy.spiders import CrawlSpider

from comics.settings import COMPANIES
from comics.items import ComicsItem
from comics.item_loaders import ComicsLoader

class ComicsSpider(CrawlSpider):
    """Processes a page containing links to comics from specified companies."""

    name = 'comics'

    start_urls = ['https://blog.gocollect.com/category/comiclist/extended-forecast/']

    def __init__(self, *args, **kwargs):
        super(ComicsSpider, self).__init__(*args, **kwargs)
        # We want only 1 set of comics from each company, which is assumed to
        # be the most recent one.
        self.companies_done = set()


    def parse(self, response):
        """Parse a feed with comics from all companies."""

        patt = f"({'|'.join(COMPANIES)})"

        for href in response.css('h2 a::attr(href)').getall():
            m = re.search(patt, href)

            # Follow links to companies pages if we haven't seen them yet
            if m and m.group(1) not in self.companies_done:
                yield response.follow(href, self.parse_company)
                self.companies_done.add(m.group(1))

        # If we haven't found all companies, go to next page
        if len(self.companies_done) != len(COMPANIES):
            for href in response.css('div.penci-pagination li:last-child a::attr(href)'):
                yield response.follow(href, self.parse)


    def parse_company(self, response):
        """Parse a page with individual comics information."""

        # The comics info is a simple <tr> element
        all_comics = response.css('div#penci-post-entry-inner table tr')

        # First row is the table header
        for comic in all_comics[1:]:
            i_loader = ComicsLoader(
                item=ComicsItem(), selector=comic, response=response
            )

            i_loader.add_xpath('title', 'td[3]/text()')
            i_loader.add_xpath('cur_date', 'td[1]/text()')
            i_loader.add_xpath('orig_date', 'td[2]/text()')

            yield i_loader.load_item()
