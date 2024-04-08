import requests

url = 'http://localhost:5000'
data = {
    'name':'lishun',
    'deepdog':'2024'
}
response = requests.post(url,data=data)
print(response.text)


