import requests

url = 'http://127.0.0.1:8000/contacts/'

payload = {
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "123456789",
    "email": "john.doe@example.com",
    "birthdate": "1990-01-01"
}

response = requests.post(url, json=payload)

print(response.status_code)
print(response.json())