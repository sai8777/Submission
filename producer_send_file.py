from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='localhost:9092')
topic = 'clickstream_topic_test'
csv_file_path = '/home/hp/Submission/user_details.csv'
# read file
with open(csv_file_path, 'r') as file:
    for line in file:
        producer.send(topic, value=line.encode())
producer.close()
