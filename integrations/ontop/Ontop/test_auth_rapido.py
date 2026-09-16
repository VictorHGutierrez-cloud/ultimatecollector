"""
Teste rápido de autenticação com a nova API key
"""
import requests
import json

API_KEY = 'eyJraWQiOiJmYWN0b3JpYWwtaWQiLCJhbGciOiJFUzI1NiJ9.eyJpYXQiOjE3NzE4ODQ4NjQsImV4cCI6MjA4NzQ1NDM4NCwianRpIjoiNzBjZWRiMzktODNiZC00MDEwLWJhYjgtMmZiMjRjNjBkNDBhIiwiY2VsbCI6ImF6dXJlLWRlbW8tZ3djLWV1MiIsImNvbXBhbnlfaWQiOjU1NDcxfQ.vwbec8pZc1ybTnGchYRaZMacnlndqXFh8WxjlJ_gFNfQ5BIYhUQjFdPhU_-ZwyvffqYyAgI5ZdaBomfKQx3cCg'
BASE_URL = 'https://api.eu2.demo.factorial.dev'
API_VERSION = '2026-07-01'

# Endpoint para testar
endpoint = f'{BASE_URL}/api/{API_VERSION}/resources/employees/employees'

print("=" * 60)
print("TESTE RAPIDO DE AUTENTICACAO")
print("=" * 60)
print()

# Teste 1: Bearer
print("1. Testando com Bearer...")
headers_bearer = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
try:
    r = requests.get(endpoint, headers=headers_bearer, params={'limit': 1}, timeout=10)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        total = data.get('meta', {}).get('total', 0)
        print(f"   SUCESSO! Total funcionarios: {total}")
        print("   METODO CORRETO: Bearer")
    else:
        print(f"   Resposta: {r.text[:200]}")
except Exception as e:
    print(f"   ERRO: {e}")

print()

# Teste 2: x-api-key
print("2. Testando com x-api-key...")
headers_xkey = {
    'x-api-key': API_KEY,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
try:
    r = requests.get(endpoint, headers=headers_xkey, params={'limit': 1}, timeout=10)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        total = data.get('meta', {}).get('total', 0)
        print(f"   SUCESSO! Total funcionarios: {total}")
        print("   METODO CORRETO: x-api-key")
    else:
        print(f"   Resposta: {r.text[:200]}")
except Exception as e:
    print(f"   ERRO: {e}")

print()

# Teste 3: X-API-Key (maiúsculo)
print("3. Testando com X-API-Key (maiusculo)...")
headers_xkey_upper = {
    'X-API-Key': API_KEY,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
try:
    r = requests.get(endpoint, headers=headers_xkey_upper, params={'limit': 1}, timeout=10)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        total = data.get('meta', {}).get('total', 0)
        print(f"   SUCESSO! Total funcionarios: {total}")
        print("   METODO CORRETO: X-API-Key")
    else:
        print(f"   Resposta: {r.text[:200]}")
except Exception as e:
    print(f"   ERRO: {e}")

print()
print("=" * 60)
