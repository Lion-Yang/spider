# coding:utf-8
"""
The main function to start the crawl process
"""
import os
from configure import get_configure
from crawl import BaiduCrawler
from __util__.library import get_keys


class FileNotExistException(Exception):

    def __init__(self, s):
        self.s = s

    def __str__(self):
        return repr(self.s)


if __name__ == '__main__':
    [input_file, output_file, threads, base_url, pattern] = get_configure()    # get the basic configuration
    if not os.path.exists(input_file):    # judge if the input file exists
        raise FileNotExistException("The input file {} didn't exist, better give the absolute path".format(input_file))
    keys = get_keys(input_file, output_file)    # get the key words from the input file
    crawl = BaiduCrawler(keys, base_url, pattern, output_file, threads)    # create a BaiduCrawler class
    crawl.start()    # start crawling







