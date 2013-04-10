#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 softtabstop=4 shiftwidth=4

# License:
# GPLv3

import json
import time
import logging

import pynotify

import driver
import job


LOG_FILE = "/tmp/job_digger.log"
CONF_FILE = "/home/zqfan/appdata/job_digger/job_digger.conf"


class JobDigger(object):
    """Class comminutes with end user.

    example: jd = JobDigger(("tencent"),)
    """

    drivers = []
    jobs = []
    new_jobs = []
    env = {}

    def __init__(self, companies=None):
        """
        @param
        @companies: tulpe of companies, which indicate series
                    DiggerDriver according to the name
        """
        self._init_log()
        self._init_driver(companies)
        self.load_env()
        self.load_jobs()
        pynotify.init("job_digger")
        allow_location = [u"深圳",u"广州"]
        self.job_filter = job.JobFilter(
            allow={"location":allow_location})

    def _init_log(self):
        format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        logging.basicConfig(filename=LOG_FILE,format=format)
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

    def get_jobs(self, *args, **kwargs):
        """Get job info from registered drivers.

        You can specify some args which will not handle by this function,
        but will affect particular driver.
        For example get_job_info(last_update="2012-01-01"), will only
        get information newer than or equal to that date.
        """
        for dd in self.drivers:
            jobs = dd.get_jobs(*args, **kwargs)
            for job in jobs:
                if self.job_exist(job.link):
                    continue
                self.jobs.append(job)
                self.new_jobs.append(job)
        self._logger.info("get jobs finished.")

    def job_exist(self, link):
        """Check if a job already exist according to the link."""
        links = [job.link for job in self.jobs]
        return link in links

    def dump_jobs(self):
        """Dump job info to a local file in json format."""
        fp = open(self.env["data_file"], 'w')
        json.dump(self.jobs, fp, default=job.to_json)
        fp.close()
        date = time.strftime("%Y-%m-%d", time.localtime())
        self.update_env({"last_update":date})
        self.dump_env()
        self._logger.info("dump jobs finished. total %d.",
            len(self.jobs))

    def load_jobs(self):
        """Load job info from a local file in json format."""
        fp = open(self.env["data_file"], "r")
        self.jobs = json.load(fp, object_hook=job.from_json)
        fp.close()
        self._logger.info("load jobs from local file finished.")

    def load_env(self):
        """Load environment from a local file in json format.

        Currently, only 'last_update' opt is used.
        """
        fp = open(CONF_FILE, "r")
        self.env = json.load(fp)
        fp.close()

    def update_env(self, kwargs):
        """Update env from a dict."""
        for key in kwargs:
            self.env[key] = kwargs[key]
        self._logger.info("env has been updated.")

    def dump_env(self):
        """Dumpp environment to a local file in json format."""
        fp = open(CONF_FILE, "w")
        json.dump(self.env, fp, indent=2)
        fp.close()
        self._logger.info("env has been dumped.")

    def print_jobs(self):
        """print all job info."""
        for job in self.jobs:
            job.print_all()
        print "total: %d" % len(self.jobs)

    def filter_jobs(self, jobs):
        filtered_jobs = []
        for job in jobs:
            if self.job_filter(job):
                filtered_jobs.append(job)
                job.print_all()
                self.notify_job(job)
        print "total: %d" % len(filtered_jobs)
        return filtered_jobs

    def update_filter(self, allow=None, deny=None):
        pass

    def notify_job(self,job):
        n = pynotify.Notification(job.title, job.detail)
        n.show()


def main():
    jd = JobDigger(("tencent",))
    jd.get_jobs(last_update=jd.env["last_update"])
    jd.dump_jobs()
    jd.filter_jobs(jd.new_jobs)

if __name__ == "__main__":
    main()
