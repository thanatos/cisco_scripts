# Copyright (c) 2009 Roy Wellington
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import socket
import string

import terminal

class IoController:
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))
        self.lines = []
        self.partial = ""
    
    def grab_lines(self):
        data = self.partial + self.sock.recv(4096)
        got_lines = string.split(data, "\n")
        for l in got_lines[:-1]:
            terminal.show_line("in", l)
            self.lines.append(l)
        self.partial = got_lines[-1]
        return (got_lines[:-1], got_lines[-1])
    
    def do_send(self, data):
        lines = string.split(data, "\n")
        if lines[-1] == "":
            lines = lines[:-1]
        for l in lines:
            terminal.show_line("out", l+"\n")
        self.sock.sendall(data)
    
    def wait_for_partial(self, partial_text):
        while 1:
            self.grab_lines()
            if self.partial == partial_text:
                break
    
    def wait_for_line(self, line_text):
        while 1:
            glines, gpartial = self.grab_lines()
            for l in glines:
                if l == line_text:
                    return glines, gpartial
    
    def wait_for_special(self, callback, my_data):
        while 1:
            new_lines, new_partial = self.grab_lines()
            cont, ret, my_data = callback(new_lines, new_partial, my_data)
            if cont == False:
                return ret
    
    def close(self):
        self.sock.close()

