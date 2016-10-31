# -*-coding:utf-8-*-
import datetime
import time
from __util__.library import create_post_urls, mail_notification
from __configure__.ConfigureParser import ConfigureParser
from __spider__.spidermovie import handle_movie
from __spider__.spidermusic import handle_music
from __spider__.spiderseries import handle_series
from __spider__.netEaseMusic import handle_netease_music

Configure = ConfigureParser('./__configure__/configure.xml')
# get interval time from the configure file
interval = int(eval(Configure.get_configure_by_tag_name('update_duration')))


def manage(func):
    """
    a decorator to print executing info and set sleep time
    :param func: the function being executed
    :return: an auxiliary function
    """
    def wraps(*arg, **args):
        while 1:
            print "Start executing at {}".format(datetime.datetime.now())
            func(*arg, **args)
            print "End executing at {}".format(datetime.datetime.now())
            time.sleep(interval)
    return wraps


@manage
def handle():
    """
    main function, to execute four spider functions
    :return: none
    """
    base_post_urls = Configure.get_configure_by_tag_name('post_base').split(',')
    music_configure = create_post_urls(Configure.get_configures_by_type('music'), base_post_urls)
    netEase_configure = create_post_urls(Configure.get_configures_by_type('netease'), base_post_urls)
    series_configure = create_post_urls(Configure.get_configures_by_type('series'), base_post_urls)
    jiemu_configure = create_post_urls(Configure.get_configures_by_type('jiemu'), base_post_urls)
    movie_configure = create_post_urls(Configure.get_configures_by_type('movie'), base_post_urls)
    handle_music(**dict(music_configure))
    handle_series(**dict(series_configure))
    handle_series(**dict(jiemu_configure))
    handle_movie(**dict(movie_configure))
    handle_netease_music(**dict(netEase_configure))


if __name__ == '__main__':
    handle()
