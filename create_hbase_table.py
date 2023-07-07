import happybase
# hbase connection settings
hbase_host = "127.0.0.1" 
hbase_table = "clickstream_table"
click_data_cf = "click_data"
geo_data_cf = "geo_data"
user_agent_data_cf = "user_agent_data"
connection = happybase.Connection(host=hbase_host)
connection.create_table(
    hbase_table,
    {
        click_data_cf: dict(),
        geo_data_cf: dict(),
        user_agent_data_cf: dict()
    }
)

connection.close()
