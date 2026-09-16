#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testa API Key diretamente com header x-api-key
"""

import requests
import json
import base64

# API Key: teste - Company ID 55229
API_KEY = "eyJraWQiOiJmYWN0b3JpYWwtaWQiLCJhbGciOiJFUzI1NiJ9.eyJpYXQiOjE3NzAwNjQ2OTIsImV4cCI6MjA4NTYzNDIxMiwianRpIjoiYmJhNzVlYmItNTBmMi00YjUyLWJkZTEtOGVmZjg0NjM1OTYxIiwiY2VsbCI6ImF6dXJlLWRlbW8tZ3djLWV1MiIsImNvbXBhbnlfaWQiOjU1MjI5fQ.Wk9AbqhfFlmqHXYpDNKnqBV0mAVOlzsiJp-MRxeR2fF4PN6ZBV0ap5zTyObyAQElNhOyEi5tXWT00vfxIcYv2g"
BASE_URL = "https://api.eu2.demo.factorial.dev"

# Decodificar token para verificar
try:
    parts = API_KEY.split('.')
    payload = parts[1]
    payload += '=' * (4 - len(payload) % 4)
    decoded = base64.urlsafe_b64decode(payload)
    data = json.loads(decoded)
    print(f"Token Company ID: {data.get('company_id')}")
    print(f"Token Cell: {data.get('cell')}")
    print()
except:
    pass

print("=" * 80)
print("TESTANDO API KEY COM HEADER x-api-key")
print("=" * 80)

# Headers com x-api-key (sem prefixos, apenas o valor)
headers = {
    'x-api-key': API_KEY,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# Testar diferentes endpoints
endpoints_to_test = [
    'companies/companies',
    'employees/employees',
    'api/2026-07-01/companies/companies',
    'api/2026-07-01/employees/employees',
]

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
                    print(f"  [OK] Sucesso! Company ID: {first_item['company_id']}")
                    if 'name' in first_item:
                        print(f"  Nome: {first_item.get('name')}")
                    if 'legal_name' in first_item:
                        print(f"  Legal Name: {first_item.get('legal_name')}")
                elif 'id' in first_item:
                    print(f"  [OK] Sucesso! Retornou {len(data['data'])} itens")
                    if 'company_id' in first_item:
                        print(f"  Company ID: {first_item.get('company_id')}")
            else:
                print(f"  [OK] Sucesso! Resposta: {json.dumps(data)[:100]}...")
            break  # Se funcionou, não precisa testar outros
        elif response.status_code == 401:
            print(f"  [ERRO] 401 Unauthorized")
            print(f"  Resposta: {response.text[:200]}")
        elif response.status_code == 404:
            print(f"  [AVISO] 404 Not Found - endpoint pode não existir")
        else:
            print(f"  [ERRO] {response.status_code}: {response.text[:200]}")
    except Exception as e:
        print(f"  [EXCECAO] {e}")

print("\n" + "=" * 80)
