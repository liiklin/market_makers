#!/usr/bin/env python

import sys
import json, requests
cnt =0
# input comes from STDIN (standard input)
for url in sys.stdin:
    resp = requests.get(url=url)
    data = json.loads(resp.text.replace("cb(","").replace(");",""))
    for price in data['bpi']:
        print '%s,%s' % (price[0],price[1])
    
#print "found ", cnt, "lines"
