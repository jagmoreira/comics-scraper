"""
File: pipelines.py
Author: Joao Moreira
Creation Date: Jan 5, 2014

Description:
Pipelines to filter out comics we don't want and count the variant covers.
"""

from collections import defaultdict
from time import strptime, strftime
from re import search

from scrapy.exceptions import DropItem
from comics.comics_list import targets

class ComicsFilterPipeline(object):
    """
    Filter for unwanted comics.
    Only includes comics whose title partially matches those from the
    {targets} tuple.
    """
        
    def process_item(self, item, spider):
        safe = False
        # Some items have no title
        # If they have a title but not a '#' character they are assumed to
        # be either a HC or a TP
        if item['title'] and ("#" in item['title']):
            for i in targets:
                if i in item['title']:
                    safe = True
                    break
        if not safe:
            raise DropItem("%s not in include list." % item['title'])

        # filtering out comics with no release date
        try:
            item['cur_date'] = strptime(item['cur_date'], '%m/%d/%y')
        except ValueError:
            raise DropItem("%s has no release date" % item['title'])

        return item


class InfoWriterPipeline(object):
    
    def __init__(self):
        self.comicsinfo = defaultdict(lambda: defaultdict(int))

    def process_item(self, item, spider):
        short_title = search('(?P<comic>^.*\#[\w.]+)(\s|$)', item['title'])
        short_title = short_title.group('comic')
        
        self.comicsinfo[item['cur_date']][short_title] += 1

        return item


    def close_spider(self, spider):
        # sorting by chronological order
        with open('final_data.txt', 'wb') as output:
            for date in sorted(self.comicsinfo.keys()):
                output.write("{0:s}\n".format(strftime('%d/%m/%y', date)))

                for title, covers in self.comicsinfo[date].iteritems():
                    output.write(
                        "\t{0:s} ({1:d} covers)\n".format(title, covers)
                    )

                output.write("\n")
