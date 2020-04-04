# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

class SubjectsSpider(scrapy.Spider):
    name = 'subjects'
    allowed_domains = ['classcentral.com']
    start_urls = ['http://classcentral.com/subjects']

    def __init__(self,subject = None):
        self.subject = subject

    def parse(self, response):
        if self.subject:
            # subject_url = response.xpath('//*[@class="border-box align-middle padding-right-xsmall"]/@href').extract_first()
            subject_url = response.xpath('//*[contains(@title,"' + self.subject+'")]/@href').extract_first()
            yield Request(response.urljoin(subject_url),callback = self.parse_subject)
        else:
            self.logger.info("Scrapping all subjects")
            subjects = response.xpath('//*[@class="border-box align-middle padding-right-xsmall"]/@href').extract()
            for subject in subjects:
                yield Request(response.urljoin(subject),callback=self.parse_subject)
    def parse_subject(self,response):
        subject_name = response.xpath("//*[@class='head-1']/text()").extract_first()
        cources = response.xpath('//*[@class="color-charcoal block line-tight course-name"]')
        for cource in cources:
            cource_url = cource.xpath('.//@href').extract_first()
            cource_name = cource.xpath('.//@title').extract_first()
            absolute_cource_url = response.urljoin(cource_url)
            yield {
            'Subject_name':subject_name,
            'Cource_name':cource_name,
            'Cource_url':absolute_cource_url
            }
        next_page = response.xpath('//*[@rel="next"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page)
        yield Request(absolute_next_page_url, callback=self.parse_subject)
