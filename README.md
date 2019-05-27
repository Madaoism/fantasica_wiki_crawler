# Fantasica Wiki crawler
### Use this crawler to get all the unit images on www.fantasicawiki.com
## Instructions
* To use this program, make sure you have installed python, scrapy, and all its dependencies
  * You can find a tutorial on how to install scrapy here: http://doc.scrapy.org/en/latest/intro/install.html
* IMPORTANT: Open fantasica_wiki_crawler/settings.py, and change FILES_STORE to whichever path you want to set to
* When you are ready, open up a console/terminal, go to the fantasica_wiki_crawler folder, and type in the following command
  * scrapy crawl fantasica_wiki
* It will take a while (depending on your internet speed, might take hours) to crawl through all the unit pages, so please be patient. Meanwhile, you can find your images popping up at the FILES_STORE directory that you specified
## Modifications
* To change the filters and URLs crawled, go to fantasica_wiki_crawler/spiders/fantasica_wiki.py and modify the spider. 
  * If you want to crawl through all webpages in the domain instead of just the units, set custom_settings = { 'DEPTH_LIMIT': 0 }
* To change your output file names, go to fantasica_wiki_crawler/pipelines.py and modify item_completed. 
  * The easiest way is to modify new_fulldir and new_fullpath in the for loop, as they will be the paths to the new file 
