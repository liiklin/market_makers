import argparse
import numpy as np
import itertools
from datetime import datetime 
from simulate import simulate
from operator import itemgetter


def optimize(start_dt, end_dt, symbols):
    d_results = []
    ls_alloc = generate_allocations(len(symbols))
    for alloc in ls_alloc:
        result = list(simulate(start_dt, end_dt, symbols, alloc))
        sa = dict(zip(symbols, alloc))
        label = ",".join(["%s:%s" % (k, v) for (k, v) in sa.iteritems() ])
        d_result = {"label":label,"sharpe":result[2], "std_ret":result[0],"avg_daily_ret":result[1], "cum_ret":result[3],"alloc":alloc }
        d_results.append(d_result)
    sorted_results = sorted(d_results, key=itemgetter("sharpe"), reverse=True)
    for item in  sorted_results[0:20]:
        print "alloc:%s, sharpe:%s, cum_ret:%s  " %(item["label"], item["sharpe"], item["cum_ret"])

    
def generate_allocations(count, by=.1, min=0, max=1):
    allocations = []
    l_alloc_ranges = []
    alloc_range = np.arange(min, max + by,by)
    for x in range(0,count-1, 1):
        l_alloc_ranges.append(alloc_range)
    all_products = itertools.product(*l_alloc_ranges)
    valid_allocations = []
    cnt = 0
    for item in all_products:
        cnt+=1
        l_item = list(item)
        l_item.append(1-sum(l_item))
        if sum(l_item) == 1:
            valid_allocations.append(l_item)
    valid_allocations = [x for x in valid_allocations if not any(y < 0 for y in)]
    return valid_allocations
        

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("start_year", type=int)
    parser.add_argument("start_month", type=int)
    parser.add_argument("start_day", type=int)
    parser.add_argument("end_year", type=int)
    parser.add_argument("end_month", type=int)
    parser.add_argument("end_day", type=int)
    parser.add_argument("symbols", type=str, help="Comma seperated list of symbols to optimize")
    args = parser.parse_args()
    
    start_dt = datetime(year=args.start_year, month=args.start_month, day=args.start_day)
    end_dt = datetime(year=args.end_year, month=args.end_month, day=args.end_day)
    symbols = args.symbols.split(',')
    optimize(start_dt, end_dt, symbols)
    
if __name__=="__main__":
    main()