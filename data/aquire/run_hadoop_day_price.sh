hadoop /usr/local/hadoop/share/hadoop/tools/sources/hadoop-streaming-2.7.2-sources.jar \

-file map_call_api.py	-mapper map_call_api.py \
-file reduce_day_price_files.py -mapper reduce_day_price_files.py \
-input /market_maker/api_calls/*.rng -output /market_maker/daily_price.csv













