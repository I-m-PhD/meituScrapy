# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MeituRankDiyItem(scrapy.Item):
    # define the fields for your item here like:
    model_name = scrapy.Field()
    model_score = scrapy.Field()
    album_head = scrapy.Field()
    img_url = scrapy.Field()
