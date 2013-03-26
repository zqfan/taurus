#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 softtabstop=4 shiftwidth=4

# License:
# GPLv3

class Job(object):
    def __init__(self, link=None, pub_time=None,
                 location=None, number=None,
                 title=None, detail=None):
        self.link = link or ""
        self.pub_time = pub_time or ""
        self.location = location or ""
        self.number = number or ""
        self.title = title or ""
        self.detail = detail or ""

    def print_all(self):
        """
        It should be __str__ but i have some problem on
        the unicode str.
        """
        print self.link
        print self.pub_time
        print self.location
        print self.number
        # the detail also contains the title
        #print self.title
        print self.detail


class JobFilter(object):
    def __init__(self, allow=None, deny=None):
        self.allow = allow
        self.deny = deny

    def __call__(self, job):
        location = self.allow.get("location")
        if job.location in location:
            return True
        return False


def to_json(obj):
    if isinstance(obj, Job):
        return {"__class__":"Job",
                "__value__":obj.__dict__}
    raise TypeError(repr(obj) + " is not JSON serializable")


def from_json(obj):
    if "__class__" in obj:
        if obj["__class__"] == "Job":
            return Job(**obj["__value__"])
    return obj
