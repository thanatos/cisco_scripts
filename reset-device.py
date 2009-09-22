#!/usr/bin/python

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
import sys
import time

import common
import ioctrl
import terminal

def wait_for_remote(sock, callback):
    while 1:
        lines, last = grab_list

def watch_for_vlan(lines, partial, my_data):
    for l in lines:
        if string.find(l, "vlan.dat") != -1:
            return (False, True, my_data)
        if string.find(l, "Directory of flash:/") == 0:
            my_data = True
        
    if len(partial) > 0 and partial[-1] == "#":
        if my_data == True:
            return (False, False, my_data)
    return (True, None, my_data)

# my_data = (what to look for, False)
def wait_for_prompt(lines, partial, my_data):
    for l in lines:
        if string.find(l, my_data[0]) != -1:
            my_data = (my_data[0], True)
    if len(partial) > 0 and partial[-1] == "#":
        return (True, None, my_data)
    return (False, None, my_data)

def reset_device(ip, port, password):
    ctrl = ioctrl.IoController(ip, port)
    
    common.device_login(ctrl, password)
    
    ctrl.do_send("dir\n")
    
    ret = ctrl.wait_for_special(watch_for_vlan, False)
    if ret == True:
        print "This appears to be a switch, and it has a vlan.dat. Deleting..."
        ctrl.do_send("delete vlan.dat\n\n\n")
        ctrl.wait_for_special(wait_for_prompt, ("[confirm]", False))
    else:
        print "This does not seem to be a switch. (No vlan.dat)"
    
    ctrl.do_send("erase startup-config\n\n")
    ctrl.do_send("reload\n")
    while 1:
        lines, part = ctrl.grab_lines()
        if string.find(part, "[confirm]") != -1:
            break
        if string.find(part, "[yes/no]") != -1:
            ctrl.do_send("no\n")
    ctrl.do_send("\n")
    
    print "Device should be restarting. Waiting for prompt."
    
    ctrl.wait_for_line("Press RETURN to get started!\r")
    ctrl.do_send("\r\n")
    
    common.skip_initial_conf_dialog(ctrl)
    
    ctrl.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "Usage:"
        print "\treset-device.py hostname port password"
    else:
        reset_device(sys.argv[1], int(sys.argv[2]), sys.argv[3])


