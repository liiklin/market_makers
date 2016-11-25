#!/bin/bash

# the default node number is 3
N=${1:-3}


# start hadoop master container
sudo docker rm -f hadoop-master &> /dev/null
echo "start hadoop-master container..."
sudo docker run -itd \
                --net=hadoop \
                -p 50070:50070 \
                -p 8088:8088 \
		-v /hdfs/master:/root/hdfs \
                --name hadoop-master \
                --hostname hadoop-master \
                kiwenlau/hadoop:1.1 &> /dev/null

		#-v /hdfs/master:/root/hdfs \

# start hadoop slave container
i=1
while [ $i -lt $N ]
do
	sudo docker rm -f hadoop-slave$i &> /dev/null
	echo "start hadoop-slave$i container..."
	sudo docker run -itd \
	                --net=hadoop \
			-v /hdfs/slave$i:/root/hdfs \
			-p $((19887+$i)):19888 \
			-p $((8041+$i)):19888 \
	                --name hadoop-slave$i \
	                --hostname hadoop-slave$i \
	                kiwenlau/hadoop:1.1
# &> /dev/null
	i=$(( $i + 1 ))
done 

#-v /hdfs/slave$i:/root/hdfs \
# get into hadoop master container
sudo docker exec -it hadoop-master bash
