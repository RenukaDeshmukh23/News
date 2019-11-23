# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['newsroom.accenture.com']
    start_urls = ['https://newsroom.accenture.com//']


    def parse(self, response):
        Url=response.xpath('//h4//a/@href').extract()
        for absolute_Url in Url:
            absolute_Url=response.urljoin(absolute_Url)
            yield Request(absolute_Url,callback=self.parse_details)

        next_page_url = response.xpath('//*[@class="next "]//a/@href').extract_first()
        if next_page_url:
            yield Request(response.urljoin(next_page_url), callback=self.parse_details)

    def parse_details(self,response):
        date=response.xpath('//*[@class="rel-date"]/text()').extract_first()
        title= response.xpath('//strong/text()').extract_first()
        #content= response.xpath('//*[@id="content-details"]//following-sibling::br//text()').extract()
        content=response.xpath('//*[@id="content-details"]/div[1]//text()').extract()

        #while "\n" in content: content.remove("\n")


        yield{ 'date':date,
                'title':title,
                'content':content
            }
