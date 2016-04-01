# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
import json
import thread
import time
import datetime
import sys
import logging

from conf import website
from utils.ShortMessage import ShortMessage
from utils.Stock import Stock
from utils.Stock import StockLimit

reload(sys)
sys.setdefaultencoding('utf-8')

# Create your views here.

buystocklogger = logging.getLogger('buystock')
sellstocklogger = logging.getLogger('sellstock')
remindlogger = logging.getLogger('remind')

MAX_PRICE = 0.01
MIN_PRICE = 1000.00

DROP_LINE = 0.04
RISE_LINE = 0.03
ROLLBACK_LINE = 0.005

buy_dict = {
    '002594': True,
    '601633': True,
    '000625': True,
    '600104': True,
    '000572': True,
    '601519': True,
    '000776': True,
    '600999': True,
    '600030': True,
    '600664': True,
    '603998': True,
    '002287': True,
    '600717': True,
    '601018': True,
    '601880': True,
    '002343': True,
    '000156': True,
    '002095': True,
    '600246': True,
    '600639': True,
    '002192': True,
    '002284': True
}

sell_dict = {
    '002594': False,
    '601633': False,
    '601519': False,
    '300033': False,
    '601211': False,
    '600999': False,
    '600030': False,
    '000776': False
}

def buy(request):
    for code in buy_dict.keys():
        stock = Stock(code)
        thread.start_new_thread(buyMonitor, (stock,))
    return render(request, website.buy)

def test(request):
    max_price = 59.20
    min_price = 56.31
    code = '002594'
    stock = Stock(code)
    print stock.forth_rise.line
    #value_list = stock.getValueList()
    # remind_master(max_price, min_price, value_list, code, 0)
    #time.sleep(5)
    # warn_master(code, DROP_LINE, 0)
    return render(request, website.test)

def stock_price_init(stock):
    value_list = stock.getValueList()
    share_price = float(value_list[1]) - float(value_list[2])
    return share_price

def buyMonitor(stock):
    min_price = MIN_PRICE
    max_price = MAX_PRICE

    code = stock.code
    dropline = stock.first_drop.line
    rollbackline = stock.first_drop.rollbackline

    max_price = stock_price_init(stock)
    buystocklogger.info(code + '股票的开盘价格为:' + str(max_price))

    warn_flag = 0
    remind_flag = 0
    while buy_dict[code]:
        value_list = stock.getValueList()
        share_price = float(value_list[1])
        buystocklogger.info(code + u'股票的价格为:' +  str(share_price))

        if share_price > max_price:
            max_price = share_price
            min_price = MIN_PRICE
        if share_price < min_price:
            min_price = share_price

        drop_percent = (max_price - min_price) / max_price
        if drop_percent > dropline:
            if warn_flag == 0:
                warn_master(code, dropline, 0)
                warn_flag = 1
            if drop_percent > stock.second_drop.line:
                dropline = stock.second_drop.line
                rollbackline = stock.second_drop.rollbackline
            if drop_percent > stock.third_drop.line:
                dropline = stock.third_drop.line
                rollbackline = stock.third_drop.rollbackline
            remind_flag = 1

        if remind_flag == 1:
            if (share_price - min_price) / min_price > rollbackline:
                remind_master(max_price, min_price, value_list, code, 0)
                max_price = MAX_PRICE
                min_price = MIN_PRICE
                dropline = stock.first_drop.line
                rollbackline = stock.first_drop.rollbackline
                remind_flag = 0
                warn_flag = 0

        time.sleep(15)

def sellMonitor(buy_price, stock, todaystart):
    if todaystart == '0':
        now_date = datetime.datetime.now()
        roll_seconds = (9 * 60 + 30) + 24 * 60 - (now_date.hour * 60 + now_date.minute)
        time.sleep(roll_seconds)

    max_price = MAX_PRICE
    code = stock.code
    riseline = stock.first_rise.line
    rollbackline = stock.first_rise.rollbackline

    warn_flag = 0
    remind_flag = 0

    while sell_dict[code]:
        value_list = stock.getValueList()
        share_price = float(value_list[1])
        sellstocklogger.info(code + '股票的价格为:' + str(share_price))

        if share_price > max_price:
            max_price = share_price

        rise_percent = (max_price - buy_price) / buy_price
        if rise_percent > riseline:
            if warn_flag == 0:
                warn_master(code, riseline, 1)
                warn_flag = 1
            if rise_percent > stock.second_rise.line:
                riseline = stock.second_rise.line
                rollbackline = stock.second_rise.rollbackline
            if rise_percent > stock.third_rise.line:
                riseline = stock.third_rise.line
                rollbackline = stock.third_rise.rollbackline
            if rise_percent > stock.forth_rise.line:
                riseline = stock.forth_rise.line
                rollbackline = stock.forth_rise.rollbackline
            remind_flag = 1

        if remind_flag == 1:
            if (max_price - share_price) / max_price > rollbackline:
                remind_master(buy_price, max_price, value_list, code, 1)

        time.sleep(15)

