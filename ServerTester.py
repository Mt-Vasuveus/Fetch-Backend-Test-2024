import requests

# Use this to send requests to the server while it's running


add_url = "http://127.0.0.1:8000/add"
spend_url = "http://127.0.0.1:8000/spend"
balance_url = "http://127.0.0.1:8000/balance"

r = requests.post(add_url, json={
    "payer": "DANNON", 
    "points": 300,
    "timestamp": "2022-10-31T10:00:00Z" })

print(r.status_code)
print(r)

r = requests.post(add_url, json={
    "payer": "UNILEVER",
	"points": 200,
	"timestamp": "2022-10-31T11:00:00Z" })
print(r.status_code)
print(r)

r = requests.post(add_url, json={
    "payer": "DANNON",
	"points": -200,
	"timestamp": "2022-10-31T15:00:00Z" })
print(r.status_code)
print(r)

r = requests.post(add_url, json={
    "payer": "MILLER COORS",
	"points": 10000,
	"timestamp": "2022-11-01T14:00:00Z" })
print(r.status_code)
print(r)

r = requests.post(add_url, json={
    "payer": "DANNON",
	"points": 1000,
	"timestamp": "2022-11-02T14:00:00Z" })
print(r.status_code)
print(r)


r = requests.post(spend_url, json={
	"points": 5000 })
print(r.status_code)
print(r)

r = requests.get(balance_url)
print(r.status_code)
print(r)
