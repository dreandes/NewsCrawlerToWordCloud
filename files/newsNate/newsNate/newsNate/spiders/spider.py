import scrapy
import requests
from scrapy.http import TextResponse
from newsNate.items import NewsnateItem
from selenium import webdriver

class NateSpider(scrapy.Spider):
    name = "NewsNate"
    allow_domain = ["https://news.nate.com/"]
    start_urls = ["https://news.nate.com/section?mid=n0200"]
   
    def parse(self, response):
        for code in range(200, 700, 100):
            url = "https://news.nate.com/section?mid=n0{}".format(code)
            req = requests.get(url)
            response = TextResponse(req.url, body=req.text, encoding="utf-8")
            links = response.xpath('//*[@id="newsContents"]/div[16]/div[1]/ul/li/a/@href').extract()
            links = ["https:" + link for link in links]
            for link in links:
                yield scrapy.Request(link, callback=self.parse_content)

    def parse_content(self, response):
        item = NewsnateItem()
        title = response.xpath('//*[@id="articleView"]/h3')[0].extract().split(">")[1].split("<")[0]
        item['title'] = title.replace("\'", "")
        item['category'] = response.xpath('//*[@id="header"]/div[2]/div/ul/li[3]/a')[0].extract().split(">")[1].split("<")[0]
        summary = response.xpath('//*[@id="realArtcContents"]/b[1]/text()').extract()
        item['summary'] = "".join(summary)
        content = response.xpath('//*[@id="realArtcContents"]/text()').extract()
        item['content'] = "".join(content).strip()
        item['link'] = response.url
        yield item
