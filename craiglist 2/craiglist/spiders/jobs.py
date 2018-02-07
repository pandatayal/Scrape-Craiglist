# -*- coding: utf-8 -*-
import scrapy


class JobsSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = ["newyork.craigslist.org"]
    start_urls = (
        'https://newyork.craigslist.org/search/egr',
    )

    def parse(self, response):
        listings = response.xpath('//li[@class="result-row"]')
        for listing in listings:
            date = listing.xpath('.//*[@class="result-date"]/@datetime').extract_first()
            link = listing.xpath('.//a[@class="result-title hdrlnk"]/@href').extract_first()
            text = listing.xpath('.//a[@class="result-title hdrlnk"]/text()').extract_first()

            yield {'date': date,
                   'link': link,
                   'text': text}

        next_page_url = response.xpath('//a[text()="next > "]/@href').extract_first()
        if next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)
