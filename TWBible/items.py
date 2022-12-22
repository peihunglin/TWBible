# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TwbibleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    book = scrapy.Field()
    #unibook = scrapy.Field()
    chapterID = scrapy.Field()
    verseID = scrapy.Field()
    verse = scrapy.Field()
    #universe = scrapy.Field()
    pass
