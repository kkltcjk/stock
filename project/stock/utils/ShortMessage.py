# -*- coding: utf-8 -*-
import urllib
import urllib2
import sys
import time
from stock.utils.CParser import CParser


SERVICE_URL = 'http://106.ihuyi.cn/webservice/sms.php?method=Submit'

reload(sys)
sys.setdefaultencoding('utf-8')

send_flag = True


class ShortMessage:
    def __init__(self, message, phone):
        self.user = 'cf_gaominquan'
        self.password = 'miffy31415926'
        self.touser = phone
        self.message = message

    def send(self):
        global send_flag
        data = {
            'account': self.user,
            'password': self.password,
            'mobile': self.touser,
            'content': self.message
        }

        try:
            while send_flag is False:
                time.sleep(1)
            send_flag = False

            encoding_data = urllib.urlencode(data)
            req = urllib2.Request(url=SERVICE_URL, data=encoding_data)
            res = urllib2.urlopen(req)

            time.sleep(1)
            send_flag = True

            result = res.read()
            parser = CParser()
            parser.feed(result)

            dict = parser.dict
            parser.close()
            return dict
        except Exception as e:
            print e
