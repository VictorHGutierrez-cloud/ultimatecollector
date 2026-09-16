"""
Testar endpoint de policy_periods/change_status
"""
import requests
import json

url = "https://api.eu2.demo.factorial.dev/api/2026-07-01/resources/payroll/policy_periods/change_status"

payload = {
    "status": "preparation",
    "notify_employee": True
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-api-key": "eyJraWQiOiJmYWN0b3JpYWwtaWQiLCJhbGciOiJFUzI1NiJ9.eyJpYXQiOjE3NzE4ODQ4NjQsImV4cCI6MjA4NzQ1NDM4NCwianRpIjoiNzBjZWRiMzktODNiZC00MDEwLWJhYjgtMmZiMjRjNjBkNDBhIiwiY2VsbCI6ImF6dXJlLWRlbW8tZ3djLWV1MiIsImNvbXBhbnlfaWQiOjU1NDcxfQ.vwbec8pZc1ybTnGchYRaZMacnlndqXFh8WxjlJ_gFNfQ5BIYhUQjFdPhU_-ZwyvffqYyAgI5ZdaBomfKQx3cCg"
}

print("=" * 60)
print("TESTANDO POLICY_PERIODS/CHANGE_STATUS")
print("=" * 60)
print()
print(f"URL: {url}")
print(f"Payload: {json.dumps(payload, indent=2)}")
print()

response = requests.post(url, json=payload, headers=headers)

print(f"Status Code: {response.status_code}")
print()
print("Resposta:")
print(response.text)
print()

if response.status_code == 200:
    try:
        data = response.json()
        print("Resposta JSON formatada:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except:
        pass
