# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import FantasicaWikiCrawlerItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import os

class FantasicaWikiSpider(CrawlSpider):
    name = 'fantasica_wiki'

    start_urls = [
        'http://www.fantasicawiki.com/wiki/1_Star_Units',
        'http://www.fantasicawiki.com/wiki/2_Star_Units',
        'http://www.fantasicawiki.com/wiki/3_Star_Units',
        'http://www.fantasicawiki.com/wiki/4_Star_Units',
        'http://www.fantasicawiki.com/wiki/5_Star_Units',
        'http://www.fantasicawiki.com/wiki/6_Star_Units',
        'http://www.fantasicawiki.com/wiki/7_Star_Units',
        'http://www.fantasicawiki.com/wiki/8_Star_Units',
        'http://www.fantasicawiki.com/wiki/9_Star_Units',
        'http://www.fantasicawiki.com/wiki/10_Star_Units',
        'http://www.fantasicawiki.com/wiki/11_Star_Units',
        'http://www.fantasicawiki.com/wiki/12_Star_Units'
    ] 

    rules = (
        Rule(LinkExtractor(allow=('^(http://www.fantasicawiki.com/wiki/)(.+)$')), callback='parse_item', follow=True),
    )

    custom_settings = {
        'DEPTH_LIMIT': 1
    }

    # start_urls = [
    #     'http://www.fantasicawiki.com/wiki/Elizabeth_11_v2',
    # ] 

    # rules = (
    #     Rule(LinkExtractor(allow=('^http://www.fantasicawiki.com/wiki/Elizabeth_11_v2$')), callback='parse_item', follow=False),
    # )

    #domain_regex = re.compile("^(http://|https://)?www\.(.*)\.(.*)")
    img_regex = re.compile("(.+)/(.+)\.(jpg|png|gif)$")
    # back_regex = re.compile("(.*)back(_.{2})?.jpg$")
    # jp_regex = re.compile("(.*)(_[jJ][pP])?.jpg$")
    # kr_regex = re.compile("(.*)(_[Kk][Rr])?.jpg$")
    # cn_regex = re.compile("(.*)(_[Cc][Nn])?.jpg$")

    #allowed_domains = ['http://www.fantasicawiki.com']

    def parse_item(self, response):
        print("\n============================== Start of parse for URL: " + response.url)

        item = FantasicaWikiCrawlerItem()

        split_url = response.url.split("//")
        split_domain = split_url[-1].split("/")

        protocol = split_url[0]  # http/https
        domain = split_domain[0] # www.fantasicawiki.com
        title = split_domain[-1]  # Archillea

        img_urls = []
        img_types = []

        # for the large main images
        for img in response.css('div#mw-content-text > p img'):
            temp_url = protocol + "//" + domain + img.css('::attr(src)').extract_first()
            if not self.img_regex.match(temp_url):
                continue
            img_urls.append(temp_url)
            img_types.append(os.path.basename(temp_url))
            print("Added image: ", temp_url)

        # for large main images inside tabs (usually for units with multiple rarity)
        for img in response.css('div.tabbertab > p img'):
            temp_url = protocol + "//" + domain + img.css('::attr(src)').extract_first()
            if not self.img_regex.match(temp_url):
                continue
            img_urls.append(temp_url)
            img_types.append(os.path.basename(temp_url))
            print("Added image: ", temp_url)

        # for the mini images in infobox
        for infobox in response.css('table.infobox'):
            infobox_title = infobox.css('caption::text').get()
            idx = 0
            for img in infobox.css('img'):

                # get only the first two images (almost guaranteed to be the icon and animation gif)
                if idx < 2:
                    temp_url = protocol + "//" + domain + img.css('::attr(src)').extract_first()
                    if not self.img_regex.match(temp_url):
                        continue
                    img_urls.append(temp_url)
                    img_types.append(os.path.basename(temp_url))
                    print("Added image: ", temp_url)
                else:
                    break
                idx+=1
        
        print("============================== End of parse for URL: " + response.url + "\n")

        item["file_urls"] = img_urls
        item["file_types"] = img_types
        item["title"] = title
        item["domain_url"] = domain

        return item
