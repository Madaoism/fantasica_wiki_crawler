# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FantasicaWikiCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    domain_url = scrapy.Field()
    title = scrapy.Field()
    file_types = scrapy.Field()
    
    file_paths = scrapy.Field()
    files = scrapy.Field()
    file_urls = scrapy.Field()

    pass
