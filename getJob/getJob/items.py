# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GetjobItem(scrapy.Item):
    updateTime = scrapy.Field()
    visitors = scrapy.Field()
    apply = scrapy.Field()
    pos_title = scrapy.Field()
    pos_name = scrapy.Field()
    pos_salary = scrapy.Field()
    pos_welfare = scrapy.Field()
    pos_num = scrapy.Field()
    pos_edu = scrapy.Field()
    pos_year = scrapy.Field()
    work_city = scrapy.Field()
    detail_address = scrapy.Field()
    company_name = scrapy.Field()
    company_category = scrapy.Field()
    company_scale = scrapy.Field()
    detail_url = scrapy.Field()
    identity = scrapy.Field()
    userName = scrapy.Field()
    userId = scrapy.Field()
    state = scrapy.Field()
    infoId = scrapy.Field()

