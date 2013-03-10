#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 softtabstop=4 shiftwidth=4

# License:
# GPLv3

import time

import requests
from BeautifulSoup import BeautifulSoup


class FakeDriver(object):
    """Fake driver return empty information."""
    def get_job_info(self, *args, **kwargs):
        return []


class TencentDriver(object):
    """Job digger driver for tencent."""
    def __init__(self):
        print "Init " + self.__class__.__name__
        self.root_url = "http://hr.tencent.com/"

    def get_job_info(self, *args, **kwargs):
        """Currently just find tech jobs in all cities."""
        last_update = kwargs.get("last_update")
        job_info = []
        base_url = self.root_url + "position.php?keywords=&tid=87"
        # TODO(aji): loop to dig all pages, currently just first page
        start = 0
        while True:
            url = base_url + "&start=" + str(start) + "#a"
            print "dig from page %d" % (start/10)
            info = self._get_job_links(url, last_update)
            job_info.extend(info)
            if len(info) < 10:
                break
            start += 10      
        return job_info

    def _get_job_links(self, url, last_update):
        job_info = []
        res = requests.get(url)
        bs = BeautifulSoup(res.content)
        table = bs.findAll("table", attrs = {"class":"tablelist"})[0]
        trs = table.findAll("tr", attrs = {"class":"even"})
        trs.extend(table.findAll("tr", attrs = {"class":"odd"}))
        for tr in trs:
            tds = tr.findChildren("td")
            publish_date = time.strptime(tds[-1].text, "%Y-%m-%d")
            last_update_date = time.strptime(last_update, "%Y-%m-%d")
            if publish_date < last_update_date:
                continue
            link = ""
            for attr in tds[0].a.attrs:
                if "href" in attr:
                    link = attr[1]
            single_job_url = self.root_url+link
            content = self._get_single_job(single_job_url)
            job_info.append({"link":single_job_url,"content":content})
            print "%s%s%s" % (self.__class__.__name__,
                    ": get job info from ",
                    single_job_url)
        return job_info
                        
    def _get_single_job(self, url):
        content = ""
        res = requests.get(url)
        bs = BeautifulSoup(res.content)
        table = bs.findAll("table", attrs = {"class": "tablelist textl"})[0]
        # the last two are bookmark text, so ignore them
        tds = table.findAll("td")[:-2]
        for td in tds:
            lis = td.findAll("li")
            if len(lis) != 0:
                content += td.div.text + "\n"
                for li in lis:
                    content += li.text + "\n"
                continue
            content += td.text + "\n"
        return content


class DriverBuilder(object):
    """Build driver according to the given name."""
    @classmethod
    def get_driver(self, name):
        if name.lower() == "tencent":
            return TencentDriver()
        return FakeDriver()
