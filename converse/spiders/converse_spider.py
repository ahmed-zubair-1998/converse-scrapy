import scrapy

class ConverseSpider(scrapy.Spider):
    name = "converse"

    def start_requests(self):
        url = "https://www.converse.ca"
        yield scrapy.Request(url, self.parse_helper)

    def parse(self, response):
        items = response.css("div.category-products ul li")
        urls = items.css("div.product-info h2 a::attr(href)").extract()
        for url in urls:
            yield scrapy.Request(url, self.description_parser)

        link = response.xpath(r"//link[@rel='next']")[0]
        url = link.css("link::attr(href)").extract_first()
        if url:
            yield scrapy.Request(url, self.parse)

    def description_parser(self, response):
        name = response.css("div.product-name h1::text").extract_first()
        price = response.css("div.product-name span.price::text").extract_first()
        description = response.css("div#product-description p::text").extract_first()
        yield {
            'name': name.strip(),
            'price': price.strip(),
            'description': description.strip(),
        }

    def parse_helper(self, response):
        urls = []
        nav = response.css("nav#nav ol li")
        links = nav.css("a::attr(href)").extract()
        for url in links:
            if ("all-sneakers" in url) or ("all-clothing" in url):
                urls.append(url)
        urls = set(urls)
        for url in urls:
            if "/sale/" not in url:
                yield scrapy.Request(url, self.parse)
