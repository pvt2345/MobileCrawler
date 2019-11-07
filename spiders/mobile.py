import scrapy, csv


class Mobile(scrapy.Spider):
    name = 'mobile'
    start_urls = ['https://fptshop.com.vn/dien-thoai']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for item in response.css('div.item a.filter-brand::attr(href)').extract():
            if item is not None:
                next_page = response.urljoin(item)
                yield scrapy.Request(url=next_page, callback=self.parse_link)

    def parse_link(self, response):
        for item in response.css('div.fs-lpil a.fs-lpil-img::attr(href)').extract():
            if item is not None:
                next_page = response.urljoin(item)
                yield scrapy.Request(url=next_page, callback=self.parse_item)

    def parse_item(self, response):
        try:
            article = {}
            article['name'] = response.css('div.f-wrap ul.fs-breadcrumb li.active::text').extract_first()
            article['brand'] = response.css('div.f-wrap ul.fs-breadcrumb a::text').extract()[2].strip()
            try:
                price  = response.xpath('/html/body/section/div/div[1]/div[2]/div[2]/div[1]/p/text()').extract()[0].strip()
                article['price'] = int(price.replace('.',''))
            except:
                price = response.xpath('/html/body/section/div/div[1]/div[2]/div[2]/div[1]/ul/li[2]/label/span/strong/text()').extract_first()[:-1]
                article['price'] = int(price.replace('.', ''))

            for item in response.css('div.fs-tsright li'):
                if (item.css('label::text').extract_first() == 'Màn hình :'):
                    article['screen'] = item.css('span::text').extract_first()
                if (item.css('label::text').extract_first() == 'Camera trước :'):
                    article['front_camera'] = item.css('span::text').extract_first()
                if (item.css('label::text').extract_first() == 'Camera sau :'):
                    article['behind_camera'] = item.css('span::text').extract_first()
                if (item.css('label::text').extract_first() == 'RAM :'):
                    article['ram'] = item.css('span::text').extract_first()
                if (item.css('label::text').extract_first() == 'Bộ nhớ trong :'):
                    article['storage'] = item.css('span::text').extract_first()
                if (item.css('label::text').extract_first() == 'CPU :'):
                    article['CPU'] = item.css('span::text').extract_first()
                if (item.css('label::text').extract_first() == 'GPU :'):
                    article['GPU'] = item.css('span::text').extract_first()
                if (item.css('label::text').extract_first() == 'Dung lượng pin :'):
                    article['battery'] = item.css('span::text').extract_first()
                if (item.css('label::text').extract_first() == 'Hệ điều hành :'):
                    article['OS'] = item.css('span::text').extract_first()
                if (item.css('label::text').extract_first() == 'Thẻ SIM :'):
                    article['SIM'] = item.css('span::text').extract_first()


            yield article
        except:
            error_url = response.url
            yield {'error_url' : error_url}

