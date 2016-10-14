import sys
import string
import MySQLdb
import hashlib
import time
from scrapy.exceptions import DropItem
from scrapy.http import Request
import logging

logger = logging.getLogger()
reload(sys)
sys.setdefaultencoding('utf8')

class MySQLStorePipeline(object):

    # put all words in lowercase
    # words_to_filter = ['\u671f\u8d27','\u91d1\u8475\u82b1','\u6668\u4f1a']
    
    def __init__(self):
        self.conn = MySQLdb.connect(host="127.0.0.1", user="test", passwd="test", db="test", charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()
        self.now = time.strftime('%Y-%m-%d %H:%M:%S')

    def process_item(self, item, spider):
        try:
            #print "Step 1: insert"
            logger.info("Step 1: insert")
            if not item['education']:
                #logger.info("-----------> education is empty")
                item['education'] = ['NA']
            if not item['subway']:
                #logger.info("-----------> subway is empty")
                item['subway'] = ['NA']
            if not item['taxfree']:
                #logger.info("-----------> taxfree is empty")
                item['taxfree'] = ['NA']
            self.cursor.execute("""INSERT INTO tbl_ljsechouse (dataid, city, district, title,
                                zonename, housetype, square, direction, remark, subway, taxfree,
                                education, totalprice, perprice, review, ins_dt)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                                (item['dataid'], item['city'], item['district'], item['title'], item['zonename'],
                                 item['housetype'], item['square'], item['direction'], item['remark'], item['subway'],
                                 item['taxfree'], item['education'], item['totalprice'], item['perprice'], item['review'],
                                 self.now))
            self.conn.commit()
        except MySQLdb.Error, e:
            #print "Error %d: %s" % (e.args[0], e.args[1])
            logger.error("Error %d: %s" %(e.args[0], e.args[1]))
            #print "item is [ %s ]" % item
            logger.info("item is [ %s ]" ,item)
            #print "Step 2: query duplicate"
            logger.info("Step 2: query duplicate")
            self.cursor.execute("SELECT is_upd FROM tbl_ljsechouse WHERE dataid=%s", (item['dataid']))
            is_upd = self.cursor.fetchone()
            #print "before is tuple"
            if type(is_upd) is tuple:
                #print "Step 2.1: pass type validation and is_upd=%s " %(is_upd[0])
                if int(is_upd[0]) > 0:
                    #print "Step 3: come in"
                    try:
                        self.cursor.execute("""UPDATE tbl_ljsechouse SET is_upd=is_upd+1,totalprice=%s, perprice=%s, review=%s, upd_dt=%s WHERE dataid=%s""",
                                        (item['totalprice'], item['perprice'], item['review'], self.now, item['dataid']))
                        self.conn.commit()
                    except MySQLdb.Error, e2:
                        print "Step 4: error unknown"
                        #print "Error %d: %s" % (e2.args[0], e2.args[1])
                        logger.error("Error %d: %s" %(e2.args[0], e2.args[1]))

        return item
