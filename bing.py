#!/bin/python
# -*- coding: utf-8 -*-

"""
Bing 壁纸爬虫
"""

import urllib
import urllib.request
import ssl
import time
import json
import os.path


class BingBgDownloader(object):
    _bing_interface = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=%d&nc=%d&pid=hp&mkt=zh-CN&uhd=1&uhdwidth=3840&uhdheight=2160'
    _bing_img_url = 'https://www.bing.com'
    _img_filename = '[%s%s][%s].%s'

    def __init__(self):
        super(BingBgDownloader, self).__init__()
        ssl._create_default_https_context = ssl._create_unverified_context

    # 下载壁纸图片
    def download(self, num=1, local_path='./'):
        if num < 0:
            num = 1
        url = self._bing_interface % (num, int(time.time()))
        img_info = self._get_img_inofs(url)
        for info in img_info:
            print(self._get_img_url(info))
            print(self._get_img_name(info))
            self._download_img(self._get_img_url(
                info), self._get_img_name(info))

    # 从接口获取图片信息
    def _get_img_inofs(self, url):
        request = urllib.request.urlopen(url).read()
        bgObj = json.loads(bytes.decode(request))
        return bgObj['images']

# 从接口数据提取图片名称
    def _get_img_name(self, img_info):
        zh_name = ''
        pos = img_info['copyright'].index('(')
        if pos < 0:
            zh_name = img_info['copyright']
        else:
            zh_name = img_info['copyright'][0:pos]
        entemp = img_info['url']
        en_name = entemp[entemp.index('OHR.') + 1: entemp.rindex('_ZH')]
        ex_name = entemp[entemp.rindex('.') + 1: entemp.rindex('&pid')]
        pix = entemp[entemp.rindex('&w=') + 3: entemp.rindex('&h')] + \
            'x' + \
            entemp[entemp.rindex('&h=') + 3: entemp.rindex('&rs')]
        img_name = self._img_filename % (zh_name, en_name, pix, ex_name)
        return img_name

    # 获取图片地址
    def _get_img_url(self, img_info):
        return self._bing_img_url + img_info['url']

    # 下载图片
    def _download_img(self, img_url, img_pathname):
        img_data = urllib.request.urlopen(img_url).read()
        f = open(img_pathname, 'wb')
        f.write(img_data)
        f.close()
        print('success img saved:', img_url)


if __name__ == '__main__':
    dl = BingBgDownloader()
    dl.download()
