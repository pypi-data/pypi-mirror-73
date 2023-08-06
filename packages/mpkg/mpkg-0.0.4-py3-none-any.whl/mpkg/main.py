#!/usr/bin/env python3
# coding: utf-8

import gettext
import json
import os
import re
import time
from functools import lru_cache
from multiprocessing.dummy import Pool
from pathlib import Path
from pprint import pformat, pprint
from typing import List, Tuple
from urllib.parse import unquote

import click
from lxml import etree

from mpkg.utils import Download, GetPage

downloader = r'wget -P "d:\Downloads"'

UA = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/601.4.4 (KHTML, like Gecko) Version/9.0.3 Safari/601.4.4'}
defaultList = [-1, -1, -1]
defaultLog = ''

_ = gettext.gettext


def selected(L: list, isSoft=False, msg=_('select (eg: 0,2-5):')) -> list:
    cfg = []
    for i, x in enumerate(L):
        if isSoft:
            print(f'{i} -> {x.id}')
        else:
            print(f'{i} -> {x}')
    option = input(f' {msg} ').replace(' ', '').split(',')
    print()
    for i in option:
        if '-' in i:
            a, b = i.split('-')
            for j in range(int(a), int(b)+1):
                cfg.append(L[j])
        else:
            cfg.append(L[int(i)])
    return cfg


def IsLatest(bydate=False):
    pass


class Soft(object):
    id = ''
    allowExtract = False
    isPrepared = False
    needConfig = False

    def __init__(self, name='', rem=''):
        if name:
            self.id = name
        self.rem = rem

    def _parse(self) -> Tuple[List[int], List[int], List[str], str]:
        return defaultList, defaultList, ['url'], defaultLog

    def json(self) -> bytes:
        if not self.isPrepared:
            self.prepare()
        return json.dumps(self.data).encode('utf-8')

    def download(self):
        # -v print(_('使用缺省下载方案'))
        if len(self.links) != 1:
            link = selected(self.links, msg=_('select a url:'))[0]
        else:
            link = self.links[0]
        Download(link)

    def prepare(self):
        self.isPrepared = True
        self.ver, self.date, self.links, self.log = self._parse()
        data = {}
        data['id'] = self.id
        data['ver'] = self.ver
        data['links'] = self.links
        if self.date != defaultList:
            data['date'] = self.date
        if self.rem:
            data['rem'] = self.rem
        if self.log:
            data['changelog'] = self.log
        self.data = data


class Driver(Soft):
    needConfig = True

    def __init__(self, url: str, name='', rem=''):
        super().__init__(name, rem=rem)
        self.name = name
        self.rem = rem
        self.url = url


class NvidiaDriver(Driver):
    def __init__(self, url, name='', rem='', isStudio=False):
        super().__init__(url, name=name, rem=rem)
        self.isStudio = isStudio

    def _parse(self):
        r = GetPage(self.url, headers=UA)
        L = etree.HTML(r).xpath('//*[@id="driverList"]')
        if self.isStudio:
            L = [x for x in L if x.xpath(
                './/a')[0].text == 'NVIDIA Studio Driver']
        else:
            L = [x for x in L if x.xpath(
                './/a')[0].text != 'NVIDIA Studio Driver']
        r = L[0].xpath('.//td')
        date = time.strptime(r[3].text, '%B %d, %Y')[0:3]
        v = r[2].text
        u = [
            f'https://us.download.nvidia.com/Windows/{v}/{v}-notebook-win10-64bit-international-dch-whql.exe']
        log = f'https://us.download.nvidia.com/Windows/{v}/{v}-win10-win8-win7-release-notes.pdf'
        return list(map(int, v.split('.'))), date, u, log


@lru_cache
def getIntelList(URL) -> list:
    # ['英特尔®显卡-Windows® 10 DCH 驱动程序', '驱动程序', ['Windows 10，64 位*'], '27.20.100.8280', '05-29-2020', '/zh-cn/download/29616/-Windows-10-DCH-']
    u = URL.split('/product/')
    u = u[0] + '/json/pageresults?pageNumber=2&productId=' + u[1]
    # u = u[0] + '/json/pageresults?productId=' + u[1]
    print(u)
    r = u#requests.get(u).json()
    return [[x['Title'], x['DownloadType'], x['OperatingSystemSet'], x['Version'], x['PublishDateMMDDYYYY'], x['FullDescriptionUrl']] for x in r['ResultsForDisplay']]


def getIntelDrivers(u) -> list:
    r = GetPage(u)
    u = [x.xpath('.//a')[0].values()[1]
         for x in etree.HTML(r).xpath('//*[@class="download-file"]')]
    drivers = [unquote(x).split('httpDown=')[::-1][0] for x in u]
    return drivers


class IntelWifi(Soft):
    id = 'IntelWifi'

    def _parse(self):
        page = GetPage(
            'https://www.intel.cn/content/www/cn/zh/support/articles/000017246/network-and-i-o/wireless-networking.html')
        a = [x for x in etree.HTML(page).xpath(
            '//a') if b'&#229;&#156;&#168;&#230;&#173;&#164;&#229;&#164;&#132;&#228;&#184;&#139;&#232;&#189;&#189;' in etree.tostring(x)]
        if len(a) == 1:
            links = sorted(getIntelDrivers(a[0].values()[0]), reverse=True)[:3]
        else:
            print('IntelWifi(Soft) parsing error')
        return defaultList, defaultList, links, defaultLog


class IntelDriver(Driver):
    def __init__(self, url, driverKeyword, name='', rem=''):
        super().__init__(url, name=name, rem=rem)
        self.kw = driverKeyword

    def _parse(self):
        L = getIntelList(self.url)
        item = sorted([x for x in L if self.kw in x[0]],
                      key=lambda x: x[3], reverse=True)[0]
        date = item[4].split('-')
        date = [date[-1]]+date[:-1]
        ver = item[3]
        url = 'https://downloadcenter.intel.com'+item[-1]
        drivers = getIntelDrivers(url)
        return list(map(int, ver.split('.'))), list(map(int, date)), drivers, defaultLog


def prepare(soft):
    soft.prepare()


SOFTS = [NvidiaDriver('https://www.nvidia.com/Download/processFind.aspx?psid=111&pfid=888&osid=57&lid=1&whql=&lang=en-us&ctk=0&dtcid=1', name='rtx'),
         IntelDriver('https://downloadcenter.intel.com/zh-cn/product/134906',
                     name='uhd', driverKeyword='英特尔®显卡-Windows® 10 DCH 驱动程序'),
         IntelDriver('https://downloadcenter.intel.com/product/125192', name='wifi',
                     driverKeyword='Windows® 10 Wi-Fi Drivers for Intel® Wireless Adapters')
         ]


@click.group()
def cli():
    pass


@cli.command()
@click.option('-j', '--jobs', default=10, help=_('threads'))
@click.option('-d', '--download', is_flag=True)
@click.option('--all', is_flag=True, help=_('check all packages'))
@click.option('--bydate', is_flag=True, help=_('check version by date'))
# @click.option('-v', default=False, help=_('show all packages'))
# @click.option('-i', '--install', default=False, help=_('install packages'))
def check(jobs, download, all, bydate):
    if all:
        soft_list = SOFTS
    else:
        soft_list = selected(SOFTS, isSoft=True)

    with Pool(jobs) as p:
        p.map(prepare, soft_list)

    for soft in soft_list:
        pprint(soft.data)

    '''soft_list = [soft for soft in soft_list if not soft.isLatest]

    if download:
        for soft in soft_list:
            soft.download()'''


if __name__ == "__main__":
    cli()
