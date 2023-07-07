import csv
import requests
import random
import string
from datetime import datetime
from user_agents import parse

# number of records to generate
num_records = 1000
api_url = 'http://ip-api.com/csv/{}'
csv_file_path = 'user_details.csv'

# function to generate random user data
def generate_user_data():
    user_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    url = 'https://' + ''.join(random.choices(string.ascii_lowercase, k=10)) + '.com'
    ip_address = '.'.join(str(random.randint(0, 255)) for _ in range(4))
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    parsed_user_agent = parse(user_agent)
    browser = parsed_user_agent.browser.family
    os = parsed_user_agent.os.family
    device = parsed_user_agent.device.family
    click_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return {"click_id": click_id, "user_id": user_id, "timestamp": timestamp, "url": url, "ip_address": ip_address, "browser": browser, "os": os, "device": device}
def get_location(ip):
    try:
        response = requests.get(api_url.format(ip))
        if response.status_code == 200:
            data = response.text.split(',')
            if len(data) >= 6:
                country = data[1]
                city = data[5]
                return country, city
    except requests.exceptions.RequestException:
        pass
    return None, None
with open(csv_file_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    for _ in range(num_records):
        user_data = generate_user_data()
        click_id = user_data['click_id']
        user_id = user_data['user_id']
        timestamp = user_data['timestamp']
        url = user_data['url']
        ip_address = user_data['ip_address']
        country, city = get_location(ip_address)
        browser = user_data['browser']
        os = user_data['os']
        device = user_data['device']
        writer.writerow([click_id, user_id, timestamp, url, ip_address, country, city, browser, os, device])

print("CSV file created with at least 1000 records.")