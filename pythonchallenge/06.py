#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shitwidth=4 softtabstop=4

import urllib,pickle


def answer():
    # solution from 
    # http://unixwars.com/2007/09/11/python-challenge-level-5-peak-hell/
    url='http://www.pythonchallenge.com/pc/def/banner.p'
    obj=pickle.load(urllib.urlopen(url))
    for line in obj:
        print ''.join(map(lambda pair: pair[0]*pair[1], line))


if __name__ == '__main__':
    answer()
