import requests

data = {
    "code": "print(1)",
    "checker": "print(2)"
}

res = requests.post("http://localhost:8087", data=data).json()
print(res)