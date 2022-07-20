# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import datetime

from itemadapter import ItemAdapter

import csv


class GetjobPipeline:
    fp = None
    csv_writer = None

    def open_spider(self, spider):
        print("开始爬取。。。")
        self.fp = open("./job58_data.csv", "w", encoding="utf-8-sig", newline="")
        self.csv_writer = csv.writer(self.fp)
        # 写入表头
        header = ['infoId', 'detail_url', 'pos_title', 'pos_name', 'pos_salary', 'pos_edu', 'pos_year', 'work_city',
                  'detail_address', 'pos_welfare', 'pos_num', 'company_name', 'company_category', 'company_scale',
                  'userId', 'userName', 'identity', 'state', 'visitors', 'apply', 'updateTime']

        self.csv_writer.writerow(header)

    def process_item(self, item, spider):
        try:
            # 处理 work_city
            item['work_city'] = "-".join(item['work_city'])
            # 处理 pos_welfare
            item['pos_welfare'] = "-".join(item['pos_welfare'])
            # 处理 updateTime
            if item['updateTime'][0].replace(" ", "") == "今天":
                item['updateTime'] = datetime.date.today()

            data = [item['infoId'], item['detail_url'], item['pos_title'], item['pos_name'], item['pos_salary'],
                    item['pos_edu'], item['pos_year'], item['work_city'],
                    item['detail_address'], item['pos_welfare'], item['pos_num'], item['company_name'],
                    item['company_category'], item['company_scale'],
                    item['userId'], item['userName'], item['identity'], item['state'], item['visitors'], item['apply'],
                    item['updateTime']]
            print(data)
            self.csv_writer.writerow(data)
        except Exception as ex:
            print(ex)

    def close_spider(self, spider):
        self.fp.close()
        print("爬取完成")
