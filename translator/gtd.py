#! /usr/bin/env python

# Copyritght (c) ZhiQiang Fan, All right reserved.

import os
import time
import string
import cmdpar

class gtd:
    def __init__(self,conf_file=''):
	print 'gtd version 0.1, copyright (c) ZhiQiang Fan 2012'
        if conf_file.strip()=="":
            self.conf = os.path.expanduser('~')+"/code/python/gtd.conf"
        else:
            self.conf = conf_file
        self.date = time.strftime("%Y-%m-%d")
        self.things = []

    def load_conf(self):        
        if os.path.isfile(self.conf):
            self._load_conf()             
        else:
            print 'configure file does not exist, program exit'
            exit(1)

    def _load_conf(self):
        fp = open(self.conf)
        lines = fp.readlines()
        for line in lines:
            if line.startswith('data_dir = '):
                self.data_dir = line[11:]
        self.data_dir = self.data_dir.strip()
        fp.close()
        if self.data_dir.strip()=='':
            self.data_dir = os.path.expanduser('~')+"/appdata/gtd"
        if os.path.isdir(self.data_dir)==False:
            # make directory
            os.mkdir(self.data_dir)

    def load_file(self):
        file_handler = open(self.data_dir+os.path.sep+'gtd-unfinished.txt','a+')
        lines = file_handler.readlines()
        file_handler.close()
        if len(lines) < 1:
            return
        ready_arg = 0
        i = 0
        self.nextid = 1;
        while i < len(lines):
            if lines[i].startswith('content = '):
                content = lines[i][10:len(lines[i])-1]
                ready_arg = ready_arg + 1
            elif lines[i].startswith('urgent = '):
                urgent = lines[i].split()[2]
                ready_arg = ready_arg + 1
            elif lines[i].startswith('status = '):
                status = lines[i].split()[2]
                ready_arg += 1
            elif lines[i].startswith('target_date = '):
                target_date = lines[i].split()[2]
                ready_arg += 1
            elif lines[i].startswith('update_date = '):
                update_date = lines[i].split()[2]
                ready_arg += 1
            elif cmp(lines[i],"")==0:
                print "invalid record has been found: "+lines[i]
            i += 1
            if ready_arg == 5:
                ready_arg = 0
                self.things.append({'id':str(self.nextid),'content':content,'urgent':urgent,'status':status,'target_date':target_date,'update_date':update_date,})
                self.nextid += 1

    def help(self):
        print "command list:"
        print "  touch                insert a new thing or modify a exist thing"
        print "    [-thing|-t string] insert a thing content, this should not be null when not use with -i"
        print "    [-urgent|-u [0-9]] specific a thing's urgency level"
        print "    [-status|-s [0-2]] specific a thing's status"
        print '    [-td]              specific target date to finish the thing'
        print "    [-id|-i] [0-9]+    specific a thing's id, this argument will make touch to a modify command instead insert command"
        print "  ls                   list all the things generally, only print the content"
        print "    [-l]               list things with details"
        print "  help                 print all the available commands"
        print "  exit                 exit gtd"
    
    def list(self,arg=""):
	if arg and (not arg.startswith('-')):
            return
        self.things.sort(self._sort_cmp);
        for thing in self.things:
            if (arg.find('a')==-1) and (thing['target_date']!=self.date):
                continue
            if arg.find('l')!=-1:
                print "id=\""+thing['id']+"\" thing=\""+thing['content']+"\" urgent=\""+thing['urgent']+"\" status=\""+thing['status']+"\" target_date=\""+thing['target_date']+"\" update_date=\""+thing['update_date']+"\""
            else:
                print thing['id']+". "+thing['content']

    def touch(self,content,urgent,status,target_date,thing_id):
        if cmp(thing_id,"")!=0:
            i = 0;
            len_things = len(self.things)
            while i < len_things:
                if cmp(self.things[i]['id'],thing_id)==0:
                    if cmp(content,"")!=0:
                        self.things[i]['content'] = content
                    if urgent:
                        self.things[i]['urgent'] = urgent
                    if status:
                        self.things[i]['status'] = status
                    if cmp(target_date,"")!=0:
                        if target_date=='today' or target_date=='tod':
                            self.things[i]['target_date'] = self.date
                        elif target_date=='tommorow' or target_date=='tom' or target_date=='nd':
                            sec = time.mktime(time.localtime())+24*60*60
                            time_t = time.localtime(sec)
                            self.things[i]['target_date'] = time.strftime('%Y-%m-%d',time_t)
                        elif target_date=='next_week' or target_date=='nw':
                            sec = time.mktime(time.localtime())+7*24*60*60
                            time_t = time.localtime(sec)
                            self.things[i]['target_date'] = time.strftime('%Y-%m-%d',time_t)
                        elif target_date=='next_month' or target_date=='nm':
                            sec = time.mktime(time.localtime())+30*24*60*60
                            time_t = time.localtime(sec)
                            self.things[i]['target_date'] = time.strftime('%Y-%m-%d',time_t)
                        else:
                            self.things[i]['target_date'] = target_date
                    self.things[i]['update_date'] = self.date
                    break
                i += 1
            if i == len_things:
                print "warning: cannot find specifical thing with id=\""+thing_id+"\""
            else:
                self._flush_single(self.things[i])
                if cmp(status,"1")==0:
                    del self.things[i]
                self._flush('undone')
        # it is a new thing
        else:
            if cmp(content,"")==0:
                print "gtd >>> gtd thing needs content to manager.\n"
                return
            if cmp(urgent,"")==0:
                urgent = "9"
            if cmp(status,"")==0:
                status = "0"
            if target_date=='':
                target_date = self.date
            else:
                if target_date=='today' or target_date=='tod':
                    target_date = self.date
                elif target_date=='tommorow' or target_date=='tom' or target_date=='nd':
                    sec = time.mktime(time.localtime())+24*60*60
                    time_t = time.localtime(sec)
                    target_date = time.strftime('%Y-%m-%d',time_t)
                elif target_date=='next_week' or target_date=='nw':
                    sec = time.mktime(time.localtime())+7*24*60*60
                    time_t = time.localtime(sec)
                    target_date = time.strftime('%Y-%m-%d',time_t)
                elif target_date=='next_month' or target_date=='nm':
                    sec = time.mktime(time.localtime())+30*24*60*60
                    time_t = time.localtime(sec)
                    self.things[i]['target_date'] = time.strftime('%Y-%m-%d',time_t)
            update_date = self.date
            self.things.append({'id':str(self.nextid),'content':content,'urgent':urgent,'status':status,'target_date':target_date,'update_date':update_date,})
            self.nextid += 1
            self._flush_single(self.things[len(self.things)-1])

    def _sort_cmp(self,a,b):
        r = cmp(a['target_date'],b['target_date'])
        if r != 0:
            return r
        else:
            return cmp(a['urgent'],b['urgent'])

    def _flush_single(self,thing):
        if cmp(thing['status'],"0")!=0:
            fp = open(self.data_dir+os.path.sep+"gtd-done.txt","a")
            fp_done_date = open(self.data_dir+os.path.sep+"gtd-done-"+time.strftime("%Y-%m-%d")+".txt","a")
            try:
                fp.write("content = "+thing['content']+"\nurgent = "+thing['urgent']+"\nstatus = "+thing['status']+"\ntarget_date = "+thing['target_date']+"\nupdate_date = "+thing['update_date']+"\n")
                fp_done_date.write("content = "+thing['content']+"\nurgent = "+thing['urgent']+"\nstatus = "+thing['status']+"\ntarget_date = "+thing['target_date']+"\nupdate_date = "+thing['update_date']+"\n")
            finally:
                fp.close()
                fp_done_date.close()
        elif cmp(thing['status'],"0")==0:
            fp = open(self.data_dir+os.path.sep+"gtd-unfinished.txt","a")
            fp.write("content = "+thing['content']+"\nurgent = "+thing['urgent']+"\nstatus = "+thing['status']+"\ntarget_date = "+thing['target_date']+"\nupdate_date = "+thing['update_date']+"\n")
            fp.close()

    def _flush(self,conf):
        if cmp(conf,'all')==0:
            fp_unfinish = open(self.data_dir+os.path.sep+"gtd-unfinished.txt","w")
            fp_done = open(self.data_dir+os.path.sep+"gtd-done.txt",'a+')
            fp_done_date = open(self.data_dir+os.path.sep+"gtd-done-"+time.strftime("%Y-%m-%d")+".txt","a")
            try:
                for thing in self.things:
                    if cmp(thing['status'],"0")!=0:
                        fp_done.write("content = "+thing['content']+"\nurgent = "+thing['urgent']+"\nstatus = "+thing['status']+"\ntarget_date = "+thing['target_date']+"\nupdate_date = "+thing['update_date']+"\n")
                        fp_done_date.write("content = "+thing['content']+"\nurgent = "+thing['urgent']+"\nstatus = "+thing['status']+"\ntarget_date = "+thing['target_date']+"\nupdate_date = "+thing['update_date']+"\n")
                    if cmp(thing['status'],'1')!=0:
                        fp_unfinish.write("content = "+thing['content']+"\nurgent = "+thing['urgent']+"\nstatus = "+thing['status']+"\ntarget_date = "+thing['target_date']+"\nupdate_date = "+thing['update_date']+"\n")
            finally:
                fp_unfinish.close()
                fp_done.close()
                fp_done_date.close()
        elif cmp(conf,'undone')==0:
            fp_undone = open(self.data_dir+os.path.sep+"gtd-unfinished.txt","w")
            for thing in self.things:
                if cmp(thing['status'],'1')!=0:
                    fp_undone.write("content = "+thing['content']+"\nurgent = "+thing['urgent']+"\nstatus = "+thing['status']+"\ntarget_date = "+thing['target_date']+"\nupdate_date = "+thing['update_date']+"\n")
            fp_undone.close();

gtdp = gtd()
gtdp.load_conf()
gtdp.load_file()
cp = cmdpar.cmd_parser(['help',gtdp.help,
                        'ls',gtdp.list,
                        'touch',gtdp.touch],
                       [[],
                        ['',''],
                        ['-t','',
                         '-u','',
                         '-s','',
                         '-td','',
                         '-i','']],
                       'gtd >>> ')
cp.run()