def warn_master(code, line, flag):
    message = ''
    message += u'您所关注的股票代码【'
    message += code
    if flag == 0:
        message += u'】累计已下跌【'
    else:
        message += u'】累计已上涨【'
    message += str(line * 100)
    message += u'】%，请及时关注。'

    short_message = ShortMessage(message)
    return_dict = short_message.send()

    return_mess = code + u'股票警告:返回值为' + return_dict['code'] + u',状态为' + return_dict['msg']
    remindlogger.info(return_mess)

def remind_master(first_price, second_price, value_list, code, flag):
    if flag == 0:
        first_percent = '%4.2f' % ((first_price - second_price) / first_price * 100)
        second_percent = '%4.2f' % ((float(value_list[1]) - second_price) / second_price * 100)
        float_percent = '%4.2f' % ((first_price - float(value_list[1])) / first_price * 100)
    else:
        first_percent = '%4.2f' % ((second_price - first_price) / first_price * 100)
        second_percent = '%4.2f' % ((second_price - float(value_list[1])) / second_price * 100)
        float_percent = '%4.2f' % ((float(value_list[1]) - first_price) / first_price * 100)

    message = ''
    message += u'您所关注的【'
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
        message += u'】%， 上一个最大值为【'
    else:
        message += u'】%， 您的买入价格为【'
    message += str(first_price)
    if flag == 0:
        message += u'】元，最小值为【'
    else:
        message += u'】元，最大值为【'
    message += str(second_price)
    if flag == 0:
        message += u'】元，较之前已先下跌【'
    else:
        message += u'】元，较之前已先上涨【'
    message += str(first_percent)
    if flag == 0:
        message += u'】%，后上浮【'
    else:
        message += u'】%，后下跌【'
    message += str(second_percent)
    message += u'】%，累计浮动【'
    message += str(float_percent)
    if flag == 0:
        message += u'】%，建议立即买入。'
    else:
        message += u'】%，建议立即抛出。'


    short_message = ShortMessage(message)
    return_dict = short_message.send()
    return_mess = code + u'股票提醒:返回值为' + return_dict['code'] + u',状态为' + return_dict['msg']
    remindlogger.info(return_mess)

def old_remind_master(extreme_price, value_list, code, flag):
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

    short_message = ShortMessage(message)
    return_dict = short_message.send()
    return_mess = code + u'股票提醒:返回值为' + return_dict['code'] + u',状态为' + return_dict['msg']
    remindlogger.info(return_mess)

def setBuyMonitor(request):
    return render(request, website.setBuyMonitor)

def startBuyMonitor(request):
    code = request.POST['code']
    dropline = float(request.POST['dropline'])
    rollbackline = float(request.POST['rollbackline'])

    global buy_dict
    buy_dict[code] = True

    stocklimit = StockLimit(dropline, rollbackline)
    stock = Stock(code, fd = stocklimit)
    thread.start_new_thread(buyMonitor, (stock,))

    return HttpResponse(json.dumps({'state': 'SUCCESS'}))

def setSellMonitor(request):
    return render(request, website.setSellMonitor)

def startSellMonitor(request):
    code = request.POST['code']
    buyprice = float(request.POST['buyprice'])
    riseline = float(request.POST['riseline'])
    rollbackline = float(request.POST['rollbackline'])
    todaystart = request.POST['todaystart']

    global sell_dict
    sell_dict[code] = True

    stocklimit = StockLimit(riseline, rollbackline)
    stock = Stock(code, fr = stocklimit)
    thread.start_new_thread(sellMonitor, (buyprice, stock, todaystart))

    return HttpResponse(json.dumps({'state': 'SUCCESS'}))

def stopBuyStock(request):
    code = request.GET['code']
    global buy_dict
    buy_dict[code] = False
    return render(request, website.test)

def stopSellStock(request):
    code = request.GET['code']
    global sell_dict
    sell_dict[code] = False
    return render(request, website.test)
