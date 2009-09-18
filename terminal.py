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

