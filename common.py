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

import string
import time

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

