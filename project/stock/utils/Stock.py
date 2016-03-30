# -*- coding:utf-8 -*-
import urllib2
import re
import datetime

class StockLimit:
    def __init__(self, line, rollbackline):
        self.line = line
        self.rollbackline = rollbackline

first_drop = StockLimit(0.04, 0.005)
second_drop = StockLimit(0.05, 0.01)
third_drop = StockLimit(0.08, 0.02)
first_rise = StockLimit(0.03, 0.003)
second_rise = StockLimit(0.04, 0.005)
third_rise = StockLimit(0.05, 0.01)
forth_rise = StockLimit(0.08, 0.02)

class Stock:
    def __init__(self, code, fd = first_drop, sd = second_drop, td = third_drop, fr = first_rise, sr = second_rise, tr = third_rise, fhr = forth_rise):
        self.code = code
        self.first_drop = fd
        self.second_drop = sd
        self.third_drop = td
        self.first_rise = fr
        self.second_rise = sr
        self.third_rise = tr
        self.forth_rise = fhr

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
