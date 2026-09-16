"""
Tentar criar ou descobrir policy periods
"""
import requests
import json

API_KEY = "eyJraWQiOiJmYWN0b3JpYWwtaWQiLCJhbGciOiJFUzI1NiJ9.eyJpYXQiOjE3NzE4ODQ4NjQsImV4cCI6MjA4NzQ1NDM4NCwianRpIjoiNzBjZWRiMzktODNiZC00MDEwLWJhYjgtMmZiMjRjNjBkNDBhIiwiY2VsbCI6ImF6dXJlLWRlbW8tZ3djLWV1MiIsImNvbXBhbnlfaWQiOjU1NDcxfQ.vwbec8pZc1ybTnGchYRaZMacnlndqXFh8WxjlJ_gFNfQ5BIYhUQjFdPhU_-ZwyvffqYyAgI5ZdaBomfKQx3cCg"
BASE_URL = "https://api.eu2.demo.factorial.dev"
API_VERSION = "2026-07-01"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-api-key": API_KEY
}

print("=" * 60)
print("TENTANDO CRIAR OU DESCOBRIR POLICY PERIODS")
print("=" * 60)
print()

# Tentar criar um policy period
print("1. Tentando criar policy period (POST)...")
try:
    url = f"{BASE_URL}/api/{API_VERSION}/resources/payroll/policy_periods"
    payload = {
        "name": "Test Period",
        "status": "preparation"
    }
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    print(f"   Status: {response.status_code}")
    print(f"   Resposta: {response.text[:300]}")
    if response.status_code == 201 or response.status_code == 200:
        data = response.json()
        period_id = data.get('id')
        print(f"   [OK] Policy period criado! ID: {period_id}")
except Exception as e:
    print(f"   ERRO: {e}")

print()

# Tentar usar o endpoint change_status com um ID comum (teste)
print("2. Tentando descobrir IDs existentes testando valores comuns...")
print("   (Isso pode demorar, testando IDs de 1 a 100)")
print()

found_ids = []
for test_id in range(1, 101):
    try:
        url = f"{BASE_URL}/api/{API_VERSION}/resources/payroll/policy_periods/{test_id}/change_status"
        payload = {
            "status": "preparation",
            "notify_employee": False
        }
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        
        # Se não for 404, pode ser um ID válido
        if response.status_code != 404:
            print(f"   ID {test_id}: Status {response.status_code}")
            if response.status_code == 200:
                found_ids.append(test_id)
                print(f"   [OK] ID {test_id} VALIDO!")
                data = response.json()
                print(f"   Dados: {json.dumps(data, indent=2)[:200]}")
    except:
        pass
    
    if test_id % 20 == 0:
        print(f"   Testado até ID {test_id}...")

print()
if found_ids:
    print(f"[OK] IDs encontrados: {found_ids}")
    print(f"   Use o ID {found_ids[0]} para criar supplements")
else:
    print("[AVISO] Nenhum ID valido encontrado nos primeiros 100")
    print("   Talvez seja necessario criar um policy period manualmente no frontend")
