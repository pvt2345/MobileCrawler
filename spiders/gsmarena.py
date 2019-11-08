import scrapy


class Mobiles(scrapy.Spider):
    name = 'gsmarena'
    start_urls = ['http://webcache.googleusercontent.com/search?q=cache:https://www.gsmarena.com/']
    domain = 'http://webcache.googleusercontent.com/search?q=cache:'
    gsm_domain = 'https://www.gsmarena.com/'

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_brand)


    def parse_brand(self, response):
        for item in response.css('div.brandmenu-v2 li'):
            if item is not None:
                next_url = item.css('a::attr(href)').extract_first()
                next_url = self.domain + self.gsm_domain + next_url
                brand = item.css('a::text').extract_first()
    #             next_page = response.urljoin(next_url)
                request = scrapy.Request(url=next_url, callback=self.parse_item)
                request.meta['brand'] = brand
                yield request

    def parse_item(self, response):
        try:
            article = {}
            article['brand'] = response.meta['brand']
            article['name'] = response.css('h1.specs-phone-name-title::text').extract_first()
            for item in response.css('div#specs-list table'):
                for ele in item.css('tr'):
                    if ele.css('td.ttl a::text').extract_first() == 'Models':
                        article['models'] = ele.css('td.nfo::text').extract_first()
                    if ele.css('td.ttl a::text').extract_first() == 'Colors':
                        article['models'] = ele.css('td.nfo::text').extract_first()
                    if ele.css('td.ttl a::text').extract_first() == 'Internal':
                        s = ele.css('td.nfo::text').extract_first().split(",")
                        info_ram = []
                        info_storage = []
                        for i in range(len(s)):
                            info_memory = s[i].split()
                            info_ram.append(info_memory[1])
                            info_storage.append(info_memory[0])
                        article['ram'] = info_ram
                        article['storage'] = info_memory
                    if ele.css('td.ttl a::text').extract_first() == 'Type':
                        article['screen'] = ele.css('td.nfo::text').extract_first()
                    if ele.css('td.ttl a::text').extract_first() == 'Size':
                        article['screen_size'] = ele.css('td.nfo::text').extract_first()
                    if ele.css('td.ttl a::text').extract_first() == 'SIM':
                        article['sim'] = ele.css('td.nfo::text').extract_first()
                    if ele.css('td.ttl a::text').extract_first() == 'OS':
                        article['os'] = ele.css('td.nfo::text').extract_first()
            yield article

        except:
            error_url = response.url
            yield {'error_url ': error_url}
