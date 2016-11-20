#!/usr/bin/env python

import sys
cnt =0
# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # split the line into words
    words = line.split(',')
    # increase counters
    print '%s' % (words[1])
    cnt +=1
#print "found ", cnt, "lines"