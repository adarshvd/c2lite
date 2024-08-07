import requests

response = requests.get('http://localhost:5005/get_devices_types')
print(response.json())
# Check for successful response
if response.status_code == 200:
  # Print the raw text content
  print(response.text)
else:
  print(f"Error getting data: {response.status_code}")