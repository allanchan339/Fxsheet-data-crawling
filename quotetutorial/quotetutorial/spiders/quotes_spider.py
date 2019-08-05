import scrapy
from ..items import *
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser

class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    number = 2
    start_urls = [
            'http://quotes.toscrape.com/login'
            ]

    def parse( self, response ):
        token = response.css('form input::attr(value)').extract_first()
        return FormRequest.from_response(response,formdata = {
                'csrf_token' : token,
                'username': 'abc',
                'password': 'abcd'
                }, callback = self.start_scraping)

    def start_scraping (self, response):
        open_in_browser(response)
        items = QuotetutorialItem()

        all_div_quotes = response.css('div.quote')

        for quote in all_div_quotes:
            title = quote.css('span.text::text').extract()
            author = quote.css('.author::text').extract()  # span can be omitted
            tag = quote.css('.tag::text').extract()

            items['title'] = title
            items['author'] = author
            items['tag'] = tag

            yield items
         #to get csrf token
        # next_page = response.css('li.next a::attr(href)').get() #get the attribute of link to next page
        # if next_page is not None: #after page 10, no css.next
        #     yield response.follow(next_page, callback = self.parse) #follow the next_page href,
        #     # callback the self def of parse

