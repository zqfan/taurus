#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shitwidth=4 softtabstop=4

import os
import zipfile


def answer():
    """now there are pairs

    url = http://www.pythonchallenge.com/pc/def/channel.html
    Step 1: download the
            http://www.pythonchallenge.com/pc/def/channel.zip
    Step 2: the readme.txt says start from 90052
    Step 3: collect the comments
    """
    zf = zipfile.ZipFile('/tmp/channel.zip')
    files = ['90052.txt']
    while True:
        content = zf.read(files[-1])
        next_file = content.split()[-1]
        if not next_file.isdigit():
            break
        files.append(''.join([next_file, '.txt']))
    print ''.join([zf.getinfo(file_name).comment
                   for file_name in files])

if __name__ == '__main__':
    answer()
