#! /usr/bin/env python
# -*- conding: utf-8 -*-
# vim: tabstop=4 softtabstop=4 shiftwidth=4

# License:
# GPLv3

import json
import time
import logging

import driver

class JobDigger(object):
    """Class comminutes with end user.

    example: jd = JobDigger(("tencent"),)
    """

    drivers = []
    job_info = []
    env = {}

    def __init__(self, companies=None):
        """
        @param
        @companies: tulpe of companies, which indicate series DiggerDriver
                    according to the name
        """
        self._init_log()
        self._init_driver(companies)
        self.load_env()
        self.load_job_info()

    def _init_log(self):
        format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        logging.basicConfig(filename="log",format=format)
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(logging.DEBUG)
        self._logger.info("initialization finished")

    def _init_driver(self, companies):
        if not companies:
            self.drivers = [driver.FakeDriver()]
            return
        for company in companies:
            dd = driver.DriverBuilder.get_driver(company)
            self.drivers.append(dd)

    def get_job_info(self, *args, **kwargs):
        """Get job info from registered drivers.

        You can specify some args which will not handle by this function,
        but will affect particular driver.
        For example get_job_info(last_update="2012-01-01"), will only
        get information newer than or equal to that date.
        """
        for dd in self.drivers:
            infos = dd.get_job_info(*args, **kwargs)
            links = []
            for job_info in self.job_info:
                links.append(job_info["link"])
            for info in infos:
                if info["link"] in links:
                    continue
                self.job_info.append(info)
        self._logger.info("get job info finished.")

    def dump_job_info(self):
        """Dump job info to a local file in json format."""
        fp = open("data", 'w')
        json.dump(self.job_info, fp)
        fp.close()
        date = time.strftime("%Y-%m-%d", time.localtime())
        self.update_env({"last_update":date})
        self.dump_env()
        self._logger.info("dump job info finished. total %d.",
            len(self.job_info))

    def load_job_info(self):
        """Load job info from a local file in json format."""
        fp = open("data", "r")
        self.job_info = json.load(fp)
        fp.close()
        self._logger.info("load job info from local file finished.")

    def load_env(self):
        """Load environment from a local file in json format.

        Currently, only 'last_update' opt is used.
        """
        fp = open("env", "r")
        self.env = json.load(fp)
        fp.close()

    def update_env(self, kwargs):
        """Update env from a dict."""
        for key in kwargs:
            self.env[key] = kwargs[key]
        self._logger.info("env has been updated.")

    def dump_env(self):
        """Dumpp environment to a local file in json format."""
        fp = open("env", "w")
        json.dump(self.env, fp, indent=2)
        fp.close()
        self._logger.info("env has been dumped.")

    def print_job_info(self):
        """print all job info."""
        for job in self.job_info:
            print job.get("content")

        print "total: %d" % len(self.job_info)

def main():
    jd = JobDigger(("tencent",))
    jd.get_job_info(last_update=jd.env["last_update"])
    jd.dump_job_info()
    jd.print_job_info()

if __name__ == "__main__":
    main()
