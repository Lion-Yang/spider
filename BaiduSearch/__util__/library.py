# coding:utf-8
"""
Some necessary small functions
"""
import threadpool
import time
import os
import socket
from selenium import webdriver
socket.setdefaulttimeout(30)


def get_cookie():
    """
    get browser cookie when the access is denied
    :return: a new browser cookie
    """
    browser = webdriver.PhantomJS(executable_path='./resource/phantomjs')
    browser.get('https://www.baidu.com')
    time.sleep(1)
    cookies = browser.get_cookies()[0]
    cookie = ''
    for key, data in cookies.items():
        cookie += str(key)+'='+str(data)+';'
    cookie = cookie[:-1]
    browser.quit()
    return cookie


def handle_keys(key):
    """
    handle the keyword to eliminate redundant words
    :param key: the keyword
    :return: cleaned keyword
    """
    keys = key.split()
    keys[1] = keys[1].replace("常见", "").replace("中华", "").replace("大全", "").\
        replace("名称", "").replace("分类", "").replace("个别", "")
    return keys


def create_thread(num, target, args):
    """
    function to create multiple threads
    :param num: number of threads
    :param target: target function
    :param args: arguments to be processed
    :return: none
    """
    args_list = []
    l = len(args)
    for i in range(num):
        args_list.append(args[(l / num) * i:(l / num) * (i + 1)])
    pool = threadpool.ThreadPool(num)
    request = threadpool.makeRequests(target, args_list)
    [pool.putRequest(req) for req in request]
    pool.wait()


def get_keys(input_file, output_file):
    """
    get keywords from the input file
    :param input_file: path of the input file
    :param output_file: path of the output file
    :return: keywords
    """
    if not os.path.exists(output_file):
        with open(input_file, 'rb') as f:
            keys = [each.strip() for each in f.readlines()]
        return keys
    else:
        with open(input_file, 'rb') as f1:
            with open(output_file, 'rb') as f2:
                keys1 = [each.strip() for each in f1.readlines()]
                keys2 = [each.strip('\t').split()[0] for each in f2.readlines()]
                keys = [each for each in keys1 if each.split('\t')[0] not in keys2]
        return keys
