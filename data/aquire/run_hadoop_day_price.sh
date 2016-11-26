hdfs dfs -rm -r /market_maker/daily_price
hdfs dfs -rm /market_maker/api_calls/*
rm *.rng
./gen_coindesk_api_calls.py -s 2013-02-1 -e 2016-11-01 -c 20
hdfs dfs -put *.rng /market_maker/api_calls
rm *.rng
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar	-files map_call_api.py,reduce_day_price_files.py -mapper map_call_api.py -reducer reduce_day_price_files.py -input /market_maker/api_calls/*.rng -output /market_maker/daily_price













