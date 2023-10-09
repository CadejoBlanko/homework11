import requests

url = 'http://127.0.0.1:8000/contacts/'

response = requests.get(url)

print(response.status_code)
print(response.json())