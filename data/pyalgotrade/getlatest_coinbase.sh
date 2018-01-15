#wget http://api.bitcoincharts.com/v1/csv/coinbaseUSD.csv.gz
#gzip -d coinbaseUSD.csv.gz
#mv coinbaseUSD.csv /home/mcstar/data/
#./resample_to_-m_min.py -s 12 -e 2016-12-31 -m 5
#./resample_to_-m_min.py -s 12 -e 2016-12-31 -m 30
date
echo 'Before download : '
wc -l 30min-BTC-2016.csv
wc -l last90days_BTC.csv
tail 30min-BTC-2016.csv | ./latest_data_map.py | ./latest_data_reduce.py >> 30min-BTC-2016.csv
echo 'After : '
wc -l 30min-BTC-2016.csv     
cat 30min-BTC-2016.csv| ./last90days_map.py > last90days_BTC.csv
wc -l last90days_BTC.csv