# coding:utf-8
import os
import threadpool
import re
import socket
import sys
import urllib
import time
from retrying import retry
from __configure__.ConfigureParser import ConfigureParser
socket.setdefaulttimeout(20)
reload(sys)
sys.setdefaultencoding('utf-8')


def create_thread(num, target, args):
    args_list = []
    l = len(args)
    for i in range(num):
        args_list.append(args[(l / num) * i:(l / num) * (i + 1)])
    pool = threadpool.ThreadPool(num)
    request = threadpool.makeRequests(target, args_list)
    [pool.putRequest(req) for req in request]
    pool.wait()
    time.sleep(30)


@retry
def get_html(key):
    url = 'http://search.jd.com/Search?keyword={}&enc=utf-8'.format(key)
    req = urllib.urlopen(url)
    return req.read()


def num_trans(s):
    trans_pattern = {u'\d+$': lambda x: int(x),
                     u'\d+(?:\.\d+)?万': lambda x: int(float(re.findall(u'\d+(?:\.\d+)?', x)[0])*10000)}
    for key, data in trans_pattern.items():
        if re.match(key, s):
            return data(s)


def handle_type(key):
    with open('./__file__/du.txt', 'r') as f:
        du = [each.strip() for each in f.readlines()]
    cut = key.split('\t')
    cut[-1] = cut[-1].replace(u'3C数码配件市场', u'数码配件').replace('brand', '').replace(u'词表', '').replace(u'副本', '')\
    .replace(u'电子词典文化用品', u'文化用品').replace(u'常见', '').replace(u' 家装饰品窗帘地毯', u'家装饰品')
    if cut[0] in du:
        return cut[0] + ' '+cut[1]
    return cut[0]


def get_keys():
    conf = ConfigureParser('./__configure__/configure.xml')
    input_file = conf.get_configure_by_tag_name('input_file')
    output_file = conf.get_configure_by_tag_name('output_file')
    if not os.path.exists(output_file):
        with open(input_file, 'rb') as f:
            keys = [each.strip() for each in f.readlines()]
        return keys
    else:
        with open(input_file, 'rb') as f1:
            with open(output_file, 'rb') as f2:
                keys1 = [each.strip() for each in f1.readlines()]
                keys2 = [each.strip().rsplit('\t', 1)[0] for each in f2.readlines()]
                keys = [each for each in keys1 if each not in keys2]
        return keys
