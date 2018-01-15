#!/usr/bin/env python

import sys
from ast import literal_eval as make_tuple
cnt =0
def extract_data(p):
    words = p.split(' ')
    if "Sending" in words:
        print "send_workitems,%s" % words[2]
    elif "Best" in words:
        tdata = make_tuple(''.join(words[8:]))
        print "best,%s,%s" % (words[5], ",".join(map(str,tdata)))
    else:
        values = "".join(words[1:]).split("-")
        if len(values) > 1:
            #print values
            tdata = values[1].split('[')
            print "result,%s,%s" % (values[0].strip(),",".join(map(str,make_tuple(tdata[0]))))
        else:
            print "??", values

# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # split the line into words
    parts = line.split(']')
    if len(parts) > 1:
        extract_data(parts[1])
    
    