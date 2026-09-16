"""
Testar criação de supplement com payload mínimo
"""
import requests
import json
from datetime import datetime

API_KEY = "eyJraWQiOiJmYWN0b3JpYWwtaWQiLCJhbGciOiJFUzI1NiJ9.eyJpYXQiOjE3NzE4ODQ4NjQsImV4cCI6MjA4NzQ1NDM4NCwianRpIjoiNzBjZWRiMzktODNiZC00MDEwLWJhYjgtMmZiMjRjNjBkNDBhIiwiY2VsbCI6ImF6dXJlLWRlbW8tZ3djLWV1MiIsImNvbXBhbnlfaWQiOjU1NDcxfQ.vwbec8pZc1ybTnGchYRaZMacnlndqXFh8WxjlJ_gFNfQ5BIYhUQjFdPhU_-ZwyvffqYyAgI5ZdaBomfKQx3cCg"
BASE_URL = "https://api.eu2.demo.factorial.dev"
API_VERSION = "2026-07-01"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-api-key": API_KEY
}

# Dados de teste
employee_id = 1792913
taxonomy_id = 1519835
policy_period_id = 1
effective_on = datetime.now().strftime('%Y-%m-%d')

print("=" * 60)
print("TESTANDO CRIACAO DE SUPPLEMENT - PAYLOADS DIFERENTES")
print("=" * 60)
print()

# Teste 1: Payload mínimo
print("1. Testando payload mínimo...")
payload1 = {
    'employee_id': employee_id,
    'amount_in_cents': 10000,
    'effective_on': effective_on,
    'contracts_taxonomy_id': taxonomy_id,
    'payroll_policy_period_id': policy_period_id,
    'unit': 'money'
}
print(f"   Payload: {json.dumps(payload1, indent=2)}")
try:
    url = f"{BASE_URL}/api/{API_VERSION}/resources/payroll/supplements"
    response = requests.post(url, json=payload1, headers=headers, timeout=10)
    print(f"   Status: {response.status_code}")
    print(f"   Resposta: {response.text[:300]}")
    if response.status_code == 201 or response.status_code == 200:
        data = response.json()
        print(f"   [OK] Supplement criado! ID: {data.get('id')}")
except Exception as e:
    print(f"   ERRO: {e}")

print()

# Teste 2: Com description
print("2. Testando com description...")
payload2 = payload1.copy()
payload2['description'] = 'Test Supplement'
print(f"   Payload: {json.dumps(payload2, indent=2)}")
try:
    response = requests.post(url, json=payload2, headers=headers, timeout=10)
    print(f"   Status: {response.status_code}")
    print(f"   Resposta: {response.text[:300]}")
    if response.status_code == 201 or response.status_code == 200:
        data = response.json()
        print(f"   [OK] Supplement criado! ID: {data.get('id')}")
except Exception as e:
    print(f"   ERRO: {e}")

print()

# Teste 3: Data no passado (1 mês atrás)
print("3. Testando com data no passado...")
from datetime import timedelta
past_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
payload3 = payload1.copy()
payload3['effective_on'] = past_date
print(f"   Payload: {json.dumps(payload3, indent=2)}")
try:
    response = requests.post(url, json=payload3, headers=headers, timeout=10)
    print(f"   Status: {response.status_code}")
    print(f"   Resposta: {response.text[:300]}")
    if response.status_code == 201 or response.status_code == 200:
        data = response.json()
        print(f"   [OK] Supplement criado! ID: {data.get('id')}")
except Exception as e:
    print(f"   ERRO: {e}")
