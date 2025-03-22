import requests

url = "http://127.0.0.1:5000/cotacao/"

dados = {"tamanho": 120, "ano": 2001, "garagem": 2}

auth = requests.auth.HTTPBasicAuth("admin", "admin")

response = requests.post(url, json=dados, auth=auth)

response.status_code

response.text
