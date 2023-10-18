# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonScraperItem(scrapy.Item):
    # define the fields for your item here like:
    Product_url = scrapy.Field()
    Name = scrapy.Field()
    Price = scrapy.Field()
    Rating = scrapy.Field()
    Reviews = scrapy.Field()
    ASIN = scrapy.Field()
    Product_description = scrapy.Field()
    Manufacturer = scrapy.Field()
    
