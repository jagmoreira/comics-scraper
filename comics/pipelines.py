"""
File: pipelines.py
Author: Joao Moreira
Creation Date: Jan 5, 2014

Description:
Pipelines to filter out comics we don't want and count the variant covers.
"""
import re
from collections import defaultdict
from time import strptime, strftime

from scrapy.exceptions import DropItem
from comics.comics_list import include, exclude

class ComicsFilterPipeline(object):
    """
    Filter for unwanted comics.
    Only includes comics whose title partially matches those from the
    {targets} tuple.
    """
    def __init__(self):
        self.re_include = re.compile("(" + "|".join(include) + ")+")
        self.re_exclude = re.compile("(" + "|".join(exclude) + ")+")

    def process_item(self, item, spider):
        safe = False
        # Some items have no title
        # If they have a title but not a '#' character they are assumed to
        # be either a HC or a TP
        if ('title' in item)  and ("#" in item['title']):
            if self.re_include.search(item["title"]):
                if not self.re_exclude.search(item["title"]):
                    safe = True

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
        short_title = re.search('(?P<comic>^.*\#[\w.]+)(\s|$)', item['title'])
        short_title = short_title.group('comic')

        self.comicsinfo[item['cur_date']][short_title] += 1

        return item

    def close_spider(self, spider):
        def write_month(output, date):
            output.write("****************\n")
            output.write(strftime('%B', date) + ":\n")

        # sorting by chronological order
        chrono_dates = sorted(self.comicsinfo.keys())
        with open('final_data.txt', 'wb') as output:
            write_month(output, chrono_dates[0])
            month = chrono_dates[0].tm_mon

            for date in chrono_dates:
                if date.tm_mon > month:
                    write_month(output, date)
                    month = date.tm_mon
                output.write("\t{0:s}\n".format(strftime('%d/%m/%y', date)))

                for title, covers in self.comicsinfo[date].iteritems():
                    output.write(
                        "\t-{0:s} ({1:d} covers)\n".format(title, covers)
                    )

                output.write("\n")
