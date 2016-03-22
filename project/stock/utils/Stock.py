# -*- coding:utf-8 -*-
import urllib2
import re
import datetime

class Stock:
    def __init__(self, code):
        self.code = code

    def getUrlByCode(self, code):
        """根据代码获取详细的url"""
        url = ''
        stockCode = ''
        if code == 'sh':
            url = 'http://hq.sinajs.cn/list=s_sh000001'
        elif code == 'sz':
            url = 'http://hq.sinajs.cn/list=s_sz399001'
        elif code == 'cyb':
            url = 'http://hq.sinajs.cn/list=s_sz399006'
        else:
            pattern = re.compile(r'^60*')
            match = pattern.match(code)
            if match:
                stockCode = 'sh'+ code
            else:
                stockCode = 'sz' + code
            url = 'http://hq.sinajs.cn/list=s_' + stockCode

        return url

    def getStockInfo(self, url):
        """根据url获取信息"""
        stockList = []
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        stockStr = response.read()
        stockList = stockStr.split(',')
        return stockList

    def getValueList(self):
        url = self.getUrlByCode(self.code)
        infoList = self.getStockInfo(url)
        return infoList

    def getShIndex(self):
        code = 'sh'
        url = self.getUrlByCode(code)
        infoList = self.getStockInfo(url)
        return infoList[1]
