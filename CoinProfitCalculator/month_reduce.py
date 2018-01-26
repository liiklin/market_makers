#!/usr/bin/python
import fileinput
from datetime import datetime

def main():
        last_ym = (0,0)
        current_ym_ttl = 0
        for line in fileinput.input():
            parts = line.split(',')
            if not "summary" in parts[0]:
                tx_date = datetime.strptime(parts[0], "%Y-%m-%dT%H:%M:%S.%fZ")
                current_amount = float(parts[1])
                current_ym = (tx_date.year, tx_date.month)
                
                #print current_ym, current_amount
                if not current_ym == last_ym:
                    print "%s, %s, %s" % (last_ym[0],last_ym[1], current_ym_ttl)
                    last_ym = current_ym
                    current_ym_ttl = current_amount
                else:
                    current_ym_ttl += current_amount
                    
        print "%s, %s, %s" % (last_ym[0],last_ym[1], current_ym_ttl)
if __name__ =="__main__":
    main()