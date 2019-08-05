import scrapy
from ..items import *

class QuoteSpider(scrapy.Spider):
    name = 'quotes1'
    number = 2
    start_urls = [
            'http://quotes.toscrape.com/page/1/'
            ]

    def parse( self, response ):

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

        # next_page = response.css('li.next a::attr(href)').get() #get the attribute of link to next page
        # if next_page is not None: #after page 10, no css.next
        #     yield response.follow(next_page, callback = self.parse) #follow the next_page href,
        #     # callback the self def of parse

        next_page = 'http://quotes.toscrape.com/page/' + str(QuoteSpider.number) + '/'
        if QuoteSpider.number < 11:
            QuoteSpider.number += 1
            yield response.follow(next_page, callback = self.parse)