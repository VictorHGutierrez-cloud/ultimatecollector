"""
Descobrir policy_period_ids através do endpoint GET de supplements
"""
import requests
import json

API_KEY = "eyJraWQiOiJmYWN0b3JpYWwtaWQiLCJhbGciOiJFUzI1NiJ9.eyJpYXQiOjE3NzE4ODQ4NjQsImV4cCI6MjA4NzQ1NDM4NCwianRpIjoiNzBjZWRiMzktODNiZC00MDEwLWJhYjgtMmZiMjRjNjBkNDBhIiwiY2VsbCI6ImF6dXJlLWRlbW8tZ3djLWV1MiIsImNvbXBhbnlfaWQiOjU1NDcxfQ.vwbec8pZc1ybTnGchYRaZMacnlndqXFh8WxjlJ_gFNfQ5BIYhUQjFdPhU_-ZwyvffqYyAgI5ZdaBomfKQx3cCg"
BASE_URL = "https://api.eu2.demo.factorial.dev"
API_VERSION = "2026-07-01"

headers = {
    "accept": "application/json",
    "x-api-key": API_KEY
}

print("=" * 60)
print("DESCOBRINDO POLICY_PERIOD_IDS ATRAVES DE SUPPLEMENTS")
print("=" * 60)
print()

# 1. Buscar todos os supplements (sem filtro)
print("1. Buscando todos os supplements existentes...")
try:
    url = f"{BASE_URL}/api/{API_VERSION}/resources/payroll/supplements"
    response = requests.get(url, headers=headers, params={'limit': 100}, timeout=10)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        supplements = data.get('data', [])
        print(f"   [OK] Encontrados {len(supplements)} supplements")
        
        if supplements:
            # Extrair policy_period_ids únicos
            policy_period_ids = set()
            for supp in supplements:
                period_id = supp.get('payroll_policy_period_id')
                if period_id:
                    policy_period_ids.add(period_id)
            
            if policy_period_ids:
                print(f"   [OK] Policy Period IDs encontrados: {sorted(policy_period_ids)}")
                print(f"   Use o ID {sorted(policy_period_ids)[0]} para criar novos supplements")
            else:
                print("   [AVISO] Nenhum policy_period_id encontrado nos supplements")
        else:
            print("   [AVISO] Nenhum supplement encontrado")
    else:
        print(f"   Resposta: {response.text[:200]}")
except Exception as e:
    print(f"   ERRO: {e}")

print()

# 2. Tentar descobrir policy_period_ids testando valores comuns
print("2. Testando policy_period_ids comuns (1-50)...")
print("   (Buscando supplements com cada ID para ver qual existe)")
print()

found_ids = []
for test_id in range(1, 51):
    try:
        url = f"{BASE_URL}/api/{API_VERSION}/resources/payroll/supplements"
        params = {
            'policy_period_ids[]': [test_id],
            'limit': 1
        }
        response = requests.get(url, headers=headers, params=params, timeout=5)
        
        # Se retornar 200 (mesmo que vazio), o policy_period_id existe
        if response.status_code == 200:
            data = response.json()
            # Verificar se a resposta não tem erro sobre policy_period_id inválido
            if 'errors' not in data or 'policy_period' not in str(data.get('errors', {})).lower():
                found_ids.append(test_id)
                print(f"   [OK] Policy Period ID {test_id} EXISTE!")
                
                # Se houver supplements, mostrar
                supplements = data.get('data', [])
                if supplements:
                    print(f"      Encontrados {len(supplements)} supplements para este periodo")
    except:
        pass
    
    if test_id % 10 == 0:
        print(f"   Testado até ID {test_id}...")

print()
if found_ids:
    print(f"[OK] Policy Period IDs encontrados: {found_ids}")
    print(f"   Use o ID {found_ids[0]} para criar novos supplements")
else:
    print("[AVISO] Nenhum policy_period_id valido encontrado")
    print("   Pode ser necessario criar um policy period manualmente no frontend")
