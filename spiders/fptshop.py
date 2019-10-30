import scrapy


class fptshop(scrapy.Spider):
    name = 'fptshop'
    start_urls = ['https://fptshop.com.vn/dien-thoai/apple-iphone']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for item in response.css('div.fs-lpil a.fs-lpil-img::attr(href)').getall():
            if item is not None:
                next_page = response.urljoin(item)
                yield scrapy.Request(url=next_page, callback=self.parse_item)


    def parse_item(self, response):
        print(response.css('div.fs-dtt-col1 h1.fs-dttname::text').extract())
        print(response.xpath('/html/body/section/div/div[1]/div[2]/div[2]/div[1]/p/text()').extract()[0].strip())
        article = {}
        keys = response.css('div.fs-tsright li label::text').extract()
        texts = response.css('div.fs-tsright li span::text').extract()
        for i in range(len(keys)):
            article[keys[i]] = texts[i]
        for key, text in article.items():
            print("{key} {text}".format(key=key.upper(), text=text))


