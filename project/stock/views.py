# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
import json
import thread
import time
import datetime
import sys

from conf import website
from utils.ShortMessage import ShortMessage
from utils.Stock import Stock

reload(sys)
sys.setdefaultencoding('utf-8')

# Create your views here.

MAX_PRICE = 0.01
MIN_PRICE = 1000.00

stock_dict = {
    '002594': '比亚迪002594',
    '601633': '长城601633',
    '601519': '大智慧601519'
}

flag_dict = {
    'byd': True,
    'cc': True,
    'dzh': True
}

mapping_dict = {
    '002594': 'byd',
    '601633': 'cc',
    '601519': 'dzh'
}


def buy(request):
    for stock in stock_dict.keys():
        thread.start_new_thread(monitor, (stock,))
    return render(request, website.buy)

def monitor(code):
    min_price = MIN_PRICE
    max_price = MAX_PRICE

    stock = Stock(code)

    max_price = stock_price_init(stock)

    flag = 0
    while flag_dict[mapping_dict[code]]:
        value_list = stock.getValueList()
        share_price = float(value_list[1])
        print share_price
        if share_price > max_price:
            max_price = share_price
            min_price = 1000.00
        if share_price < min_price:
            min_price = share_price
        if (max_price - share_price) / max_price > 0.03:
            flag = 1
        if flag == 1:
            if (share_price - min_price) / min_price > 0.005:
                remind_master(max_price, value_list, code, 0)
                thread.exit_thread()
        time.sleep(15)

def stock_price_init(stock):
    value_list = stock.getValueList()
    share_price = float(value_list[1]) - float(value_list[2])
    return share_price

def remind_master(max_price, value_list, code, flag):
    sh_index = Stock('sh').getShIndex()
    grand_total = '%4.2f' % ((max_price - float(value_list[1])) / max_price * 100)
    message = ''
    message += u'目前上证指数为：【'
    message += str(sh_index)
    message += u'】 ,您所关注的【'
    message += stock_dict[code]
    message += u'】公司股价为：【'
    message += value_list[1]
    if flag == 0:
        message += u'】元，今日下跌【'
    else:
        message += u'】元，今日上涨【'
    message += value_list[2]
    message += u'】元，浮动【'
    message += value_list[3]
    if flag == 0:
        message += u'】%， 较之前累计已下跌【'
    else:
        message += u'】%， 较之前累计已上涨【'
    message += str(grand_total)
    if flag == 0:
        message += u'】%，建议立即买入。'
    else:
        message += u'】%，建议立即抛出。'
    print message

    short_message = ShortMessage(message)
    short_message.send()


def sell(request):
    max_price = 58.20
    stock = Stock('002594')
    value_list = stock.getValueList()
    remind_master(max_price, value_list, code, 0)
    return render(request, website.sell)

def stop(request):
    stock = request.GET['stock']
    if flag_dict.has_key(stock):
        flag_dict[stock] = False
