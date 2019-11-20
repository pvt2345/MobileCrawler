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
                request = scrapy.Request(url=next_url, callback=self.parse_list_item)
                request.meta['brand'] = brand
                yield request


    def parse_list_item(self, response):
        for item in response.css('div.makers li'):
            if item is not None:
                next_url = item.css('a::attr(href)').extract_first()
                next_url = self.domain + self.gsm_domain + next_url
                request = scrapy.Request(url=next_url, callback=self.parse_item)
                request.meta['brand'] = response.meta['brand']
                yield request
        if response.css('a.pages-next::attr(href)').extract_first() != '#1':
            next_page = response.css('a.pages-next::attr(href)').extract_first()
            next_page = self.domain + self.gsm_domain + next_page
            yield scrapy.Request(url=next_page, callback=self.parse_list_item)

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
                        article['color'] = ele.css('td.nfo::text').extract_first().split(",")
                    if ele.css('td.ttl a::text').extract_first() == 'Internal':
                        s = ele.css('td.nfo::text').extract_first().split(",")
                        info_ram = []
                        info_storage = []
                        info_rom = []
                        if 'ROM' not in s[1]:
                            for i in range(len(s)):
                                info_memory = s[i].split()
                                info_ram.append(info_memory[1])
                                info_storage.append(info_memory[0])
                            article['ram'] = info_ram
                            article['storage'] = info_storage
                        else:
                            for i in range(len(s)):
                                info_memory = s[i].split()
                                info_ram.append(info_memory[1])
                                info_rom.append(info_memory[0])
                            article['ram'] = info_ram
                            article['storage'] = info_rom
                    if ele.css('td.ttl a::text').extract_first() == 'Type':
                        article['screen'] = ele.css('td.nfo::text').extract_first()
                    if ele.css('td.ttl a::text').extract_first() == 'Size':
                        article['screen_size'] = ele.css('td.nfo::text').extract_first()
                    if ele.css('td.ttl a::text').extract_first() == 'SIM':
                        article['sim'] = ele.css('td.nfo::text').extract_first()
                    if ele.css('td.ttl a::text').extract_first() == 'OS':
                        article['os'] = ele.css('td.nfo::text').extract_first()
                        
                    main_camera = response.css('td.nfo[data-spec="cam1modules"]::text').extract()
                    main_camera = [item.strip() for item in main_camera]
                    article['behind_camera'] = main_camera

                    selfie_camera = response.css('td.nfo[data-spec="cam2modules"]::text').extract()
                    selfie_camera = [item.strip() for item in selfie_camera]
                    article['front_camera'] = selfie_camera


            yield article

        except:
            error_url = response.url
            yield {'error_url ': error_url}
