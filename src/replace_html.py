#!/usr/bin/env python3
# -*- coding: utf-8 -*

import sys, os
import codecs
import requests
import time
from datetime import datetime
import random
from lxml import etree
import yaml

config = yaml.load(open('../conf/conf.yml'))
GIT_IMG_PATH = config["git"]["img_path"]
print (GIT_IMG_PATH)

def down_load_pic(img_src, local_folder):
    """
    下载并返回图片名
    :param img_src: url
    :param local_folder: 本地路径
    :return: 图片名
    """
    #t = str(int(time.time()))
    t = time.strftime("%Y%m%d%H%M%S")
    a = str(random.randint(0, 10000)).zfill(5)
    name = t + a + ".jpg"
    output_name = os.path.join(local_folder, name)
    img = requests.get(img_src)
    with open(output_name, 'ab') as f:
        f.write(img.content)

    return name

def generate_new_name(name):
    """
    将图片名变为github图床中的名字
    :param name:
    :return:
    """
    return os.path.join(GIT_IMG_PATH, name)

def replace_img_in_html(src_html, dst_html):
    """
    家在本地html文件，替换图床后，生成新html文件
    :param src_html:
    :param dst_html:
    :return:
    """
    html = etree.parse(src_html, etree.HTMLParser())
    #links = html.xpath('//img/@src')
    links = html.xpath('//img[@src]')
    for link in links:
        url = link.get('src')
        name = down_load_pic(url, "../pic")
        new_name = generate_new_name(name)
        link.set("src", new_name)

    html.write(dst_html)

    return


if __name__ == '__main__':

    src_html = "/Users/karl/Downloads/md2all.html"
    dst_html = "/Users/karl/Desktop/md2all.html"

    replace_img_in_html(src_html, dst_html)

