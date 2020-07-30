import scrapy

class NewsnateItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    category = scrapy.Field()
    summary = scrapy.Field()    
    link = scrapy.Field()
