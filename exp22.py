import requests

url = 'http://dongaars.donga.com:8001/117776449/117776449'

temp = requests.get(url)
print(temp.content.decode('utf-8'))
print(temp.headers)