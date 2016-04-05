# -*- coding:utf-8 -*-
import sys
from ShortMessage import ShortMessage
import Static

reload(sys)
sys.setdefaultencoding('utf-8')

name_dict = Static.name_dict
buystocklogger = Static.buystocklogger
sellstocklogger = Static.sellstocklogger
remindlogger = Static.remindlogger


def warn_master(code, line, flag):
    message = ''
    message += u'您所关注的股票代码【'
    message += name_dict[code] + code
    if flag == 0:
        message += u'】累计已下跌【'
    else:
        message += u'】累计已上涨【'
    message += str(line * 100)
    message += u'】%，请及时关注。'

    phone = '13148499085'
    short_message = ShortMessage(message, phone)
    return_dict = short_message.send()

    return_mess = name_dict[code] + code + u'股票警告:返回值为' + return_dict['code'] + u',状态为' + return_dict['msg']
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
    message += name_dict[code] + code
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

    phone = '18657106966'
    short_message = ShortMessage(message, phone)
    return_dict = short_message.send()

    return_mess = name_dict[code] + code + u'股票提醒:返回值为' + return_dict['code'] + u',状态为' + return_dict['msg']
    remindlogger.info(return_mess)


def deadline_master(code, buy_price):
    message = ''
    message += u'您所买入的【'
    message += name_dict[code] + code
    message += u'】公司股价为【'
    message += str(buy_price)
    message += u'】，已经持仓超过5天，现在已达到抛出标准，建议立即抛出。'

    phone = '13148436656'
    short_message = ShortMessage(message, phone)
    return_dict = short_message.send()

    return_mess = name_dict[code] + code + u'股票期限到达提醒:返回值为' + return_dict['code'] + u',状态为' + return_dict['msg']
    remindlogger.info(return_mess)
