# Data Pipeline for clickstream data


To build a real-time data pipeline that streams data from Kafka, processes the data in a data store, and indexes the processed data in Elasticsearch
- Ingest Clickstream data from kafka 
- Store ingested data in Apache Hbase the column family considered are Row key: Unique identifier for each click event.
Column families:
click_data: user ID, timestamp, and URL.
geo_data:country and city
user_agent_data:browser, operating system, and device
- Periodically process the stored clickstream data in any data store by aggregating the data by URL and country,and calculating the number of clicks, unique users, and average time spent on each URL by users from each country.
- Index the processed data in Elasticsearch.
- ## Assumption
- The data stream details are stored in a csv file .

## Tech

The following project uses no open source projects to work properly:

- Apache Spark - v3.0.3 - To transform and process data!
- Apache Hbase  - v2.5.5 - Data store for clickstream data
- Apche Kafka -v2.1.2 - To stream Data
- Elastic search v7.16.3 - To index d store final data
- Python 3 - Scripting language 

## Installation

- Apache Spark installation - https://spark.apache.org/news/index.html
- Apache Kafka installation - https://kafka.apache.org/downloads
- Apache Hbase installation - https://hbase.apache.org/downloads.html
- Elastic search installation -https://www.elastic.co/downloads/elasticsearch

## Dependencies
- happybase -To connect to hbase from Python 
```sh
pip install happybase
```
## Packages
- org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.3
- org.apache.kafka:kafka-clients:2.8.1
- org.apache.hbase:hbase-client:2.5.5 
```sh
./bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.3,org.apache.kafka:kafka-clients:2.8.1,org.apache.hbase:hbase-client:2.5.5 /home/hp/kafka_hbase.py
```
## jars
- elasticsearch-spark-30_2.12-7.16.3.jar

## Steps to run the code
Note : Start the server for Apache kafka and Apache Hbase 
Create hbase table:
```
python create_hbase_table.py
```
Create sample data in csv format for streaming 
```sh
python sampledata.py
```
Start the producer and consumer to read the data from stream and write the data to Hbase:
- use producer_send_file.py to send file 
- use producer_folder_dir.py to send csv file in a directory 
```sh 
./bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.3,org.apache.kafka:kafka-clients:2.8.1,org.apache.hbase:hbase-client:2.5.5 /home/hp/kafka_hbase.py
```
```sh 
python producer_send_file.py
```
To read data from hbase and store it elasticsearch with indexing:
```sh
./bin/spark-submit --jars  elasticsearch-spark-30_2.12-7.16.3.jar /home/hp/hbase_spark.py
```

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
