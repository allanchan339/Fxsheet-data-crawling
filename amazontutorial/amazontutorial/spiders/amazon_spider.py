# -*- coding: utf-8 -*-
import scrapy
from ..items import *


class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon_spider'
    page_number = 2
    start_urls = [
            'https://www.amazon.com/s?bbn=283155&rh=n%3A283155%2Cp_n_publication_date%3A1250226011&dc&fst=as%3Aoff&qid=1564824385&rnid=1250225011&ref=lp_283155_nr_p_n_publication_date_0'
            'https://www.amazon.com/s?i=stripbooks&bbn=283155&rh=n%3A283155%2Cp_n_publication_date%3A1250226011&dc&page=2&fst=as%3Aoff&qid=1564826718&rnid=1250225011&ref=sr_pg_2'
                  ]

    def parse(self, response):
        items = AmazontutorialItem()

        product_name = response.css('.a-color-base.a-text-normal::text').extract()
        product_author = response.css('.a-color-secondary .a-size-base:nth-child(2)').css('::text').extract()
        price = response.css('.a-spacing-top-small .a-price:nth-child(1) .a-price-whole').css('::text').extract()
        product_image = response.css('.s-image').css('::attr(src)').extract()
        #.getall() == .extract()

        items['product_name'] = product_name
        items['product_author'] = product_author
        items['price'] = price
        items['product_image'] = product_image

        next_page = 'https://www.amazon.com/s?i=stripbooks&bbn=283155&rh=n%3A283155%2Cp_n_publication_date' \
                    '%3A1250226011&dc&page='+ str(AmazonSpiderSpider.page_number) \
                    +'&fst=as%3Aoff&qid=1564827225&rnid=1250225011&ref=sr_pg_3'
        if AmazonSpiderSpider.page_number <= 70:
            AmazonSpiderSpider.page_number += 1
            yield response.follow(next_page, callback = self.parse)

        yield items




from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
process = CrawlerProcess(get_project_settings())

# 'followall' is the name of one of the spiders of the project.
process.crawl('amazon_spider')
process.start() # the script will block here until the crawling is finished