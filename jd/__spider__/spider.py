# coding:utf-8
import socket
import sys
from scrapy import Selector
from __configure__.ConfigureParser import ConfigureParser
from __util__.library import get_html, handle_type, num_trans
socket.setdefaulttimeout(20)
reload(sys)
sys.setdefaultencoding('utf-8')


def jd_search(keys):
    conf = ConfigureParser('./__configure__/configure.xml')
    output_file = conf.get_configure_by_tag_name('output_file')
    xpath = conf.get_configure_by_tag_name('xpath')
    for key in keys:
        source = get_html(handle_type(key))
        try:
            sel = Selector(text=source).xpath(xpath)
            num = str(num_trans(sel.extract()[0]))
        except:
            num = '0'
        print handle_type(key), num
        with open(output_file, 'ab') as f:
            f.write(key+'\t'+num+'\n')