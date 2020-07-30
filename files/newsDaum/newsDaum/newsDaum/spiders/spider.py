import scrapy
from newsDaum.items import NewsdaumItem
# from selenium import webdriver
from scrapy.http import TextResponse
import requests

class DaumSpider(scrapy.Spider):
    name = "NewsDaum"
    allow_domain = ["https://daum.net"]
    start_urls = ["https://news.daum.net/breakingnews/economic"]
    
    def parse(self, response):
        categories = ['society', 'politics', 'economic', 'foreign', 'culture', 'entertain', 'sports', 'digital']
        for name in categories:
            for page in range(1, 100):
                url = "https://news.daum.net/breakingnews/{}?page={}".format(name, page)
                req = requests.get(url)
                response = TextResponse(req.url, body=req.text, encoding="utf-8")
                links  = response.xpath('//*[@id="mArticle"]/div[3]/ul/li/div/strong/a/@href').extract()
                for link in links:
                    yield scrapy.Request(link, callback=self.parse_content)
            
    def parse_content(self, response):
        item = NewsdaumItem()
        item['title'] = response.xpath('//*[@id="cSub"]/div/h3')[0].extract().split(">")[1].split("<")[0]
        item['category'] = response.xpath('//*[@id="kakaoBody"]')[0].extract().split(">")[1].split("<")[0]
        content = response.xpath('//*[@id="harmonyContainer"]/section/p/text()').extract()
        item['content'] = "".join(content)
        item['link'] = response.url
        yield item
