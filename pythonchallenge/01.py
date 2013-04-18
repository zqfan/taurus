#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shitwidth=4 softtabstop=4

import string


def answer():
    table = string.maketrans("abcdefghijklmnopqrstuvwxyz",
                             "cdefghijklmnopqrstuvwxyzab")
    source = "".join(["g fmnc wms bgblr rpylqjyrc gr zw fylb. ",
                      "rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw ",
                      "fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr ",
                      "gq qm jmle. sqgle qrpgle.kyicrpylq() gq ",
                      "pcamkkclbcb. lmu ynnjw ml rfc spj.",])
    target = string.translate(source,table)
    print target


if __name__ == '__main__':
    answer()
