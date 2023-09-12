# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GetemoticonsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pages = scrapy.Field()
    title = scrapy.Field()
    img_url = scrapy.Field()
    img_date = scrapy.Field()
    img_info = scrapy.Field()
    extract_date = scrapy.Field()
