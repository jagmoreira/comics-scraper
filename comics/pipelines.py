# -*- coding: utf-8 -*-
"""Pipelines to filter and format scraping output

Don't forget to add your pipeline to the ITEM_PIPELINES setting
See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
"""
import re
from collections import defaultdict
from datetime import datetime

from scrapy.exceptions import DropItem


class ComicsFilterPipeline:
    """Filter for unwanted comics.

    Only includes comics whose title partially matches those from the
    `user_settings.INCLUDE` tuple.
    """
    def __init__(self, include, exclude):
        self.re_include = re.compile('(' + '|'.join(include) + ')+')
        self.re_exclude = re.compile('(' + '|'.join(exclude) + ')+')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(include=crawler.settings.get('INCLUDE', []),
                   exclude=crawler.settings.get('EXCLUDE', []))

    def process_item(self, item, spider):
        safe = False
        # Some items have no title
        # If they have a title but not a '#' character they
        # are assumed to be either a HC or a TP
        if ('title' in item)  and ('#' in item['title']) and ('Poster' not in item['title']):
            if self.re_include.search(item['title']):
                if not self.re_exclude.search(item['title']):
                    safe = True

        if not safe:
            raise DropItem('%s not in include list.' % item['title'])

        # filtering out comics with no release date
        try:
            item['cur_date'] = datetime.strptime(item['cur_date'], '%m/%d/%y')
        except ValueError:
            raise DropItem('%s has no release date' % item['title'])

        return item


class InfoWriterPipeline:
    """Final output formatter."""
    def __init__(self, count_covers=True):
        self.count_covers = count_covers
        self.comicsinfo = defaultdict(lambda: defaultdict(int))

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        table = settings.getbool('INFO_WRITER_COUNT_COVERS', True)

        # Instantiate the pipeline with your table
        return cls(table)

    def process_item(self, item, spider):
        short_title = re.search(r'(?P<comic>^.*\#[\w/.]+)(\s|$)', item['title'])
        short_title = short_title.group('comic')

        self.comicsinfo[item['cur_date']][short_title] += 1

        return item

    def close_spider(self, spider):
        def write_month(output, date):
            output.write('****************\n')
            output.write(date.strftime('%B') + ':\n')

        # sorting by chronological order
        chrono_dates = sorted(self.comicsinfo.keys())
        if chrono_dates:
            with open('final_data.txt', 'w') as output:
                write_month(output, chrono_dates[0])
                prev_mon = chrono_dates[0].strftime('%Y/%m')

                for date in chrono_dates:
                    new_mon = date.strftime('%Y/%m')
                    if new_mon > prev_mon:
                        write_month(output, date)
                        prev_mon = new_mon
                    output.write(f"\t{date.strftime('%m/%d/%Y')}\n")

                    if self.count_covers:
                        for title, covers in self.comicsinfo[date].items():
                            output.write(f'\t-{title} ({covers} covers)\n')
                    else:
                        for title in self.comicsinfo[date].keys():
                            output.write(f'\t-{title}\n')

                    output.write('\n')
