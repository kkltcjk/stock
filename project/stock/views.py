# -*- coding:utf-8 -*-
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

DROP_LINE = 0.03
RISE_LINE = 0.03
ROLLBACK_LINE = 0.005

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
        thread.start_new_thread(buyMonitor, (stock, DROP_LINE, ROLLBACK_LINE))
    return render(request, website.buy)

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

def stock_price_init(stock):
    value_list = stock.getValueList()
    share_price = float(value_list[1]) - float(value_list[2])
    return share_price

def buyMonitor(code, dropline, rollbackline):
    min_price = MIN_PRICE
    max_price = MAX_PRICE

    stock = Stock(code)

    max_price = stock_price_init(stock)
    print '待买入' + code + 'first price:' + str(max_price)

    flag = 0
    stop_mark = True
    while stop_mark:
        value_list = stock.getValueList()
        share_price = float(value_list[1])
        print '待买入' + code + ':' +  str(share_price)
        if share_price > max_price:
            max_price = share_price
            min_price = MIN_PRICE
        if share_price < min_price:
            min_price = share_price
        if (max_price - share_price) / max_price > dropline:
            flag = 1
        if flag == 1:
            if (share_price - min_price) / min_price > rollbackline:
                remind_master(max_price, value_list, code, 0)
                stop_mark = False
                max_price = MAX_PRICE
                min_price = MIN_PRICE
                flag = 0
        time.sleep(15)

def sellMonitor(buy_price, code, riseline, rollbackline):
    now_date = datetime.datetime.now()
    roll_seconds = (9 * 60 + 30) + 24 * 60 - (now_date.hour * 60 + now_date.minute)
    time.sleep(roll_seconds)

    max_price = MAX_PRICE

    stock = Stock(code)

    flag = 0
    stop_mark = True

    while stop_mark:
        value_list = stock.getValueList()
        share_price = float(value_list[1])
        print '待卖出' + code + ':' + str(share_price)
        if share_price > max_price:
            max_price = share_price
        if (max_price - buy_price) / buy_price > riseline:
            flag = 1
        if flag == 1:
            if (max_price - share_price) / max_price > rollbackline:
                remind_master(buy_price, value_list, code, 1)
                stop_mark = False
        time.sleep(15)

def remind_master(extreme_price, value_list, code, flag):
    sh_index = Stock('sh').getShIndex()
    if flag == 0:
        grand_total = '%4.2f' % ((extreme_price - float(value_list[1])) / extreme_price * 100)
    else:
        grand_total = '%4.2f' % ((float(value_list[1]) - extreme_price) / extreme_price * 100)
    message = ''
    message += u'目前上证指数为：【'
    message += str(sh_index)
    message += u'】 ,您所关注的【'
    message += code
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

def setBuyMonitor(request):
    return render(request, website.setBuyMonitor)

def startBuyMonitor(request):
    code = request.POST['code']
    dropline = float(request.POST['dropline'])
    rollbackline = float(request.POST['rollbackline'])

    thread.start_new_thread(buyMonitor, (code, dropline, rollbackline))
    return HttpResponse(json.dumps({'state': 'SUCCESS'}))

def setSellMonitor(request):
    return render(request, website.setSellMonitor)

def startSellMonitor(request):
    code = request.POST['code']
    buyprice = float(request.POST['buyprice'])
    riseline = float(request.POST['riseline'])
    rollbackline = float(request.POST['rollbackline'])

    thread.start_new_thread(sellMonitor, (buyprice, code, riseline, rollbackline))
    return HttpResponse(json.dumps({'state': 'SUCCESS'}))
