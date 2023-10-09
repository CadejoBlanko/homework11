import requests

contact_id = 1
url = f'http://127.0.0.1:8000/contacts/{contact_id}'

response = requests.get(url)

print(response.status_code)
print(response.json())