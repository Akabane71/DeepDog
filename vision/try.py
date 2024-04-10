import requests
url = 'http://192.168.1.101:5000/qr'
response = requests.post(url)
print(response.text)