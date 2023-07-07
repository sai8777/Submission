from kafka import KafkaProducer
import os
import csv
producer = KafkaProducer(bootstrap_servers='localhost:9092')
topic = 'clickstream_topic_test'
# path to the csv fplder
csv_folder_path = '/home/hp/sub_data/'

for filename in os.listdir(csv_folder_path):
    if filename.endswith('.csv'):
        csv_file_path = os.path.join(csv_folder_path, filename)
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                message = ','.join(row).encode('utf-8')
                producer.send(topic, value=message)
        print("csv file sent to kafka")
producer.close()


