# -*- coding: utf-8 -*-
import scrapy

class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    author_affiliations = scrapy.Field()
    abstract = scrapy.Field()
    full_text = scrapy.Field()
    journal_name = scrapy.Field()
    journal_issn = scrapy.Field()
