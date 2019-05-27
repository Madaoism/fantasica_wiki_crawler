# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings
import os
from io import BytesIO
from pprint import pprint
import hashlib


class FantasicaWikiCrawlerPipeline(FilesPipeline):

    def item_completed(self, results, item, info):
        print ("\n=========================================== Start of item_completed")

        file_paths = []

        settings = get_project_settings()
        storage = settings.get('FILES_STORE')

        for idx, result in enumerate(results):
            responded, info = result
            if 'path' not in info:
                print("Does not have path: ", info)
                continue

            # old name
            old_fullpath = os.path.join(storage, info['path'])
            extension = os.path.splitext(old_fullpath)[-1]

            # new name
            basename = os.path.splitext(item['file_types'][idx])[0] + extension
            dirname = item['title']
            new_fullpath = os.path.join(storage, dirname, basename)
            new_fulldir = os.path.join(storage, dirname)
            
            # create dir if it does not exist
            if not os.path.exists(new_fulldir):
                os.makedirs(new_fulldir)
                print("created directory: ", new_fulldir)

            # remove old image file if same exists
            if os.path.exists(new_fullpath):
                print ("removed old file: ", new_fullpath)
                os.remove(new_fullpath)
            
            # rename to the new file
            if not os.path.exists(new_fullpath):
                os.rename(old_fullpath, new_fullpath)
                print ("renamed to :" + new_fullpath)            
                file_paths.append(new_fullpath)
            else:
                print ("Unable to rename file from " + old_fullpath + " to " + new_fullpath)
                file_paths.append(old_fullpath)

        print ("=========================================== End of item_completed", "\n")
        item['file_paths'] = file_paths
        return item

    # def file_path(self, request, response=None, info=None):
    #     print("===============> def file_path: ", request, response, info)
    #     image_guid = hashlib.sha1(to_bytes(url)).hexdigest()  # change to request.url after deprecation
    #     return 'full/%s.jpg' % (image_guid)