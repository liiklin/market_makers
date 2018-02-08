import argparse
import numpy as np
import itertools
from datetime import datetime 
from simulate import simulate
from operator import itemgetter
from scipy import optimize


def optimize_portfolio(start_dt, end_dt, symbols):
    d_results = []
    step = 1/float(len(symbols))
    init = [step] * len(symbols)
    args = (start_dt, end_dt, symbols)
    result = optimize.fmin_cg(init, call_simulate_sharpe, args)
    print result
    
def call_simulate_sharpe(x, *args):
    start_dt, end_dt, symbols = args
    result = list(simulate(start_dt, end_dt, symbols, x))
    return result[2]

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
    optimize_portfolio(start_dt, end_dt, symbols)
    
if __name__=="__main__":
    main()