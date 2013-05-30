#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import sys
import json
import readline

import argparse


class FileNotFound(Exception): pass
class DirNotFound(Exception):
    def __str__(self):
        return "".join(("Error: directory is not found. ",
                super(Exception, self).__str__()))


class explog(object):
    """A expense recorder."""
    _elist = []
    _ecat = {}
    conf = ""

    def __init__(self, conf_file=""):
        if conf_file.strip() == "":
            path = os.path.realpath(sys.path[0])
            if os.path.isfile(path):
                path = os.path.dirname(path)
                path = os.path.abspath(path)
            self.conf = path+os.path.sep+"explog.conf"
        else:
            self.conf = conf_file
        if not os.path.isfile(self.conf):
            raise FileNotFound(self.conf)
        self.date = time.strftime("%Y-%m-%d")

    def _get_file_by_date(self, date, auto_create=True):
        date = date or self.date
        time_t = time.strptime(date,'%Y-%m-%d')
        year = str(time_t.tm_year)
        mon = '%02d' % time_t.tm_mon
        year_dir = self._concate_dir(self.data_dir, year, auto_create)
        mon_dir = self._concate_dir(year_dir, mon, auto_create)
        return os.path.join(mon_dir,date+".txt")

    def add(self, item, price, category='other', date=''):
        category = category or 'other'
        new_data = {'item': item,
                    'price' : price,
                    'category': category,
                    'date': date}
        file_name = self._get_file_by_date(date)
        with open(file_name, 'a+') as f:
            try:
                data = json.load(f)
            except ValueError, e:
                data = self._read_old_format_data(file_name)
            data.append(new_data)
        with open(file_name, 'w') as f:
            json.dump(data, f, indent=2)
        self.list(date)

    def _concate_dir(self, path, sub='', auto_create=False):
        new_dir = os.path.join(path,sub)
        if not os.path.isdir(new_dir):
            if auto_create:
                os.mkdir(new_dir)
            else:
                raise DirNotFound(new_dir)
        return new_dir

    def list(self, date):
        try:
            file_name = self._get_file_by_date(date, False)
        except DirNotFound, e:
            print "Error: no such record: " + date
            return
        if not os.path.isfile(file_name):
            print date+' has no data'
            return
        self._elist = self._list_day(file_name)
        self._print_list()

    def sum(self, month=None, year=None):
        self._elist = []
        if year and not month:
            try:
                year_dir = self._concate_dir(self.data_dir, year)
            except DirNotFound, e:
                print e
                return
            self._list_year(year_dir)
        else:
            month = month or ("%02d" % time.localtime().tm_mon)
            year = year or str(time.localtime().tm_year)
            try:
                year_dir = self._concate_dir(self.data_dir, year)
                month_dir = self._concate_dir(year_dir, month)
            except DirNotFound, e:
                print e
                return
            for root, dirs, files in os.walk(month_dir):
                for name in files:
                    data = self._list_day(os.path.join(root, name))
                    self._elist.extend(data)
        self._print_list()
        self._print_summary(summary=self._get_summary())

    def update(self, id, item=None, price=None, category=None):
        if len(self._elist) <= id or id < 0:
            print "Error: Index error."
            return
        entry = self._elist[item_id]
        entry['item'] = item or entry['item']
        entry['price'] = price or entry['price']
        entry['category'] = category or entry['category']
        self._dump_by_date(date)

    def find(self, item=None, category=None):
        self._elist = []
        for root, year_dirs, files in os.walk(self.data_dir):
            for file_name in files:
                data = self._list_day(os.path.join(root, file_name))
                self._elist.extend(data)
        filtered_list = []
        for entry in self._elist:
            if (entry['item'] == item or
                entry['category'] == category):
                filtered_list.append(entry)
        self._elist = filtered_list
        self._print_list()
        self._print_summary(summary=self._get_summary())

    def delete(self, id):
        id = int(id)
        if len <= id or id < 0:
            print u"Error: Index error."
            return
        date = self._elist[id]['date']
        del self._elist[id]
        self._dump_by_date(date)
        self._print_list()

    def _dump_by_date(self, date):
        new_data = []
        for (i, v) in enumerate(self._elist):
            if self._elist[i]['date'] == date:
                new_data.append(self._elist[i])
        file_name = self._get_file_by_date(date)
        with open(file_name, 'w') as f:
            json.dump(new_data, f)

    def load_conf(self):
        with open(self.conf) as fp:
            for line in fp:
                if line.startswith('data_dir = '):
                    self.data_dir = line[11:].strip()
        if self.data_dir == '':
            self.data_dir = os.path.expanduser('~')+'/appdata/explog'
        if not os.path.isdir(self.data_dir):
            # make directory
            os.mkdir(self.data_dir)

    def _read_old_format_data(self, file_name):
        data = []
        basename = os.path.basename(file_name)
        date = os.path.splitext(basename)[0]
        with open(file_name) as f:
            count = 0
            index = len(self._elist)
            for line in f:
                if line.startswith('category = '):
                    count += 1
                    cat = line[len('category = '):-1]
                elif line.startswith('item = '):
                    count += 1
                    item = line[len('item = '):-1]
                elif line.startswith('price = '):
                    count += 1
                    price = line[len('price = '):-1]
                if count == 3:
                    data.append({'category': cat,
                                 'item': item,
                                 'price': price,
                                 'date': date})
                    index += 1
                    count = 0
        return data

    def _list_day(self,file_name,option=None):
        with open(file_name) as f:
            try:
                data = json.load(f)
            except ValueError, e:
                f.close()
                data = self._read_old_format_data(file_name)
            finally:
                basename = os.path.basename(file_name)
                date = os.path.splitext(basename)[0]
                for entry in data:
                    entry['date'] = entry.get('date') or date
                return data

    def _get_summary(self):
        summary = {}
        for l in self._elist:
            if not summary.has_key(l['category']):
                summary[l['category']] = [1,float(l['price'])]
            else:
                summary[l['category']][0] += 1
                summary[l['category']][1] += float(l['price'])
        return summary

    def _print_list(self):
        self._elist.sort(key=lambda x: x['date'])
       	print '+------+-----------------+-----------------+------------+------------+'
        print ('| %-4.4s | %-15.15s | %-15.15s | %-10.10s | %-10.10s |' %
               ('id','category','item','price','date'))
	print '+------+-----------------+-----------------+------------+------------+'
        for (i, v) in enumerate(self._elist):
            print ('| %-4.4s | %-15.15s | %-15.15s | %-10.10s | %-10.10s |' %
                   (i, self._elist[i]['category'],
                    self._elist[i]['item'],
                    self._elist[i]['price'],
                    self._elist[i]['date']))
	print '+------+-----------------+-----------------+------------+------------+'

    def _print_summary(self, prompt=None, summary={}):
        total = cost = income = 0
        print prompt or 'category summary'
        print '+------------+--------+------------+'
        print ('| %-10.10s | %-6.6s | %-10.10s |' %
               ('category','count','total'))
        print '+------------+--------+------------+'
        for k in summary:
            print ('| %-10.10s | %-6d | %-10.1f |' %
                   (k,summary[k][0],summary[k][1]))
            if k=='bank':
                continue
            if summary[k][1] > 0 :
                income += summary[k][1]
            else:
                cost += summary[k][1]
            total += summary[k][1]
        print '+------------+--------+------------+'
        print ('cost = ' + str(cost) +
               ', income = '+str(income) +
               ', total = '+str(total))

    def exit(self):
        print u'Bye!'
        exit(0)

    def run(self):
        while True:
            try:
                command = raw_input(u'> ')
            except (EOFError, KeyboardInterrupt), e:
                self.exit()
            args = self.argument_parse(command.split())
            args_dict = vars(args)
            func = args_dict.pop('func')
            func(**args_dict)

    def argument_parse(self, args):
        parser = argparse.ArgumentParser()
        sub_parser = parser.add_subparsers()

        parser_add = sub_parser.add_parser('add')
        parser_add.set_defaults(func=self.add)
        parser_add.add_argument('-i', '--item')
        parser_add.add_argument('-p', '--price')
        parser_add.add_argument('-c', '--category', default='other')
        parser_add.add_argument('-d', '--date', default='')

        parser_delete = sub_parser.add_parser('delete')
        parser_delete.set_defaults(func=self.delete)
        parser_delete.add_argument('id')

        parser_list = sub_parser.add_parser('ls')
        parser_list.set_defaults(func=self.list)
        parser_list.add_argument('-d', '--date', default='')

        parser_update = sub_parser.add_parser('update')
        parser_update.set_defaults(func=self.update)
        parser_update.add_argument('-id')
        parser_update.add_argument('-i', '--item', default='')
        parser_update.add_argument('-p', '--price', default='')
        parser_update.add_argument('-c', '--category', default='')

        parser_find = sub_parser.add_parser('find')
        parser_find.set_defaults(func=self.find)
        parser_find.add_argument('-i', '--item', default='')
        parser_find.add_argument('-c', '--category', default='')

        parser_sum = sub_parser.add_parser('sum')
        parser_sum.set_defaults(func=self.sum)
        parser_sum.add_argument('-m', '--month', default='')
        parser_sum.add_argument('-y', '--year', default='')

        parser_exit = sub_parser.add_parser('exit')
        parser_exit.set_defaults(func=self.exit)

        return parser.parse_args(args)


if __name__ == "__main__":
    elog = explog()
    elog.load_conf()
    elog.run()
