#! /usr/bin/env python

import urllib2
import os
import sys
import time
import argparse
import traceback
import requests
from BeautifulSoup import BeautifulSoup

class iciba_parser():
    word = ''
    word_interpret = []

    def _get_page_content(self):
        up = urllib2.urlopen('http://www.iciba.com/'+self.word)
        self.content = up.readlines()
        up.close()

    def _get_pronunce(self, bs):
        p = ""
        tags = bs.findAll("span",attrs={"class":"fl"})
        for tag in tags:
            p += tag.text
        return [p]

    def _add_space(self, text, pattern):
        """add a single space between pattern and alpha in text."""
        l = text.find(pattern)
        if l == -1:
            return text
        result = text[:l]
        r = l + len(pattern)
        if l > 0 and text[l-1].isalpha():
            result += " "
        result += pattern
        if r < len(text) and text[r].isalpha():
            result += " "
        result += text[r:]
        return result

    def _get_collins_interpret(self,bs):
        interprets = []
        tags = bs.findAll("div", attrs={"class":"collins_en_cn"})
        for tag in tags:
            interpret = []
            st = tag.findAll("span", attrs={"class":"st"})
            if not st:
                continue
            interpret.append(st[0].contents[0].strip())
            ch = tag.findAll("span", attrs={"class":"text_blue"})
            interpret.append(ch[0].text)
            cap = tag.findAll("div", attrs={"class":"caption"})
            if ch[0].text == "":
                continue
            else:
                eng = cap[0].text.split(ch[0].text)[-1].split("&nbsp;")[0]
            #eng = eng.replace(self.word, " "+self.word+" ")
            interpret.append(eng)
            examples = []
            all_lis = tag.findAll("li")
            except_lis = tag.findAll("li", attrs={"class":"explain_r"})
            lis = [li for li in all_lis if li not in except_lis]
            for li in lis:
                ps = li.findAll("p")
                for p in ps:
                    text = self._add_space(p.text, self.word)
                    #text = p.text.replace(self.word, " "+self.word+" ")
                    examples.append(text)
            interpret.append(examples)
            interprets.append(interpret)
        return interprets

    def _get_word_title(self, bs):
        title = bs.findAll("h1", attrs={"id":"word_name_h1"})
        return title[0].text

    def get_interpret(self, word="empty"):
        r = requests.get("http://www.iciba.com/"+word)
        content = r.content.replace("<b>","")
        content = content.replace("</b>","")
        bs = BeautifulSoup(content)
        self.word = self._get_word_title(bs)
        self.word_interpret = []
        self.word_interpret.append(self._get_pronunce(bs))
        interpret = self._get_collins_interpret(bs)
        self.word_interpret.extend(interpret)
        return self.word_interpret
        

