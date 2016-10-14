# Scrapy settings for dirbot project

SPIDER_MODULES = ['dirbot.spiders']
NEWSPIDER_MODULE = 'dirbot.spiders'
DEFAULT_ITEM_CLASS = 'dirbot.items.SecondHouse'

#ITEM_PIPELINES = {'dirbot.pipelines.FilterWordsPipeline': 1}
ITEM_PIPELINES = ['dirbot.mysqlpipelines.MySQLStorePipeline']
FEED_EXPORTERS = {
    'csv': 'dirbot.my_project_csv_item_exporter.MyProjectCsvItemExporter',
}
##LOG_LEVEL = 'INFO'
##LOG_ENCODING = 'utf-8'
##LOG_FILE = 'ljsechouse.log'

FIELDS_TO_EXPORT = [
    'dataid',
    'city',
    'district',
    'title',
    'zonename',
    'housetype',
    'square',
    'direction',
    'remark',
    'subway',
    'taxfree',
    'education',
    'totalprice',
    'perprice',
    'review'
]

CSV_DELIMITER = '^'
