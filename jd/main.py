# coding:utf-8
import socket
import sys
import os
from __util__.library import get_keys, create_thread
from __spider__.spider import jd_search
socket.setdefaulttimeout(20)
reload(sys)
sys.setdefaultencoding('utf-8')


if __name__ == '__main__':
    os.system('chmod +x ./__util__/double.sh;./__util__/double.sh ./__file__/jd.txt;mv du.txt ./__file__')
    keys = get_keys()
    create_thread(5, jd_search, keys)
    os.system('rm ./__file__/du.txt')
