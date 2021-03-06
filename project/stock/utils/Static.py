# -*- coding:utf-8 -*-
import logging

MAX_PRICE = 0.01
MIN_PRICE = 1000.00

buystocklogger = logging.getLogger('buystock')
sellstocklogger = logging.getLogger('sellstock')
remindlogger = logging.getLogger('remind')

name_dict = {
    '002594': u'比亚迪',
    '601633': u'长城汽车',
    '000625': u'长安汽车',
    '600104': u'上汽集团',
    '000572': u'海马汽车',
    '601519': u'大智慧',
    '000776': u'广发证券',
    '600999': u'招商证券',
    '600030': u'中信证券',
    '600664': u'哈药股份',
    '603998': u'方盛制药',
    '002287': u'奇正藏药',
    '600717': u'天津港',
    '601018': u'宁波港',
    '601880': u'大连港',
    '002343': u'慈文传媒',
    '000156': u'华数传媒',
    '002095': u'生意宝',
    '600246': u'万通地产',
    '600639': u'浦东金桥',
    '002192': u'融捷股份',
    '002284': u'亚太股份',
    '002236': u'大华股份',
    '000333': u'美的集团',
    '601919': u'中国远洋',
    '600021': u'上海电力',
    '600116': u'三峡水利',
    '002279': u'久其软件',
    '600718': u'东软集团',
    '601601': u'中国太保',
    '601318': u'中国平安',
    '601628': u'中国人寿',
    '000416': u'民生控股',
    '600029': u'南方航空',
    '600115': u'东方航空',
    '601111': u'中国国航',
    '600893': u'中航动力',
    '600316': u'洪都航空',
    '000738': u'中航动控',
    '000807': u'云铝股份',
    '002378': u'章源钨业',
    '600549': u'厦门钨业',
    '000998': u'隆平高科',
    '600598': u'北大荒',
    '600161': u'天坛生物',
    '002007': u'华兰生物',
    '600566': u'济川药业',
    '002603': u'以岭药业',
    '002038': u'双鹭药业',
    '000929': u'兰州黄河',
    '000858': u'五粮液',
    '002415': u'海康威视',
    '000839': u'中信国安',
    '002460': u'赣锋锂业',
    '300014': u'亿纬锂能',
    '002407': u'多氟多',
    '002249': u'大洋电机',
    '000559': u'万向钱潮',
    '600522': u'中天科技',
    '600570': u'恒生电子'
}

buy_stable_dict = {
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
    '600246': True,
    '002236': True,
    '000333': True,
    '601919': True,
    '600021': True
}

buy_unstable_dict = {
    '600717': True,
    '601018': True,
    '601880': True,
    '002343': True,
    '000156': True,
    '002095': True,
    '600639': True,
    '002284': True,
    '002279': True,
    '600718': True,
    '603998': True,
    '002192': True,
    '601601': True,
    '601318': True,
    '601628': True,
    '000416': True,
    '600029': True,
    '600115': True,
    '601111': True,
    '600893': True,
    '600316': True,
    '000738': True,
    '000807': True,
    '002378': True,
    '600549': True,
    '000998': True,
    '600598': True,
    '600161': True,
    '002007': True,
    '600566': True,
    '002603': True,
    '002038': True,
    '000929': True,
    '000858': True,
    '002415': True,
    '000839': True,
    '002460': True,
    '300014': True,
    '002407': True,
    '002249': True,
    '000559': True,
    '600522': True,
    '600570': True
}

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
    '600717': True,
    '601018': True,
    '601880': True,
    '002343': True,
    '000156': True,
    '002095': True,
    '600246': True,
    '600639': True,
    '002192': True,
    '002284': True,
    '002236': True,
    '000333': True,
    '601919': True,
    '600021': True,
    '002279': True,
    '600718': True,
    '601601': True,
    '601318': True,
    '601628': True,
    '000416': True,
    '600029': True,
    '600115': True,
    '601111': True,
    '600893': True,
    '600316': True,
    '000738': True,
    '000807': True,
    '002378': True,
    '600549': True,
    '000998': True,
    '600598': True,
    '600161': True,
    '002007': True,
    '600566': True,
    '002603': True,
    '002038': True,
    '000929': True,
    '000858': True,
    '002415': True,
    '000839': True,
    '002460': True,
    '300014': True,
    '002407': True,
    '002249': True,
    '000559': True,
    '600522': True,
    '600570': True
}

sell_dict = {}


def set_buy_dict(code, value):
    global buy_dict
    buy_dict[code] = value


def set_sell_dict(code, value):
    global sell_dict
    sell_dict[code] = value
