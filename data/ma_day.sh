cat gdax_11-16_btc.csv | ./map_group_per_range.py --ts_file gdax_ts_bins_btc.json --ts_name Days | sort -k1 -n -t, | ./reduce_ma.py