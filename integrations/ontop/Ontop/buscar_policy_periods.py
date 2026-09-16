"""
Buscar policy periods em diferentes endpoints
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

# Testar diferentes endpoints relacionados a payroll
endpoints = [
    f'{BASE_URL}/api/{API_VERSION}/resources/payroll',
    f'{BASE_URL}/api/{API_VERSION}/resources/payroll/policies',
    f'{BASE_URL}/api/{API_VERSION}/resources/payroll/periods',
    f'{BASE_URL}/api/{API_VERSION}/resources/payroll/payrolls',
    f'{BASE_URL}/api/{API_VERSION}/resources/payroll/supplements',  # Ver se tem policy_period_id nos existentes
]

print("Buscando policy periods em diferentes endpoints...")
print()

for endpoint in endpoints:
    try:
        r = requests.get(endpoint, headers=HEADERS, params={'limit': 5}, timeout=10)
        print(f"{endpoint}")
        print(f"  Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            items = data.get('data', [])
            print(f"  [OK] Encontrados {len(items)} itens")
            if items and len(items) > 0:
                print(f"  Primeiro item: {json.dumps(items[0], indent=2)[:200]}")
        else:
            print(f"  Resposta: {r.text[:150]}")
        print()
    except Exception as e:
        print(f"  ERRO: {e}")
        print()

# Tentar buscar supplements existentes para ver se tem policy_period_id
print("Buscando supplements existentes para ver estrutura...")
try:
    r = requests.get(f'{BASE_URL}/api/{API_VERSION}/resources/payroll/supplements', 
                     headers=HEADERS, params={'limit': 1}, timeout=10)
    if r.status_code == 200:
        data = r.json()
        supplements = data.get('data', [])
        if supplements:
            print(f"  [OK] Encontrado supplement exemplo:")
            print(json.dumps(supplements[0], indent=2))
    else:
        print(f"  Status: {r.status_code}")
        print(f"  Resposta: {r.text[:200]}")
except Exception as e:
    print(f"  ERRO: {e}")
