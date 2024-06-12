# -*- coding: utf-8 -*-
"""Spider for comics data."""
import re

import scrapy

from comics.items import ComicsItem
from comics.item_loaders import ComicsLoader

class ComicsSpider(scrapy.Spider):
    """Processes a page containing links to comics from specified companies."""

    name = 'comics'

    start_urls = ['https://gocollect.com/blog/category/comiclist/extended-forecast/']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # We want only 1 set of comics from each company, which is assumed to
        # be the most recent one.
        self.companies_done = set()
        self.done = False
        self.curr_page = 1
        self.max_page = 5

    def parse(self, response):
        """Parse a feed with comics from all companies."""

        patt = f"({'|'.join(self.settings['COMPANIES'])})"

        # Parse posts in index page
        for href in response.css('h2.my-2 > a::attr(href)').getall():
            # Check latest post for links to company pages
            if 'extended-forecasts' in href and not self.done:
                yield response.follow(href, self.parse)

        # Parse links in latest post
        for href in response.css('div.post-content > h4 > a::attr(href)').getall():
            m = re.search(patt, href)

            # Follow links to companies pages if we haven't seen them yet
            if not self.done and m and (m.group(1) not in self.companies_done):
                yield response.follow(href, self.parse_company)
                self.companies_done.add(m.group(1))
                self.done = len(self.companies_done) == len(self.settings['COMPANIES'])

        # If we haven't found all companies, go to next post
        if not self.done and self.curr_page < self.max_page:
            self.curr_page += 1
            next_page = f'{ComicsSpider.start_urls[0]}?page={self.curr_page}'
            yield response.follow(next_page, self.parse)


    def parse_company(self, response):
        """Parse a page with individual comics information."""
        # The comics info is a simple <tr> element
        all_comics = response.css('div.post-body table tr')

        # First row is the table header
        for comic in all_comics[1:]:
            i_loader = ComicsLoader(
                item=ComicsItem(), selector=comic, response=response
            )

            i_loader.add_xpath('title', 'td[3]//text()')
            i_loader.add_xpath('cur_date', 'td[1]/text()')
            i_loader.add_xpath('orig_date', 'td[2]/text()')

            yield i_loader.load_item()
