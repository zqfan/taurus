#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shitwidth=4 softtabstop=4

import requests


def answer():
    r = requests.get("http://www.pythonchallenge.com/pc/def/equality.html")
    mess = r.content.split("-->")[-2]
    url = ""

    def _check(mess, index, x):
        r = True
        for i in range(0,3):
            index += x
            if 0 <= i and i < len(mess):
                r = r and mess[index].isupper()
            else:
                r = False
        index += x
        # if it out of bounds, it will be true
        if 0 <= i and i < len(mess):
            r = r and mess[index].islower()
        return r
        
    index = 0
    leng = len(mess)-2
    while index < leng:
        index += 1
        if not mess[index].islower():
            continue
        # check left and right side
        r = _check(mess, index, -1)
        r = r and _check(mess, index, 1)
        if r:
            url += mess[index]
    print url


if __name__ == '__main__':
    answer()
