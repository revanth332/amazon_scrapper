import scrapy
import pandas as pd
from ..items import AmazonScraperItem

class AmazonSpider(scrapy.Spider):
    name = 'amazon_spider'
    # start_urls = ['https://www.amazon.in/s?k=bags&page=2&crid=2M096C61O4MLT&qid=1697623398&sprefix=ba%2Caps%2C283&ref=sr_pg_2']
    start_urls = ['https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1',
                  'https://www.amazon.in/s?k=bags&page=2&crid=2M096C61O4MLT&qid=1697623398&sprefix=ba%2Caps%2C283&ref=sr_pg_2',
                  'https://www.amazon.in/s?k=bags&page=3&crid=2M096C61O4MLT&qid=1697623406&sprefix=ba%2Caps%2C283&ref=sr_pg_3',
                  'https://www.amazon.in/s?k=bags&page=4&crid=2M096C61O4MLT&qid=1697623436&sprefix=ba%2Caps%2C283&ref=sr_pg_4',
                  'https://www.amazon.in/s?k=bags&page=5&crid=2M096C61O4MLT&qid=1697623482&sprefix=ba%2Caps%2C283&ref=sr_pg_5',
                  'https://www.amazon.in/s?k=bags&page=6&crid=2M096C61O4MLT&qid=1697623509&sprefix=ba%2Caps%2C283&ref=sr_pg_6',
                  'https://www.amazon.in/s?k=bags&page=7&crid=2M096C61O4MLT&qid=1697623531&sprefix=ba%2Caps%2C283&ref=sr_pg_7',
                  'https://www.amazon.in/s?k=bags&page=8&crid=2M096C61O4MLT&qid=1697623552&sprefix=ba%2Caps%2C283&ref=sr_pg_8',
                  'https://www.amazon.in/s?k=bags&page=9&crid=2M096C61O4MLT&qid=1697623580&sprefix=ba%2Caps%2C283&ref=sr_pg_9',
                  'https://www.amazon.in/s?k=bags&page=10&crid=2M096C61O4MLT&qid=1697623594&sprefix=ba%2Caps%2C283&ref=sr_pg_10',
                  'https://www.amazon.in/s?k=bags&page=11&crid=2M096C61O4MLT&qid=1697635592&sprefix=ba%2Caps%2C283&ref=sr_pg_11',
                  'https://www.amazon.in/s?k=bags&page=12&crid=2M096C61O4MLT&qid=1697642507&sprefix=ba%2Caps%2C283&ref=sr_pg_12',
                  'https://www.amazon.in/s?k=bags&page=13&crid=2M096C61O4MLT&qid=1697642528&sprefix=ba%2Caps%2C283&ref=sr_pg_13'
                  ]

    def parse(self, response):
        for product in response.xpath('//div[contains(@class, "sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16")]'):
            url = product.xpath('.//a[contains(@class,"a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")]/@href').get(default='')
            url = 'https://www.amazon.in'+url
            title = product.xpath('.//span[contains(@class, "a-size-medium a-color-base a-text-normal")]/text()').get(default='')
            rating = product.xpath('.//span[contains(@class, "a-icon-alt")]/text()').get(default='')
            price = product.xpath('.//span[contains(@class, "a-price-whole")]/text()').get(default='')
            reviews = product.xpath('.//span[contains(@class, "a-size-base s-underline-text")]/text()').get(default='')
            yield scrapy.Request(url, callback=self.parse_product,meta={
                'url':url,
                'title': title,
                'rating': rating,
                'price': price,
                'reviews': reviews,
            })

    def parse_product(self, response):
      items = AmazonScraperItem()
      url = response.url
      title = response.meta['title']
      rating = response.meta['rating']
      price = response.meta['price']
      reviews = response.meta['reviews']
      asin = response.xpath('//ul[@class="a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list"]/li[4]/span/span[2]/text()').get(default='')
      product_description = response.xpath('//div[@id="productDescription"]/p/span/text()').get(default='')
      manufacturer = response.xpath('//ul[@class="a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list"]/li[8]/span/span[2]/text()').get(default='')
      if asin == '':
          asin = response.xpath('//*[(@id = "productDetails_detailBullets_sections1")]//tr[(((count(preceding-sibling::*) + 1) = 1) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "prodDetAttrValue", " " ))]/text()').get(default='')
      if manufacturer =='':
          manufacturer = response.xpath('//tr[(((count(preceding-sibling::*) + 1) = 2) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "prodDetAttrValue", " " ))]/text()').get(default='')
      if product_description == '':
          product_description = response.xpath('//*[(@id = "aplus")]//p/text()').get(default='')
        
      items['Product_url'] = url
      items['Name'] = title
      items['Price'] = price
      items['Rating'] = rating
      items['Reviews'] = reviews
      items['ASIN']= asin
      items['Product_description']= product_description
      items['Manufacturer']= manufacturer

      yield items

# command to run spider and save in excel sheet
# scrapy crawl amazon_spider -o data2.csv