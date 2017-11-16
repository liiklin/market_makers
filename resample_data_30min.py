from pyalgotrade.bitcoincharts import barfeed
from pyalgotrade.tools import resample
from pyalgotrade import bar
import argparse
import datetime


def main(file_in, file_out, freq):
    barFeed = barfeed.CSVTradeFeed()
    barFeed.addBarsFromCSV(file_in, fromDateTime=datetime.datetime(2014, 1, 1))
    resample.resample_to_csv(barFeed, bar.Frequency.MINUTE*freq, file_out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", help="file to extract data from")
    parser.add_argument("--out", help="file to save resampled data to")
    parser.add_argument("--freq", help="resample freq in minutes (defaults to 30 min)", default=30 )
    args = parser.parse_args()

    main(args.file)