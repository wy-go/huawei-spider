# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import codecs
import json
import os

from itemadapter import ItemAdapter

from scrapy.exporters import JsonLinesItemExporter


class HuaweiSpiderPipeline(object):
    def __init__(self):
        self.fp = codecs.open("huawei.json", "w+", encoding='UTF-8')

    def open_spider(self, spider):
        self.fp.write('[\n')
        print('huawei_spider started...')

    def process_item(self, item, spider):
        item_json = json.dumps(dict(item), ensure_ascii=False)
        self.fp.write('\t' + item_json + ',\n')
        return item

    def close_spider(self, spider):
        self.fp.seek(-2, os.SEEK_END)
        # 使用 truncate() 方法，将后面的数据清空
        self.fp.truncate()
        # 重新输出'\n'，并输出']'，与 open_spider(self, spider) 时输出的 '[' 相对应，构成一个完整的数组格式
        self.fp.write('\n]')
        self.fp.close()
        print('huawei_spider stopped...')