#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 softtabstop=4 shiftwidth=4

import sys
import time
import json
import argparse


data_path = '/home/zqfan/appdata/cloth/'
filename = 'cloth.data'
cloth_list = [
    'underpants', 
    'underwear', 
    'trousers', 
    'sweater', 
    'coat']


class Clothes(object):
    """Basical clothes class contains normal cloth."""
    def __init__(self):
        self._current = {}
        self._history = []
        self._load_data()

    def _load_data(self):
        fp = open(data_path+filename,'r')
        self._current, self._history = json.load(fp)
        fp.close()

    def save(self):
        content = (self._current, self._history)
        fp = open(data_path+filename,'w')
        json.dump(content, fp)
        fp.close()

    def list(self, *args, **kwargs):
        for key in self._current:
            print self._current[key], key

    def add(self, *args, **kwargs):
        for key in kwargs:
            if not kwargs[key]:
                continue
            if key in self._current:
                continue
            self._current[key] = time.strftime('%Y-%m-%d')
        self.mark()

    def remove(self, *args, **kwargs):
        for key in kwargs:
            if not kwargs[key]:
                continue
            if key in self._current:
                del self._current[key]
        self.mark()

    def update(self, **kwargs):
        for cloth in self._current:
            if cloth in kwargs and kwargs[cloth]:
                self._current[cloth] = time.strftime('%Y-%m-%d')
        self.mark()
    
    def mark(self):
        self._history.append(self._current)

    def exit(self):
        self.save()


class CLI(object):
    """simple CLI for Clothes."""
    def __init__(self, app):
        self._app = app()
        self._parser = argparse.ArgumentParser()
        for cloth in cloth_list:
            self._parser.add_argument('--'+cloth, action='store_true')
        self._parser.add_argument('command')
        self._args = self._parser.parse_args(sys.argv[1:])

    def run(self):
        self._dispatch()

    def _dispatch(self):
        command = self._args.command
        if hasattr(self._app, command):
            del self._args.command
            getattr(self._app, command)(**self._args.__dict__)
        else:
            print 'invalid command ' + command
    
    def exit(self):
        self._app.exit()
    

def main():
    cli = CLI(Clothes)
    cli.run()
    cli.exit()
        

if __name__ == '__main__':
    main()
