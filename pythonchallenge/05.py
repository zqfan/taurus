#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shitwidth=4 softtabstop=4

import requests


def answer():
    url_base = "http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing="
    url = url_base + "12345"
    for i in range(0,1000):
        r = requests.get(url)
        print r.content
        next_id = r.content.split()[-1]
        url = url_base + next_id
        if not next_id.isdigit() and next_id.endswith(".html"):
            url = "http://www.pythonchallenge.com/pc/def/"+next_id
            return url

if __name__ == '__main__':
    answer()
