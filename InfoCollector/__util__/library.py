# -*-coding:utf-8-*-
import hashlib
import json
import sys
import os
import traceback
from retrying import retry
from xml.etree import ElementTree
reload(sys)


sys.setdefaultencoding('utf8')


def md5_secret(s):
    """
    Encrypt a string through md5 method
    :param s: the string being encrypted
    :return: a string encrypted
    """
    m = hashlib.md5(s)
    return m.hexdigest()


def handle_data(data):
    """
    handle the data crawled, adding a verification sign
    :param data: data crawled
    :return: date after adding a sign
    """
    sign = md5_secret(data + 'raventech_nlp')
    final_data = json.loads('{"sign":"' + sign + '","data":' + data + '}')
    return final_data


def create_post_urls(configure_dict, post_base):
    configure_dict['post_urls'] = [each+configure_dict['post_url'] for each in post_base]
    del configure_dict['post_url']
    return configure_dict


def mail_notification(admin):
    def _notify(func):
        def __notify(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except TransException as e:
                print traceback.print_exc()
                os.system('echo "Some problem happened in {}: {}" | mail -s "error notification" {}'.format(func.__name__,
                                                                                                       e, admin))
            except:
                pass
        return __notify
    return _notify


class TransException(Exception):
    pass


my_retry = retry(wait_random_min=1000, wait_random_max=2000, stop_max_attempt_number=3)