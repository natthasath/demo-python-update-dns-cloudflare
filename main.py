import requests
import json
from decouple import config

# Replace these values with your own
api_key = config("CLOUDFLARE_API_KEY")
zone_identifier = config("CLOUDFLARE_ZONE_ID")
record_id = config("CLOUDFLARE_RECORD_ID")
record_name = config("CLOUDFLARE_RECORD_NAME")  # Replace with your record name
new_ip = config("CLOUDFLARE_NEW_IP")  # Replace with the new IP address

headers = {
    'Authorization' : api_key,
    'Content-Type': 'application/json'
}

# Fetch the current record details
url = f'https://api.cloudflare.com/client/v4/zones/{zone_identifier}/dns_records/{record_id}'
response = requests.get(url, headers=headers)
data = response.json()

# Update the record with the new IP
if response.status_code == 200:
    current_record = data['result']
    current_record['content'] = new_ip

    # Make PUT request to update the record
    update_response = requests.put(url, headers=headers, data=json.dumps(current_record))
    
    if update_response.status_code == 200:
        print(f"DNS record updated successfully: {record_name} now points to {new_ip}")
    else:
        print(f"Failed to update DNS record: {update_response.status_code} - {update_response.text}")
else:
    print(f"Failed to fetch DNS record: {response.status_code} - {response.text}")
