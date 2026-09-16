#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testa a API diretamente com o token correto
"""

import requests
import json
import base64

# Token do novo ambiente (Company ID 55229)
API_KEY = "eyJraWQiOiJmYWN0b3JpYWwtaWQiLCJhbGciOiJFUzI1NiJ9.eyJpYXQiOjE3NzAwMzc4MDgsImV4cCI6MjA4NTYwNzMyOCwianRpIjoiZWQwZDllYzEtOWRmYS00NmM2LWFlN2ItNGVlMDM1NDllOTNjIiwiY2VsbCI6ImF6dXJlLWRlbW8tZ3djLWV1MiIsImNvbXBhbnlfaWQiOjU1MjI5fQ.UUva0-lOWTjksMJrNUwpH0pJ9jn2ZBUvCWgtYNaYjefKK2wvVu1RzhlQH4H03dvfFPhAQZW7ACsW0LyMH2sMTw"
BASE_URL = "https://api.eu2.demo.factorial.dev"

# Decodificar token para verificar
parts = API_KEY.split('.')
payload = parts[1]
payload += '=' * (4 - len(payload) % 4)
decoded = base64.urlsafe_b64decode(payload)
data = json.loads(decoded)
print(f"Token Company ID: {data.get('company_id')}")
print(f"Token Cell: {data.get('cell')}")
print()

# Testar diferentes formatos de endpoint e autenticação
endpoints_to_test = [
    'companies/companies',
    'api/2026-07-01/companies/companies',
    'api/2026-07-01/companies/companies',
    'employees/employees',
    'api/2026-07-01/employees/employees',
]

auth_methods = [
    ('Bearer', {'Authorization': f'Bearer {API_KEY}'}),
    ('x-api-key', {'x-api-key': API_KEY}),
]

print("=" * 80)
print("TESTANDO API DIRETAMENTE")
print("=" * 80)

for auth_name, headers in auth_methods:
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/json'
    
    print(f"\n{'='*80}")
    print(f"Metodo de autenticacao: {auth_name}")
    print(f"{'='*80}")
    
    for endpoint in endpoints_to_test:
        url = f"{BASE_URL}/{endpoint}"
        print(f"\nTestando: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and len(data['data']) > 0:
                    first_item = data['data'][0]
                    if 'company_id' in first_item:
                        print(f"  [OK] Sucesso! Company ID retornado: {first_item['company_id']}")
                        if 'name' in first_item:
                            print(f"  Nome da empresa: {first_item.get('name', 'N/A')}")
                    elif 'id' in first_item:
                        print(f"  [OK] Sucesso! Retornou {len(data['data'])} itens")
                else:
                    print(f"  [OK] Sucesso! Resposta: {json.dumps(data)[:100]}...")
                break  # Se funcionou, não precisa testar outros endpoints
            elif response.status_code == 401:
                print(f"  [ERRO] 401 Unauthorized")
            else:
                print(f"  [ERRO] {response.status_code}: {response.text[:100]}")
        except Exception as e:
            print(f"  [EXCECAO] {e}")

print("\n" + "=" * 80)
