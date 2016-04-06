# -*- coding:utf-8 -*-
import sys
import time
import datetime
import Static
import Reminder

reload(sys)
sys.setdefaultencoding('utf-8')

MAX_PRICE = Static.MAX_PRICE
MIN_PRICE = Static.MIN_PRICE

buystocklogger = Static.buystocklogger
sellstocklogger = Static.sellstocklogger
remindlogger = Static.remindlogger

name_dict = Static.name_dict


def stock_price_init(stock):
    value_list = stock.getValueList()
    share_price = float(value_list[1]) - float(value_list[2])
    return share_price


def buyMonitor(stock):
    min_price = MIN_PRICE
    max_price = MAX_PRICE

    code = stock.code
    dropline = stock.limit.first_drop.line
    rollbackline = stock.limit.first_drop.rollbackline

    max_price = stock_price_init(stock)

    buystocklogger.info(u'开始监控待买入股票:' + name_dict[code] + code)
    buystocklogger.info(name_dict[code] + code + '股票的开盘价格为:' + str(max_price))

    warn_flag = 0
    remind_flag = 0
    while Static.buy_dict[code]:
        value_list = stock.getValueList()
        if not value_list:
            continue
        share_price = float(value_list[1])
        # buystocklogger.info(name_dict[code] + code + u'股票的价格为:' +  str(share_price))

        if share_price > max_price:
            max_price = share_price
            min_price = MIN_PRICE
        if share_price < min_price:
            min_price = share_price

        drop_percent = (max_price - min_price) / max_price
        if drop_percent > dropline:
            if warn_flag == 0:
                Reminder.warn_master(code, dropline, 0)
                stock_mess = name_dict[code] + code + u':当前股价为' + str(share_price) + u',股价最大值为' + str(max_price)
                buystocklogger.info(stock_mess)
                warn_flag = 1
            if drop_percent > stock.limit.second_drop.line:
                dropline = stock.limit.second_drop.line
                rollbackline = stock.limit.second_drop.rollbackline
            if drop_percent > stock.limit.third_drop.line:
                dropline = stock.limit.third_drop.line
                rollbackline = stock.limit.third_drop.rollbackline
            remind_flag = 1

        if remind_flag == 1:
            if (share_price - min_price) / min_price > rollbackline:
                Reminder.remind_master(max_price, min_price, value_list, code, 0)
                max_price = MAX_PRICE
                min_price = MIN_PRICE
                dropline = stock.limit.first_drop.line
                rollbackline = stock.limit.first_drop.rollbackline
                remind_flag = 0
                warn_flag = 0

        time.sleep(15)


def deadlineMonitor(stock, buy_price):
    code = stock.code

    deadline = 0.02
    riseline = 0.01
    rollbackline = 0.002

    max_price = MAX_PRICE

    sellstocklogger.info(name_dict[code] + code + u':已买入5天，开始监视')

    remind_flag = 0
    while Static.sell_dict[code]:
        share_price = float(stock.getValueList()[1])

        if (share_price - buy_price) / buy_price > deadline:
            Reminder.deadline_master(code, share_price)
            break

        if share_price > max_price:
            max_price = share_price

        if (max_price - buy_price) / buy_price > riseline:
            remind_flag = 1

        if remind_flag == 1:
            if (max_price - share_price) / max_price > rollbackline:
                Reminder.deadline_master(code, share_price)
                break

        time.sleep(15)


def sellMonitor(stock, buy_price, todaystart):
    now_date = datetime.datetime.now()
    deadline = now_date + datetime.timedelta(days=5)

    if todaystart == 0:
        roll_seconds = (1 * 60 + 30) + 24 * 60 - (now_date.hour * 60 + now_date.minute)
        time.sleep(roll_seconds)

    max_price = MAX_PRICE
    code = stock.code
    riseline = stock.limit.first_rise.line
    rollbackline = stock.limit.first_rise.rollbackline

    sellstocklogger.info(u'开始监控待卖出股票:' + name_dict[code] + code)

    warn_flag = 0
    remind_flag = 0

    while Static.sell_dict[code]:
        now = datetime.datetime.now()
        if now > deadline:
            deadlineMonitor(stock, buy_price)
            break

        value_list = stock.getValueList()
        share_price = float(value_list[1])
        # sellstocklogger.info(name_dict[code] + code + '股票的价格为:' + str(share_price))

        if share_price > max_price:
            max_price = share_price

        rise_percent = (max_price - buy_price) / buy_price
        if rise_percent > riseline:
            if warn_flag == 0:
                Reminder.warn_master(code, riseline, 1)
                stock_mess = name_dict[code] + code + u':当前股价为' + str(share_price) + u',买入价格为' + str(buy_price)
                buystocklogger.info(stock_mess)
                warn_flag = 1
            if rise_percent > stock.limit.second_rise.line:
                riseline = stock.limit.second_rise.line
                rollbackline = stock.limit.second_rise.rollbackline
            if rise_percent > stock.limit.third_rise.line:
                riseline = stock.limit.third_rise.line
                rollbackline = stock.limit.third_rise.rollbackline
            if rise_percent > stock.limit.forth_rise.line:
                riseline = stock.limit.forth_rise.line
                rollbackline = stock.limit.forth_rise.rollbackline
            remind_flag = 1

        if remind_flag == 1:
            if (max_price - share_price) / max_price > rollbackline:
                Reminder.remind_master(buy_price, max_price, value_list, code, 1)
                break

        time.sleep(15)


def threadMonitor(threadList, flag):
    while True:
        for thread in threadList:
            if not thread.isAlive():
                if flag == 0:
                    buystocklogger.info(u'线程' + name_dict[thread.name] + thread.name + u'已经停止运行')
                else:
                    sellstocklogger.info(u'线程' + name_dict[thread.name] + thread.name + u'已经停止运行')
                threadList.remove(thread)
        time.sleep(15)
