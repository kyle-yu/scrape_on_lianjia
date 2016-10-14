import unicodedata
import string
import urllib2
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import HtmlResponse
from lxml import etree
import re

"""
http://sh.lianjia.com/ershoufang/jingan/
http://sh.lianjia.com/ershoufang/xuhui/
http://sh.lianjia.com/ershoufang/huangpu/
http://sh.lianjia.com/ershoufang/changning/
http://sh.lianjia.com/ershoufang/putuo/
http://sh.lianjia.com/ershoufang/pudongxinqu/
http://sh.lianjia.com/ershoufang/baoshan/
http://sh.lianjia.com/ershoufang/zhabei/
http://sh.lianjia.com/ershoufang/hongkou/
http://sh.lianjia.com/ershoufang/yangpu/
http://sh.lianjia.com/ershoufang/minhang/
http://sh.lianjia.com/ershoufang/jinshan/
http://sh.lianjia.com/ershoufang/jiading/
http://sh.lianjia.com/ershoufang/chongming/
http://sh.lianjia.com/ershoufang/fengxian/
http://sh.lianjia.com/ershoufang/songjiang/
http://sh.lianjia.com/ershoufang/qingpu/
http://sh.lianjia.com/ershoufang/shanghaizhoubian/

Xpath manual & detail:
http://www.cnblogs.com/ChengDong/archive/2012/06/28/2567744.html
"""
from dirbot.items import SecondHouse

def fn_text(self, str):
    dr = re.compile(r'<[^>]+>',re.S)
    dd = dr.sub('',str)
    return dd

class LJSecHouseSpider(Spider):
    name = "ljsechouse"
    district = 'xuhui'
    city = 'Shanghai'
    
    download_delay = 0.5
    allowed_domains = ["http://sh.fang.lianjia.com"]
    homeurl = 'http://sh.lianjia.com/ershoufang/' + district + '/'
    print homeurl
    response = urllib2.urlopen(homeurl)
    html = response.read()
    tree = etree.HTML(html)
    #/div/div[2]/div/a[4]/text()
    nodes = tree.xpath('//*[@mod-id="lj-ershoufang-list"]/div/div[2]/div/@page-data')
    #print len(nodes)
    #print nodes
    totalPage = 0
    for node in nodes:
        #print node
        pgdata = '%s' % node
        pgdata = pgdata.split(':',1)[1]
        pgdata = pgdata.split(',')[0]
        #print pgdata
        totalPage = int(pgdata) + 1
    #totalPage = 2
    print totalPage

    url = 'http://sh.lianjia.com/ershoufang/' + district + '/pg$/'
    #print url
    start_urls = []
    for num in range(1, totalPage):
        tmpstr = url.replace('$',('%d' %num))
        #print tmpstr
        start_urls.append(tmpstr)

    print tmpstr

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//*[@id="house-lst"]/li')
        items = []

        for site in sites:
            item = SecondHouse()

            dr = re.compile(r'<[^>]+>',re.S)
            item['dataid'] = site.xpath('@data-id').extract()
            #//*[@id="house-lst"]/li[1]/div[2]/h2/a
            item['title'] = site.xpath('div[2]/h2/a/text()').extract()

			#//*[@id="house-lst"]/li[1]/div[2]/div[1]/div[1]/a/span
            item['zonename'] = string.join(site.xpath('div[2]/div[1]/div[1]/a/span/text()').extract()).strip()

            #//*[@id="house-lst"]/li[1]/div[2]/div[1]/div[1]/span[1]/span
            #housetype = string.join(site.xpath('div[2]/div[1]/div[2]').extract())
            #item['housetype'] = dr.sub('',housetype).strip()
            item['housetype'] = string.join(site.xpath('div[2]/div[1]/div[1]/span[1]/span/text()').extract()).strip()
            
            #//*[@id="house-lst"]/li[1]/div[2]/div[1]/div[1]/span[2]
            item['square'] = string.join(site.xpath('div[2]/div[1]/div[1]/span[2]/text()').extract()).strip()

            #//*[@id="house-lst"]/li[1]/div[2]/div[1]/div[1]/span[3]
            item['direction'] = string.join(site.xpath('div[2]/div[1]/div[1]/span[3]/text()').extract()).strip()

            #//*[@id="house-lst"]/li[1]/div[2]/div[1]/div[2]/div
            remark = string.join(site.xpath('div[2]/div[1]/div[2]/div').extract())
            item['remark'] = dr.sub('',remark).strip()

            #//*[@id="house-lst"]/li[2]/div[2]/div[1]/div[3]/div/div/span[@class="fang-subway-ex"]/span
            item['subway'] = site.xpath('div[2]/div[1]/div[3]/div/div/span[@class="fang-subway-ex"]/span/text()').extract()

            #//*[@id="house-lst"]/li[2]/div[2]/div[1]/div[3]/div/div/span[@class="taxfree-ex"]/span
            item['taxfree'] = site.xpath('div[2]/div[1]/div[3]/div/div/span[@class="taxfree-ex"]/span/text()').extract()

            #//*[@id="house-lst"]/li[2]/div[2]/div[1]/div[3]/div/div/span[@class="fang05-ex"]/span
            item['education'] = site.xpath('div[2]/div[1]/div[3]/div/div/span[@class="fang05-ex"]/span/text()').extract()

            #//*[@id="house-lst"]/li[2]/div[2]/div[2]/div[1]/span
            item['totalprice'] = site.xpath('div[2]/div[2]/div[1]/span/text()').extract()

            #//*[@id="house-lst"]/li[2]/div[2]/div[2]/div[2]
            item['perprice'] = site.xpath('div[2]/div[2]/div[2]/text()').extract()

            #//*[@id="house-lst"]/li[2]/div[2]/div[3]/div/div[1]/span
            item['review'] = site.xpath('div[2]/div[3]/div/div[1]/span/text()').extract()

            item['city'] = self.city
            item['district'] = self.district
            
            items.append(item)

        return items


