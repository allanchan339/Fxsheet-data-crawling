# -*- coding: utf-8 -*-
import scrapy
import os
from ..items import *
from scrapy_splash import SplashRequest
from datetime import datetime


# import re


class NfpTchSpider(scrapy.Spider):
    links_global = []
    name = 'NFP_TCH'
    start_urls = [
            'https://www.fxstreet.com/economic-calendar/country/0345d08a-7068-42e0-a65f-e2c6243c4de1',
            'https://www.fxstreet.com/economic-calendar/country/f0b72088-34bb-4752-9337-c41f329c7798',
            'https://www.fxstreet.com/economic-calendar/country/652a1f9f-5ffe-42de-a53f-e30900fef5e5',
            'https://www.fxstreet.com/economic-calendar/country/89d5f89c-a5d5-40cc-8690-9725de83504d',
            'https://www.fxstreet.com/economic-calendar/country/e137f7ff-5990-4e7e-89c1-9976744a6628'
            ]
    # allowed_domains = ['https://www.fxstreet.com/economic-calendar/event/9cdf56fd-99e4-4026-aa99-2b6c0ca92811']
    # start_urls = [
    #         'https://www.fxstreet.com/economic-calendar/event/9cdf56fd-99e4-4026-aa99-2b6c0ca92811',    #1
    #         'https://www.fxstreet.com/economic-calendar/event/f3ea3723-c2de-4332-b7a5-1ba539bea3f4',    #?
    #         'https://www.fxstreet.com/economic-calendar/event/5d9ff5c8-1e0e-44b8-8d06-4ac39d217bf3',    #2
    #         'https://www.fxstreet.com/economic-calendar/event/fcfae951-09a7-449e-b6fe-525e1335aaba',    #Fed rate
    #         'https://www.fxstreet.com/economic-calendar/event/7da4ac8a-2918-4b66-a532-a6db0b6ce4fe',    #3
    #         'https://www.fxstreet.com/economic-calendar/event/f9277929-3091-4219-aa73-715d3adadb57',    #5
    #         'https://www.fxstreet.com/economic-calendar/event/9ba65d91-c2d2-4e4b-b6f3-dfe3677dc980',    #4
    #         'https://www.fxstreet.com/economic-calendar/event/2e1d69f3-8273-4096-b01b-8d2034d4fade',    #6
    #         ''
    #       ]

    # def __init__( self):
    #     #self.days = int(days)
    #     #self.pairs = ['EURUSD', 'USDJPY', 'EURGBP']
    #     self.urls = [
    #             'https://www.fxstreet.com/economic-calendar/event/9cdf56fd-99e4-4026-aa99-2b6c0ca92811']

    def start_requests( self ):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse_urls, args = {'wait': 10})

    # def start_requests( self ):
    #     for url in self.urls:
    #         yield SplashRequest(url = url, callback = self.parse, args = {'wait': 5})

    def parse_urls( self,response ):
        links = response.xpath('//*[(@id = "fxst-tablefilter-event")]//*[contains(concat( " ", @class, " " ), '
                               'concat( " ", "fxit-eventurl", " " ))]').xpath('@href').extract()
        for link in links:
            if 'https://www.fxstreet.com' not in link:
                self.links_global = response.urljoin(link)
            yield SplashRequest(self.links_global, callback = self.parse, args = {'wait': 5}) #TODO: improve the speed

    def parse( self, response):
        items = FxstreetItem()
        # name = response.css('#fxit-h1title::text').extract_first()
        # country = response.css('.fxit-countryurl::text').extract_first()
        # real = response.css('.fxst-actual-value::text').extract_first()
        # consensus = response.css('.fxst-cons-value::text').extract_first()
        # previous = response.css('.fxst-prev-value::text').extract_first()
        # next_release = response.css('.fxst-nextevent .fxst-date-value').css('::text').extract_first()

        xpaths_address = [
                '//*[(@id = "fxit-h1title")]',
                '//*[contains(concat( " ", @class, " " ), concat( " ", "fxit-countryurl", " " ))]',
                '//*[contains(concat( " ", @class, " " ), concat( " ", "fxst-actual-value", " " ))]',
                '//*[contains(concat( " ", @class, " " ), concat( " ", "fxst-cons-value", " " ))]',
                '//*[contains(concat( " ", @class, " " ), concat( " ", "fxst-prev-value", " " ))]',
                '//*[contains(concat( " ", @class, " " ), concat( " ", "fxst-nextevent", " " ))]//*[contains(concat( '
                '" ", @class, " " ), concat( " ", "fxst-date-value", " " ))]',
                '//*[contains(concat( " ", @class, " " ), concat( " ", "fxst-lastevent", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "fxst-date-value", " " ))]'
                ]
        # items = ['name','country','real','consensus','previous','next_release']

        xpaths_address_fixed = []
        for xpath_number in xpaths_address:
            xpaths_address_fixed.append('normalize-space(' + xpath_number + '/text())')

        name = response.xpath(xpaths_address_fixed[0]).extract()
        country = response.xpath(xpaths_address_fixed[1]).extract()
        real =  response.xpath(xpaths_address_fixed[2]).extract()
        consensus = response.xpath(xpaths_address_fixed[3]).extract()
        previous =  response.xpath(xpaths_address_fixed[4]).extract()
        next_release = response.xpath(xpaths_address[5] + '/text()').extract()
        date = response.xpath(xpaths_address_fixed[6]).extract()

        # for i in range(len(xpaths_address)):
        #     items[i] = response.xpath('normalize-space(').xpath(xpaths_address[i]).xpath('/text())').extract()

        items['name'] = name
        items['country'] = country
        items['real_data'] = real
        items['consensus_data'] = consensus
        items['previous_data'] = previous
        if next_release is not None: ##TODO : solve the problem of index error (no data)
            items['next_release'] = next_release[0]
            items['next_release_time'] = next_release[1]
        else:
            next_release = ['-', '-']
            items['next_release'] = next_release[0]
            items['next_release_time'] = next_release[1]

        items['date_release'] = date
        items['links'] = response.url
        yield items
