from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import StructType, StringType, TimestampType
import happybase
#connection details for hbase 
hbase_host = '127.0.0.1'
hbase_table = 'clickstream_table'
hbase_column_families = {
    'click_data': {},
    'geo_data': {},
    'user_agent_data': {}
}
# create a SparkSession
spark = SparkSession.builder \
    .appName("KafkaToHBase") \
    .getOrCreate()
# Read the Kafka stream data
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "clickstream_topic_test") \
    .load()
kafka_df= df.selectExpr("CAST(value AS STRING)")
kafka_df = kafka_df.withColumn('click_id',split(col('value'),',').getItem(0))\
.withColumn('user_id',split(col('value'),',').getItem(1))\
.withColumn('timestamp',split(col('value'),',').getItem(2)).withColumn('timestamp',col('timestamp').cast(StringType()))\
.withColumn('url',split(col('value'),',').getItem(3))\
.withColumn('country',split(col('value'),',').getItem(5))\
.withColumn('city',split(col('value'),',').getItem(6))\
.withColumn('browser',split(col('value'),',').getItem(7))\
.withColumn('os',split(col('value'),',').getItem(8))\
.withColumn('device',split(col('value'),',').getItem(9))
kafka_df=kafka_df.drop('value')
#print(kafka_df.printSchema())
# Write the streaming data to HBase
def write_to_hbase(row):
    connection = happybase.Connection(hbase_host)
    table = connection.table(hbase_table)
    with table.batch() as batch:
        row_key = row["click_id"] 
        batch.put(row_key, {'click_data:user_id': row["user_id"],
                            'click_data:timestamp': row["timestamp"],
                            'click_data:url': row["url"]})
        batch.put(row_key, {'geo_data:country': row["country"],
                            'geo_data:city': row["city"]})
        batch.put(row_key, {'user_agent_data:browser': row["browser"],
                            'user_agent_data:os': row["os"],
                            'user_agent_data:device': row["device"]})
    connection.close()
query= kafka_df.writeStream.format('console').start()
#Write the record
hbase_writer = kafka_df.writeStream.foreach(write_to_hbase).start()
spark.streams.awaitAnyTermination()
hbase_writer.stop()
spark.stop()
query.awaitTermination()
