import requests
url = 'http://127.0.0.1:5000/qr'
response = requests.post(url)
print(response.text)