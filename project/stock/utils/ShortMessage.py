# -*- coding: utf-8 -*-
import urllib
import urllib2
import cookielib
import sys

SERVICE_URL = 'http://106.ihuyi.cn/webservice/sms.php?method=Submit'

reload(sys)
sys.setdefaultencoding('utf-8')

class ShortMessage:
    def __init__(self, message):
        self.user = 'cf_gaominquan'
        self.password = 'miffy31415926'
        self.touser = '18657106966'
        self.message = message

    def send(self):
        data = {
            'account': self.user,
            'password': self.password,
            'mobile': self.touser,
            'content': self.message
        }

        try:
            encoding_data = urllib.urlencode(data)
            req = urllib2.Request(url = SERVICE_URL, data = encoding_data)
            res = urllib2.urlopen(req)
            result = res.read()
            print result
        except Exception as e:
            print e

