hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar	-files map_call_api.py,reduce_day_price_files.py,timestamp.py -mapper map_call_api.py -reducer reduce_day_price_files.py -input /market_maker/api_calls/*.rng -output /market_maker/daily_price













