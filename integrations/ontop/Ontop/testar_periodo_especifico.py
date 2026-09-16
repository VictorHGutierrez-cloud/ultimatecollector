"""
Testar um policy_period_id específico para ver se está aberto
"""
import requests
import json
import sys
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
effective_on = datetime.now().strftime('%Y-%m-%d')

# Pegar ID do argumento ou pedir
if len(sys.argv) > 1:
    period_id = int(sys.argv[1])
else:
    period_id = int(input("Digite o Policy Period ID para testar: "))

print("=" * 60)
print(f"TESTANDO POLICY PERIOD ID {period_id}")
print("=" * 60)
print()

url = f"{BASE_URL}/api/{API_VERSION}/resources/payroll/supplements"
payload = {
    'employee_id': employee_id,
    'amount_in_cents': 1000,
    'effective_on': effective_on,
    'contracts_taxonomy_id': taxonomy_id,
    'payroll_policy_period_id': period_id,
    'unit': 'money',
    'description': 'Teste de periodo aberto'
}

print(f"Payload:")
print(json.dumps(payload, indent=2))
print()

try:
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.text}")
    print()
    
    if response.status_code == 201 or response.status_code == 200:
        data = response.json()
        supplement_id = data.get('id')
        print(f"[OK] PERIODO ABERTO! Supplement criado com ID: {supplement_id}")
        print()
        print("Agora voce pode executar:")
        print(f"  python test_factorial_data_insert.py {period_id}")
        print()
        print("Ou adicionar ao config_unificado.env:")
        print(f"  POLICY_PERIOD_ID={period_id}")
        
        # Deletar supplement de teste
        try:
            delete_url = f"{BASE_URL}/api/{API_VERSION}/resources/payroll/supplements/{supplement_id}"
            delete_response = requests.delete(delete_url, headers=headers, timeout=5)
            if delete_response.status_code == 200 or delete_response.status_code == 204:
                print()
                print("(Supplement de teste deletado)")
        except:
            pass
    else:
        print("[ERRO] Periodo nao esta aberto ou ha outro problema")
        print("Verifique:")
        print("1. O periodo esta aberto no frontend?")
        print("2. O ID esta correto?")
        print("3. O employee_id e taxonomy_id sao validos?")
        
except Exception as e:
    print(f"[ERRO] {e}")
