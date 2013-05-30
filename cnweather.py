#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 softtabstop=4 shiftwidth=4

import sys
import json
import re

import argparse
from urllib import quote
import requests


def get_argparse():
    args = argparse.ArgumentParser(
        description='get weather from www.weather.com.cn')
    args.add_argument('-c', '--city-code',
                      default='101010100',  # beijing
                      dest='city_code',
                      help='citycode of your city')
    args.add_argument('-n', '--city-name',
                      dest="city_name",
                      help="city name of your city")
    args.add_argument('-o', '--output-file',
                      dest='output_file',
                      help='print weather info to specific file')
    return args


def get_weather_data(city_code):
    data_url = 'http://m.weather.com.cn/data/%s.html' % city_code

    try:
        resp = requests.get(data_url)
    except:
        return
    if resp.status_code != 200:
        return
    content = resp.content.replace("℃", "'C")
    content = content.replace('~', ' / ')
    try:
        data = json.loads(content)['weatherinfo']
    except ValueError, e:
        return
    return data


def dump_weather_data(data, file_name):
    with open(file_name, 'w') as f:
        f.write(data.get('city'))
        for i in range(1, 7):
            temp = "temp%d" % i
            weather = "weather%d" % i
            wind = "wind%d" % i
            f.write('\n%s %s %s' % (data.get(temp),
                                  data.get(weather),
                                  data.get(wind)))


def print_weather_data(data, file_name=None):
    if not data:
        return
    if file_name:
        dump_weather_data(data, file_name)
        return
    print data.get('city')
    for i in range(1, 7):
        temp = "temp%d" % i
        weather = "weather%d" % i
        wind = "wind%d" % i
        print data.get(temp), data.get(weather), data.get(wind)


def get_city_code(city_name):
    city_name = quote(city_name)  # url encode
    url = ("http://toy.weather.com.cn/SearchBox/searchBox?"
           "callback=jsonp1342857491709&_=1342857620727"
           "&language=zh&keyword=%s" % city_name)
    resp = requests.get(url)
    content = resp.content.split("(")[1].split(")")[0]
    city_code = json.loads(content)["i"][0]["i"]
    return city_code


def main():
    args = get_argparse()
    args.parse_args(sys.argv[1:], args)
    if args.city_name:
        args.city_code = get_city_code(args.city_name)
    data = get_weather_data(args.city_code)
    print_weather_data(data, args.output_file)


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()
