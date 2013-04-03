# Copyright (c) ZhiQiang Fan 2012, All rights reserved.
# this file is used to parse command line arguments

import readline

class cmd_parser:
    def __init__(self,cmd2func,arg_lists,prompt='# '):
	print 'cmdpar version 0.1, copyright (c) ZhiQiang Fan 2012'
        self.cmd2func = cmd2func
        self.arg_lists = arg_lists
        self.prompt = prompt

    def run(self):
        while True:
            cmd = raw_input(self.prompt)
            if cmd=='exit' or cmd=='e' or cmd=='quit' or cmd=='q':
                break
            self._parse_cmd(cmd)

    def _parse_cmd(self,cmd):
        self.func_index = 0;
        # check each cmd
        len_cmd2func = len(self.cmd2func)
        while self.func_index < len_cmd2func:
            if cmd.startswith(self.cmd2func[self.func_index]):
                self._parse_arg(cmd[len(self.cmd2func[self.func_index]):])
                # invoke func with args
                real_arg = []
                i = 1
                length = len(self.arg_lists[self.func_index/2])
                while i < length:
                    real_arg.append(self.arg_lists[self.func_index/2][i])
                    i += 2
                self.cmd2func[self.func_index+1](*real_arg)
                break;
            self.func_index += 2;

    def _parse_arg(self,argv):
        length = len(self.arg_lists[self.func_index/2])
        if length==0:
            return
        # initialize the arg value list
        i = 1
        while i < length:
            self.arg_lists[self.func_index/2][i]=''
            i += 2
        # check if contains following arguments
        if argv.strip()=='':
            return
        key = ''
        value = ""
        words = argv.split(' ')
        # check each words
        i = 0
        words_len = len(words)
        arglist_len = len(self.arg_lists[self.func_index/2])
        prev_key_index = 0 
        while i < words_len:
            j = 0
            # argvs[i] is a arg, it could be a reg!
            while j < arglist_len:
                if words[i] == self.arg_lists[self.func_index/2][j]:
                    # if there is a prev key need to handle
                    if key.strip()!='':
                        if value.strip()=='':
                            print key+' need a value, but here tempory set to null'
                            # set value to key
                        self.arg_lists[self.func_index/2][prev_key_index+1] = value
                        value = ''
                    key = words[i]
                    prev_key_index = j
                    # no need to search rest argument in arg_list
                    break;
                # jump to next argument
                j += 2
            # search ends, check find whether a argument or a value words
            if j >= arglist_len:
                # append to value
                if value.strip()=='':
                    value = words[i]
                else:
                    value = value+' '+words[i]
            i += 1
        # while loop is end regulary
        if i >= words_len and (len(self.arg_lists[self.func_index/2]) > 1):
            self.arg_lists[self.func_index/2][prev_key_index+1] = value
