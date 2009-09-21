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

def replace_unprintables(line):
    out = ""
    for c in line:
        o = ord(c)
        if o < 32 or o > 127:
            out += "\x1b[2;37m<" + ("0" + hex(o)[2:])[-2:] + ">\x1b[0m"
        else:
            out += c;
    return out

def show_line(dir, line):
    if dir == "in":
        print "\x1b[1;32min  >>\x1b[0m ",
    elif dir == "out":
        print "\x1b[1;34mout <<\x1b[0m ",
    else:
        print "\x1b[1m" + (dir + "    ")[-4:] + "==\x1b[0m",
    
    line = replace_unprintables(line)
    print line

