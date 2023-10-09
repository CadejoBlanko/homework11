import requests

contact_id = 1 
url = f'http://127.0.0.1:8000/contacts/{contact_id}'

payload = {
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "987654321",
    "email": "john.doe@example.com",
    "birthdate": "1990-01-01"
}

response = requests.put(url, json=payload)

print(response.status_code)
print(response.json())