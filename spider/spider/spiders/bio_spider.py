# -*- coding: utf-8 -*-
from spider.items import ArticleItem
from datetime import datetime
import scrapy
import PyPDF2
import io

def log(message):
    with open('data/log.txt', 'a') as f:
        f.write('\n[%s] %s' % (str(datetime.now()), message))

class QuotesSpider(scrapy.Spider):
    name = "bio"

    def start_requests(self):
        urls = [
            'http://bioline.org.br/titles?id=md&year=2016&vol=19&num=01&keys=V19N1',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        log('updating (%s)' % response.url)

        urls = response.css('li a::attr(href)').extract()
        titles_ = response.xpath('//a[@id="bold"]')
        authors = response.css('span.TOCAuthor::text').extract()

        paper_title = response.css('font.paperTitle::text').extract_first()
        journal_issn = response.css('font.paperISSN font.paperISSN::text').extract_first()

        for i in range(len(urls)):
            url = response.urljoin(urls[i])
            title = ''.join(titles_[i].xpath('.//text()').extract()).strip()
            author = authors[i]

            item = ArticleItem()
            item['title'] = title
            item['author'] = author
            item['journal_name'] = paper_title
            item['journal_issn'] = journal_issn

            request = scrapy.Request(url, callback=self.parse_article)
            request.meta['item'] = item
            yield request

    def parse_article(self, response):
        item = response.meta['item']
        parts_ = response.xpath('//div[@class="AbstractText"]')
        abstract = ''.join(parts_[0].xpath('.//text()').extract())

        item['abstract'] = abstract
        item['full_text'] = ''

        pdf_urls = response.css('a::attr(href)').re('/pdf.+')
        if len(pdf_urls) > 0:
            pdf_url = pdf_urls[0]
            pdf_url = response.urljoin(pdf_url)

            request = scrapy.Request(pdf_url, callback=self.parse_pdf_article)
            request.meta['item'] = item
            yield request

        else:
            yield item

    def _pdf_to_text(self, file_like_object):
        read_pdf = PyPDF2.PdfFileReader(file_like_object)
        number_of_pages = read_pdf.getNumPages()
        result = ''
        for i in range(number_of_pages):
            page = read_pdf.getPage(0)
            page_content = page.extractText()
            result += page_content.strip().replace('\n', '') + '\n\n'
        return result

    def parse_pdf_article(self, response):
        item = response.meta['item']
        full_text = self._pdf_to_text(io.BytesIO(response.body))
        item['full_text'] = response.url + '\t' + full_text
        yield item






