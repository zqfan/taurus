#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shitwidth=4 softtabstop=4

import requests


def answer():
    r = requests.get("http://www.pythonchallenge.com/pc/def/ocr.html")
    mess = r.content.split("-->")[-2]
    url = []
    for c in mess:
        if "a" <= c <= "z":
            url.append(c)
    print ''.join(url)


if __name__ == '__main__':
    answer()
