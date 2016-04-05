# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
import json
import thread
import sys

from conf import website
from utils.Stock import Stock
from utils import Static
from utils import Reminder
from utils import Monitor

reload(sys)
sys.setdefaultencoding('utf-8')

# Create your views here.

name_dict = Static.name_dict
buy_stable_dict = Static.buy_stable_dict
buy_unstable_dict = Static.buy_unstable_dict


def buy(request):
    for code in buy_stable_dict.keys():
        stock = Stock(code, True)
        thread.start_new_thread(Monitor.buyMonitor, (stock,))
    for code in buy_unstable_dict.keys():
        stock = Stock(code, False)
        thread.start_new_thread(Monitor.buyMonitor, (stock,))

    return render(request, website.buy)


def test(request):
    max_price = 59.20
    code = '002594'
    Reminder.deadline_master(code, max_price)
    return render(request, website.test)


def setBuyMonitor(request):
    return render(request, website.setBuyMonitor)


def startBuyMonitor(request):
    code = request.POST['code']
    isstable = int(request.POST['isstable'])

    if isstable == 1:
        isStable = True
    else:
        isStable = False

    Static.set_buy_dict(code, True)

    stock = Stock(code, isStable)
    thread.start_new_thread(Monitor.buyMonitor, (stock,))

    return HttpResponse(json.dumps({'state': 'SUCCESS'}))


def setSellMonitor(request):
    return render(request, website.setSellMonitor)


def startSellMonitor(request):
    code = request.POST['code']
    buyprice = float(request.POST['buyprice'])
    todaystart = int(request.POST['todaystart'])
    isstable = int(request.POST['isstable'])

    if isstable == 1:
        isStable = True
    else:
        isStable = False

    Static.set_sell_dict(code, True)

    stock = Stock(code, isStable)
    thread.start_new_thread(Monitor.sellMonitor, (buyprice, stock, todaystart))

    return HttpResponse(json.dumps({'state': 'SUCCESS'}))


def setDeadlineMonitor(request):
    return render(request, website.setDeadlineMonitor)


def startDeadlineMonitor(request):
    code = request.POST['code']
    buyprice = float(request.POST['buyprice'])
    isstable = int(request.POST['isstable'])

    if isstable == 1:
        isStable = True
    else:
        isStable = False

    Static.set_sell_dict(code, True)

    stock = Stock(code, isStable)
    thread.start_new_thread(Monitor.deadlineMonitor, (stock, buyprice))

    return HttpResponse(json.dumps({'state': 'SUCCESS'}))


def stopBuyStock(request):
    code = request.GET['code']
    Static.set_buy_dict(code, False)
    return render(request, website.test)


def stopSellStock(request):
    code = request.GET['code']
    Static.set_sell_dict(code, False)
    return render(request, website.test)
