#!/usr/bin/env python

import sys,argparse


if __name__ == "__main__":
    # input comes from STDIN (standard input)
    for line in sys.stdin:
        # remove leading and trailing whitespace
        line = line.strip()
        # split the line into words
        parts = line.split(',')
        if len(parts) > 1:
            if parts[0] == "result":
                print ",".join(parts[1:])
            
    
    