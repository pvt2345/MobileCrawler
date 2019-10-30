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
        article = {}
        keys = response.css('div.fs-tsright li label::text').extract()
        texts = response.css('div.fs-tsright li span::text').extract()
        article['Model: '] = response.css('div.f-wrap ul.fs-breadcrumb li.active::text').extract()
        article['Hãng: '] = response.css('div.f-wrap ul.fs-breadcrumb a::text').extract()[2].strip()
        article['Giá: '] = response.xpath('/html/body/section/div/div[1]/div[2]/div[2]/div[1]/p/text()').extract()[
            0].strip()
        for i in range(len(keys)):
            article[keys[i]] = texts[i]
        csv_columns = ['Model', 'Hãng', 'Giá', 'Màn hình', 'Camera trước', 'Camera sau', 'RAM', 'Bộ nhớ trong', 'CPU',
                       'GPU', 'Dung lương pin', 'Hệ điều hành', 'Thẻ sim']
        csv_file = "Mobile.csv"
        try:
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames= csv_columns)
                writer.writeheader()
                for data in article:
                    writer.writerow(data)
        except IOError:
            print("I/O error")
