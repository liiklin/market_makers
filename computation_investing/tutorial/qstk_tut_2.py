import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
import sys 
import pandas as pd
def load_data():
    np_data = np.loadtxt('example-data.csv', delimiter=",", skiprows=1)
    np_price = np_data[:, 3:]
    np_dates = np.int_(np_data[:, 0:3])
    ls_symbols = ["$SPX", "XOM", "GOOG", "GLD"]
    sys.stdout.write("Length price: %s dates: %s symbols: %s" %(len(np_price), len(np_dates), len(ls_symbols)))
    df = pd.DataFrame({"dates":np_dates.tolist(), "symbols":ls_symbols, "price":np_price.tolist()})
    sys.stdout.write(json.dumps(df))
    


if "__main__" in __name__:
    load_data()
