"""
Buscar policy periods - tentar diferentes endpoints GET
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

# Tentar diferentes variações do endpoint GET
endpoints = [
    f"{BASE_URL}/api/{API_VERSION}/resources/payroll/policy_periods",
    f"{BASE_URL}/api/{API_VERSION}/resources/payroll/policy_periods/",
    f"{BASE_URL}/api/{API_VERSION}/payroll/policy_periods",
    f"{BASE_URL}/api/{API_VERSION}/payroll/policy_periods/",
]

print("=" * 60)
print("BUSCANDO POLICY PERIODS - DIFERENTES ENDPOINTS")
print("=" * 60)
print()

for endpoint in endpoints:
    print(f"Testando: {endpoint}")
    try:
        response = requests.get(endpoint, headers=headers, params={'limit': 10}, timeout=10)
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            periods = data.get('data', [])
            print(f"  [OK] Encontrados {len(periods)} policy periods!")
            print()
            
            if periods:
                print("  Policy Periods encontrados:")
                for i, period in enumerate(periods[:5], 1):
                    period_id = period.get('id')
                    name = period.get('name', 'N/A')
                    status = period.get('status', 'N/A')
                    print(f"    {i}. ID: {period_id}, Nome: {name}, Status: {status}")
                
                # Retornar o primeiro ID para usar
                first_id = periods[0].get('id')
                print()
                print(f"  [INFO] Use o ID {first_id} para criar supplements")
                break
            else:
                print("  Nenhum policy period encontrado na resposta")
        else:
            print(f"  Resposta: {response.text[:200]}")
        print()
    except Exception as e:
        print(f"  ERRO: {e}")
        print()

# Se não encontrou, tentar buscar através de payrolls ou outros recursos
print("=" * 60)
print("TENTANDO BUSCAR ATRAVES DE OUTROS RECURSOS")
print("=" * 60)
print()

# Tentar buscar payrolls que podem ter policy_period_id
try:
    url = f"{BASE_URL}/api/{API_VERSION}/resources/payroll/payrolls"
    response = requests.get(url, headers=headers, params={'limit': 5}, timeout=10)
    print(f"Testando: {url}")
    print(f"  Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        payrolls = data.get('data', [])
        print(f"  [OK] Encontrados {len(payrolls)} payrolls")
        if payrolls:
            print("  Verificando policy_period_id nos payrolls...")
            for payroll in payrolls[:3]:
                period_id = payroll.get('payroll_policy_period_id') or payroll.get('policy_period_id')
                if period_id:
                    print(f"    Policy Period ID encontrado: {period_id}")
except Exception as e:
    print(f"  ERRO: {e}")