class Translator():
    def __init__(self):
        self.home_dir = os.path.expanduser('~')+os.path.sep
        self.data_dir = self.home_dir+'appdata'+os.path.sep+'dict'+os.path.sep
        self.word_list_file = self.data_dir+'word_list.txt'
        self.word_map_file = self.data_dir+'word_map.txt'
        self.parser = iciba_parser()
        self.word = ''
        self.interprets = []
        self.word_list = {}
        self.interprets_from_file = False
        self.word_map = {}

        self.load_word_list()
        self.load_word_map()

    def _read_from_file(self, word):
        try:
            fp = open(self.data_dir+word+'.txt')
            self.interprets = fp.readlines()
            fp.close()
        except Exception as e:
            print "ERROR: read file error: %s" % word
            self.interprets = []

    def find(self,word='empty',net='False'):
        self.interprets_from_file = False
        self.word = word
        if net:
            self.interprets = self.get_interpret_from_net(word)
        else:
            self.interprets = self._read_from_file(word)
            if self.interprets:
                self.interprets_from_file = True
            else:
                self.interprets = self.get_interpret_from_net(word)
        if word in self.word_list:
            self.word_list[word]['count'] += 1
            self.word_list[word]['update_time'] = time.strftime('%Y-%m-%d-%H:%M:%S')
        else:
            word_attr = {'count':1,'update_time':time.strftime('%Y-%m-%d-%H:%M:%S')}
            self.word_list[word] = word_attr
        return

        if word in self.word_list:
            self.word_list[word]['count'] += 1
            self.word_list[word]['update_time'] = time.strftime('%Y-%m-%d-%H:%M:%S')
            if not net:
                self.interprets_from_file = True
                fp = open(self.data_dir+word+'.txt')
                self.interprets = fp.readlines()
                fp.close()
            else:
                self.interprets = self.get_interpret_from_net(word)
        else:
            self.interprets = self.get_interpret_from_net(word)
            word_attr = {'count':1,'update_time':time.strftime('%Y-%m-%d-%H:%M:%S')}
            self.word_list[word] = word_attr

    def get_interpret_from_net(self, word):
        try:
            interpret = self.parser.get_interpret(word)
        except Exception as e:
            traceback.print_exc()
            return []
        return interpret

    def print_interprets(self):
        print self.word
        if self.interprets_from_file:
            for line in self.interprets:
                print line.encode('utf-8'),
        else:
            for interpret in self.interprets:
                if len(interpret) == 1:
                    print interpret[0]+'\n'
                    continue
                print interpret[0],interpret[1],interpret[2]
                for example in interpret[3]:
                    print example
                print ''

    def save_interprets(self,overwrite=False):
	if self.interprets_from_file:
	    return
        if len(self.interprets) == 0:
            return
        file_name = self.data_dir+self.word+'.txt'
        if os.path.isfile(file_name) and not overwrite:
            return
        fp = open(file_name,'a')
        for interpret in self.interprets:
            if len(interpret) == 1:
                fp.write(interpret[0]+os.linesep+os.linesep)
                continue
            fp.write(interpret[0]+' '+interpret[1]+' '+interpret[2]+os.linesep)
            for example in interpret[3]:
                fp.write(example+os.linesep)
            fp.write(os.linesep)
        fp.close()

    def load_word_map(self):
        fp = open(self.word_map_file,'a+')
        word_map_lines = fp.readlines()
        fp.close()
        for word_map_line in word_map_lines:
            words = word_map_line.split()
            self.word_map[words[0]] = words[1]
    
    def load_word_list(self):
        fp = open(self.word_list_file,'a+')
        lines = fp.readlines()
        fp.close()
        for line in lines:
            attr = line.split()
            word_attr = {'count': int(attr[1])}
            if len(attr) > 2:
                word_attr['update_time'] = attr[2]
            else:
                word_attr['update_time'] = time.strftime('%Y-%m-%d-%H:%M:%S')
            self.word_list[attr[0]] = word_attr

    def dump(self):
        self.save_interprets()
        self.save_word_list()
        self.save_word_map()

    def save_word_list(self):
        fp = open(self.word_list_file,'w')
        for word in self.word_list:
            fp.write(word+' '+str(self.word_list[word]['count'])+' '+self.word_list[word]['update_time']+os.linesep)
        fp.close()

    def save_word_map(self):
        fp = open(self.word_map_file,'w')
        for word in self.word_map:
            fp.write(word+' '+self.word_map[word]+os.linesep)
        fp.close()

def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    dic = Translator()
    args = argparse.ArgumentParser(
        description='a simple dict using collins',
        prog='dic')
    args.add_argument('-n', '--net',
                      action='store_true',
                      help='force to get interpret from internet',
                      default='False')
    args.add_argument('word', help='word to be interpreted')
    args.parse_args(sys.argv[1:], args)
    dic.find(args.word,args.net)
    dic.print_interprets()
    if not dic.interprets_from_file:
        save_opt = raw_input("save this word? yes/no: ")
        if save_opt == "yes" or save_opt == 'y':
            dic.dump()
    else:
        dic.save_word_list()
    
if __name__ == '__main__':
    main()
