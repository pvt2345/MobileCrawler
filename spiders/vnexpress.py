# -*- coding: utf8 -*-
import scrapy


class VnexpressNet(scrapy.Spider):
    name = "vnexpress"

    def start_requests(self):
        urls = ['https://vnexpress.net/du-lich/viet-nam-huong-den-bau-troi-mo-asean-4001184.html']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_artilce)

    def parse_artilce(self, response):
        artilce = {}
        artilce['title'] = response.xpath('//*[@id="col_sticky"]/h1/text()').extract()[0].strip()
        artilce['description'] = response.xpath('//*[@id="col_sticky"]/p[1]').extract()[0].strip()
        artilce['content'] = response.xpath('//*[@id="col_sticky"]/article').extract()[0].strip()
        artilce['author'] = response.xpath('//*[@id="col_sticky"]/p[2]/strong/text()').extract()[0].strip()
        artilce['publish_date'] = response.xpath('//*[@id="col_sticky"]/header/span/text()').extract()[0].strip()
        for key, text in artilce.items():
            print("{key}: {text}".format(key=key.upper(), text=text))

