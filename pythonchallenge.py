#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shitwidth=4 softtabstop=4

# License: GPL

# NOTE: these codes are written for challenges on http://www.pythonchallenge.com

def challenge_001():
    print 2**38

def challenge_002_v1():
    character_map = "cdefghijklmnopqrstuvwxyzab"
    source = "g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."
    target = ""
    index = 0
    for c in source:
        if "a" <= c and c <= "z":
            i = character_map.find(c)
            target += character_map[(i+2)%26]
        else:
            target += c
        index += 1
    print target

def challenge_002(source=None):
    import string
    table = string.maketrans("abcdefghijklmnopqrstuvwxyz","cdefghijklmnopqrstuvwxyzab")
    if not source:
        source = "g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."
    target = string.translate(source,table)
    print target

def challenge_003():
    import requests
    r = requests.get("http://www.pythonchallenge.com/pc/def/ocr.html")
    mess = r.content.split("-->")[-2]
    url = ""
    for c in mess:
        if "a" <= c and c <= "z":
            url += c
    print url

# this is efficient but it is wrong
def challenge_004_v1():
    import requests
    r = requests.get("http://www.pythonchallenge.com/pc/def/equality.html")
    mess = r.content.split("-->")[-2]
    url = ""
    l = 0 # left upper cha count
    r = 0 # right upper cha count
    m = None # middle lower cha is found
    for c in mess:
        if c.isalpha():
            if c.islower() and l == 3 and not m:
                m = c
            elif c.islower() and r ==3 and m:
                url += m
                m = c
                r = 0
            elif c.islower():
                l = 0
                m = None
                r = 0
            elif not m:
                l += 1
                if l > 3:
                    l = 0
            elif m:
                r += 1
        else:
            l = 0
            m = None
            r = 0
    print url

# i think it is a two dimensions array, but it is wrong
# finally, it is proved to be a single dimension
def challenge_004_v2():
    import requests
    r = requests.get("http://www.pythonchallenge.com/pc/def/equality.html")
    mess = r.content.split("-->")[-2]
    mazes = mess.split("\n")
    url = ""

    def _check(mazes, i, j, x, y):
        result = True
        for index in range(0,3):
            i += x
            j += y
            result = result and mazes[j][i].isupper()
        i += x
        j += y
        if (0 <= i and i < len(mazes[0])) and (0 <= j and j < len(mazes)):
            result = result and mazes[j][i].islower()
        return result

    i = j = 2
    lenx = len(mazes[0])
    leny = len(mazes)
    while j < leny - 3:
        j += 1
        while i < lenx - 3:
            i += 1
            if not mazes[j][i].islower():
                continue
            r = _check(mazes, i, j, 0, -1)
            r = r and _check(mazes, i, j, 1, 0)
            r = r and _check(mazes, i, j, 0, 1)
            r = r and _check(mazes, i, j, -1, 0)
            if r:
                url += mazes[j][i]
    print url

def challenge_004():
    import requests
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

def challenge_005():
    import requests

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

def challenge_006():
    # solution from http://unixwars.com/2007/09/11/python-challenge-level-5-peak-hell/ 
    import urllib,pickle
    url='http://www.pythonchallenge.com/pc/def/banner.p'
    obj=pickle.load(urllib.urlopen(url))
    for line in obj:
        print ''.join(map(lambda pair: pair[0]*pair[1], line))

if __name__ == "__main__":
    print challenge_006()
    
