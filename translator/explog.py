#! /usr/bin/env python

import os
import time
import cmdpar

class explog:
    _elist = []
    _ecat = {}
    conf = ""

    def __init__(self,conf_file=""):
        print 'elog version 0.1, copyright (c) ZhiQiang Fan, all rights reserved.'
        if conf_file.strip()=="":
            self.conf = os.path.expanduser('~')+"/code/python/explog.conf"
        else:
            self.conf = conf_file
        self.date = time.strftime("%Y-%m-%d")

    def load_conf(self):        
        if os.path.isfile(self.conf):
            self._load_conf()             
        else:
            print 'configure file does not exist, program exit'
            exit(1)

    def add(self,item,price,category='other',date=''):
	if category.strip()=='':
	    category = 'other'
        if date.strip()=='':
            date = self.date
        time_t = time.strptime(date,'%Y-%m-%d')
        year_dir = str(time_t.tm_year)
        mon_dir = str(time_t.tm_mon)
        if len(mon_dir) == 1:
            mon_dir = '0'+mon_dir
        if not os.path.isdir(self.data_dir+os.path.sep+year_dir):
            os.mkdir(self.data_dir+os.path.sep+year_dir)
        if not os.path.isdir(self.data_dir+os.path.sep+year_dir+os.path.sep+mon_dir):
            os.mkdir(self.data_dir+os.path.sep+year_dir+os.path.sep+mon_dir)
        file_name = self.data_dir+os.path.sep+year_dir+os.path.sep+mon_dir+os.path.sep+date+".txt"
        fp = open(file_name,'a')
        fp.write("category = "+category+"\nitem = "+item+"\nprice = "+price+"\n")
        fp.close()
        self._elist = [date,]
        self._list_day(file_name)

    def list(self,date=''):
        if date.strip()=='':
            date = self.date
        time_t = time.strptime(date,'%Y-%m-%d')
        year_dir = str(time_t.tm_year)
        mon_dir = str(time_t.tm_mon)
        if len(mon_dir) == 1:
            mon_dir = '0'+mon_dir
        if not os.path.isdir(self.data_dir+os.path.sep+year_dir):
            print year_dir+' has no data'
            return
        if not os.path.isdir(self.data_dir+os.path.sep+year_dir+os.path.sep+mon_dir):
            print year_dir+'-'+mon_dir+' has no data'
            return
        file_name = self.data_dir+os.path.sep+year_dir+os.path.sep+mon_dir+os.path.sep+date+".txt"
        if os.path.isfile(file_name)==False:
            print date+' has no data'
            return
        self._elist = [date,]
        self._list_day(file_name)
        self._summary_cat()
        self._print_list()
        
    def sum(self,month=None,year=None):
        if year and not month:
            year_dir = self.data_dir+os.path.sep+year+os.path.sep
            if not os.path.exists(year_dir):
                print 'directory '+year_dir+' does not exist.'
                return
            self._elist = [year,]
            self._list_year(year_dir)
        else:
            m = month or str(time.localtime().tm_mon)
            y = year or str(time.localtime().tm_year)
            if len(m)==1:
                m = '0'+m
            month_dir = self.data_dir+os.path.sep+y+os.path.sep+m+os.path.sep
            if not os.path.exists(month_dir):
                print 'directory '+month_dir+' does not exist.'
                return
            self._elist = [y+'-'+m,]
            self._list_month(month_dir)
        self._summary_cat()
        self._print_list()
        self._print_cat()
    
    def update(self,item_id,item=None,price=None,category=None,date=None):
        i = 1
        length = len(self._elist)
        while i < length:
            if self._elist[i][0]==int(item_id):
                if len(self._elist[0]) != 10:
                    return
                if date:
                    item = item or self._elist[i][2]
                    p = price or self._elist[i][3]
                    c = category or self._elist[i][1]
                    d = self._elist[0]
                    self.add(item,p,c,date)
                    # add will list by default, which will change _elist entirely
                    # del self._elist[i]
                    self.list(d)
                    del self._elist[i]
                    self._flush_list()
                    return
                if category:
                    self._elist[i][1] = category
                if item:
                    self._elist[i][2] = item
                if price:
                    self._elist[i][3] = price
                self._flush_list()
                return
            i += 1

    def find(self,item=None,category=None,date=None):
        year_dir_list = os.listdir(self.data_dir)
        year_dir_list.sort()
        self._elist = ["find"]
        for year in year_dir_list:
            self._list_year(self.data_dir+os.path.sep+year+os.path.sep)
        i = 1
        length = len(self._elist)
        while i < length:
            if item:
                if self._elist[i][2] != item:
                    del self._elist[i]
                    length -= 1
                    continue
            if category:
                if self._elist[i][1] != category:
                    del self._elist[i]
                    length -= 1
                    continue
            if date:
                if self._elist[i][4] != date:
                    del self._elist[i]
                    length -= 1
                    continue
            i += 1
        self._summary_cat()
        self._print_list()
        self._print_cat()

    def delete(self,item_id):
        i = 1
        length = len(self._elist)
        while i < length:
            if self._elist[i][0]==int(item_id):
                if self._elist[i][4] != self._elist[0]:
                    return
                del self._elist[i]
                self._flush_list()
                break
            i += 1

    def help(self):
        print "sum [-m month][-y year]"
        print "find [-c category][-i item][-d date]"

    def _flush_list(self):
        file_name = self.data_dir+os.path.sep+self._elist[0][:4]+os.path.sep+self._elist[0][5:7]+os.path.sep+self._elist[0]+'.txt'
        if not os.path.isfile(file_name):
            print 'file not exist: '+file_name
            return
        length = len(self._elist)
        i = 1
        fp = open(file_name,'w')
        while i < length:
            fp.write('category = '+self._elist[i][1]+'\nitem = '+self._elist[i][2]+'\nprice = '+self._elist[i][3]+'\n')
            i += 1
        fp.close()

    def _list_year(self,year_dir):
        month_list = os.listdir(year_dir)
        for month_dir in month_list:
            if os.path.isdir(year_dir+month_dir):
                self._list_month(year_dir+month_dir+os.path.sep)

    def _list_month(self,month_dir):
        dir_list = os.listdir(month_dir)
        dir_list.sort()
        length = len(dir_list)
        i = 0
        while i < length:
            if os.path.isfile(month_dir+dir_list[i]):
                self._list_day(month_dir+dir_list[i])
                i += 1

    def _load_conf(self):
        fp = open(self.conf)
        lines = fp.readlines()
        for line in lines:
            if line.startswith('data_dir = '):
                self.data_dir = line[11:]
        self.data_dir = self.data_dir.strip()
        fp.close()
        if self.data_dir.strip()=='':
            self.data_dir = os.path.expanduser('~')+"/appdata/explog"
        if os.path.isdir(self.data_dir)==False:
            # make directory
            os.mkdir(self.data_dir)

    def _list_day(self,file_name,option=None):
        fp = open(file_name)
        lines = fp.readlines()
        fp.close()
        count = 0
        index = len(self._elist)
        for line in lines:
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
                self._elist.append([index,cat,item,price,os.path.split(file_name)[1].split('.')[0]])
                index += 1
                count = 0

    def _summary_cat(self):
        self._ecat = {}
        elist = self._elist[1:]
        for l in elist:
            if not self._ecat.has_key(l[1]):
                self._ecat[l[1]] = [1,float(l[3])]
            else:
                self._ecat.get(l[1])[0] += 1
                self._ecat.get(l[1])[1] += float(l[3])

    def _print_list(self):
        print 'log for '+self._elist[0]
       	print '+------+-----------------+-----------------+------------+------------+'
        print '| %-4.4s | %-15.15s | %-15.15s | %-10.10s | %-10.10s |'%('id','category','item','price','date')
	print '+------+-----------------+-----------------+------------+------------+'
        length = len(self._elist)
        i = 1
        while i < length:
            print u'| %-4.4s | %-15.15s | %-15.15s | %-10.10s | %-10.10s |'%(self._elist[i][0],self._elist[i][1],self._elist[i][2].decode('utf8'),self._elist[i][3],self._elist[i][4])
            i += 1
	print '+------+-----------------+-----------------+------------+------------+'

    def _print_cat(self,prompt=None):
        total = cost = income = 0
        print prompt or 'category summary'
        print '+------------+--------+------------+'
        print '| %-10.10s | %-6.6s | %-10.10s |'%('category','count','total')
        print '+------------+--------+------------+'
        for k in self._ecat:
            print '| %-10.10s | %-6d | %-10.1f |'%(k,self._ecat[k][0],self._ecat[k][1])
            if k=='bank':
                continue
            if self._ecat[k][1] > 0 :
                income += self._ecat[k][1]
            else:
                cost += self._ecat[k][1]
            total += self._ecat[k][1]
        print '+------------+--------+------------+'
        print 'cost = '+str(cost)+', income = '+str(income)+', total = '+str(total)

elog = explog()
elog.load_conf()
cp = cmdpar.cmd_parser(['add',elog.add,'ls',elog.list,'sum',elog.sum,'update',elog.update,'delete',elog.delete,'find',elog.find,'help',elog.help],
                [['-i',"",'-p',"",'-c',"other",'-d',time.strftime('%Y-%m-%d')],
                 ['-d',''],
                 ['-m','','-y',''],
                 ['-id','','-i','','-p','','-c','','-d',''],
                 ['-id',''],
                 ['-i','','-c','','-d',''],
                 [],
                ],
                'explog # ')
cp.run()
