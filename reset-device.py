#!/usr/bin/python

import sys
import socket
import string
import time

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

def skip_initial_conf_dialog(ctrl):
    while 1:
        lines, part = ctrl.grab_lines()
        if len(part) > 0 and (part[-1] == ">" or part[-1] == "#"):
            break
        if string.find(part, "Would you like to enter the initial configuration dialog?") != -1:
            ctrl.do_send("no\r")

def device_login(ctrl, password):
    ctrl.wait_for_partial("Password: ")
    
    print "Reached password point."
    ctrl.do_send(password + "\n")
    ctrl.wait_for_line("Password OK\r");
    print "Password accepted."
    
    print "Sleeping for device."
    time.sleep(1)
    
    print "Sending newlines."
    ctrl.do_send("\r\n")
    
    skip_initial_conf_dialog(ctrl)
    
    ctrl.do_send("enable\n")

def reset_device(ip, port, password):
    ctrl = IoController(ip, port)
    
    device_login(ctrl, password)
    
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
    
    skip_initial_conf_dialog(ctrl)
    
    ctrl.close()

if __name__ == "__main__":
    reset_device(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])


