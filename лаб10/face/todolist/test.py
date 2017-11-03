import requests

response = requests.post('http://127.0.0.1:8000/get-token/', data={'username':'anmik98','password':'12345MAS'})
print (response)
print (response.json())
