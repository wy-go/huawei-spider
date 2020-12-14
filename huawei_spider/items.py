# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HuaweiSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    detail = scrapy.Field()
    intro = scrapy.Field()
    img = scrapy.Field()

