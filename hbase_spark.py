from pyspark.sql import SparkSession,Row
from pyspark.sql.functions import *
import happybase
#Configure nodes and port for elastic search 
spark = SparkSession.builder \
    .appName("HBaseReadExample")\
    .config("spark.es.nodes", "localhost") \
    .config("spark.es.port", "9200") \
    .getOrCreate()

#Cnnection details for hbase 
hbase_host = "127.0.0.1" 
hbase_table = "clickstream_table" 

# Create a connection to HBase
connection = happybase.Connection(host=hbase_host)
table = connection.table(hbase_table)

# Fetch the data from HBase
rows = table.scan()

# Convert the data to an RDD
rdd = spark.sparkContext.parallelize(rows).map(lambda x: Row(_1=x[0], _2=x[1]))

# Create a DataFrame from the RDD
read_df = spark.createDataFrame(rdd)
#print(df.count())
#print(df.printSchema())
exploded_read_df=read_df.select(col("_1").cast('string'), explode("_2").alias('key','value'))
#k.show()
exploded_read_df=exploded_read_df.select(col('_1'),col('key').cast('string'),col('value').cast('string'))
transformed_df=exploded_read_df.groupBy('_1').pivot('key').agg(first(col('value')).alias("value"))
#transformed_df.write.parquet('/home/hp/sub')
#df=jk
column_change_df=transformed_df.withColumnRenamed('_1','click_data').\
    withColumnRenamed('click_data:timestamp','timestamp').\
    withColumnRenamed('click_data:url','url').\
    withColumnRenamed('click_data:user_id','user_id').\
    withColumnRenamed('geo_data:city','city').\
    withColumnRenamed('geo_data:country','country').\
    withColumnRenamed('user_agent_data:browser','browser').\
    withColumnRenamed('user_agent_data:device','device').\
    withColumnRenamed('user_agent_data:os','os')
column_change_df=column_change_df.drop('click_data:timestamp')
column_change_df.createOrReplaceTempView("clickstream")
aggregated_data = spark.sql("""SELECT,url,country,COUNT(*) AS click_count,COUNT(DISTINCT user_id) AS unique_users,AVG(timestamp) AS avg_time_spent FROM clickstream GROUP BY url,country""")
aggregated_data.show()
aggregated_data.write.format("org.elasticsearch.spark.sql") \
    .option("es.resource", "mydata/_doc") \
    .option("es.nodes.wan.only", "true") \
    .mode("append") \
    .save()
# Close the HBase connection
connection.close()
# Stop the Spark session
spark.stop()
