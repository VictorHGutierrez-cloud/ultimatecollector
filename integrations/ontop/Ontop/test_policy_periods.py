"""
Testar diferentes endpoints de policy periods
"""
import requests
import json

API_KEY = 'eyJraWQiOiJmYWN0b3JpYWwtaWQiLCJhbGciOiJFUzI1NiJ9.eyJpYXQiOjE3NzE4ODQ4NjQsImV4cCI6MjA4NzQ1NDM4NCwianRpIjoiNzBjZWRiMzktODNiZC00MDEwLWJhYjgtMmZiMjRjNjBkNDBhIiwiY2VsbCI6ImF6dXJlLWRlbW8tZ3djLWV1MiIsImNvbXBhbnlfaWQiOjU1NDcxfQ.vwbec8pZc1ybTnGchYRaZMacnlndqXFh8WxjlJ_gFNfQ5BIYhUQjFdPhU_-ZwyvffqYyAgI5ZdaBomfKQx3cCg'
BASE_URL = 'https://api.eu2.demo.factorial.dev'
API_VERSION = '2026-07-01'

HEADERS = {
    'x-api-key': API_KEY,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

endpoints = [
    f'{BASE_URL}/api/{API_VERSION}/resources/payroll/policy_periods',
    f'{BASE_URL}/api/{API_VERSION}/resources/payroll/policy-periods',
    f'{BASE_URL}/api/{API_VERSION}/payroll/policy_periods',
    f'{BASE_URL}/api/{API_VERSION}/payroll/policy-periods',
    f'{BASE_URL}/api/{API_VERSION}/resources/policy_periods',
]

print("Testando endpoints de policy periods...")
print()

for endpoint in endpoints:
    try:
        r = requests.get(endpoint, headers=HEADERS, params={'limit': 5}, timeout=10)
        print(f"{endpoint}")
        print(f"  Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            periods = data.get('data', [])
            print(f"  [OK] Encontrados {len(periods)} policy periods")
            if periods:
                print(f"  Primeiro: {periods[0].get('id')} - {periods[0].get('name', 'N/A')}")
        else:
            print(f"  Resposta: {r.text[:100]}")
        print()
    except Exception as e:
        print(f"  ERRO: {e}")
        print()
