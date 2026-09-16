#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testa diferentes formatos de endpoint para encontrar o correto
"""

import requests
import json

API_KEY = "eyJraWQiOiJmYWN0b3JpYWwtaWQiLCJhbGciOiJFUzI1NiJ9.eyJpYXQiOjE3NzAwNjQ2OTIsImV4cCI6MjA4NTYzNDIxMiwianRpIjoiYmJhNzVlYmItNTBmMi00YjUyLWJkZTEtOGVmZjg0NjM1OTYxIiwiY2VsbCI6ImF6dXJlLWRlbW8tZ3djLWV1MiIsImNvbXBhbnlfaWQiOjU1MjI5fQ.Wk9AbqhfFlmqHXYpDNKnqBV0mAVOlzsiJp-MRxeR2fF4PN6ZBV0ap5zTyObyAQElNhOyEi5tXWT00vfxIcYv2g"
BASE_URL = "https://api.eu2.demo.factorial.dev"

headers = {
    'x-api-key': API_KEY,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# Testar diferentes formatos de endpoint
endpoints = [
    # Formato usado pelo coletor
    'api/2026-07-01/resources/companies/companies',
    'api/2026-07-01/resources/employees/employees',
    
    # Outros formatos
    'api/2026-07-01/resources/companies/companies',
    'api/2026-07-01/resources/employees/employees',
    
    # Sem resources
    'api/2026-07-01/companies/companies',
    'api/2026-07-01/employees/employees',
    
    # Formato direto
    'companies/companies',
    'employees/employees',
]

print("=" * 80)
print("TESTANDO DIFERENTES FORMATOS DE ENDPOINT")
print("=" * 80)

for endpoint in endpoints:
    url = f"{BASE_URL}/{endpoint}"
    print(f"\nTestando: {endpoint}")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  [OK] SUCESSO!")
            if 'data' in data:
                print(f"  Itens retornados: {len(data.get('data', []))}")
                if len(data.get('data', [])) > 0:
                    first = data['data'][0]
                    if 'company_id' in first:
                        print(f"  Company ID: {first.get('company_id')}")
                    if 'name' in first:
                        print(f"  Nome: {first.get('name')}")
            print(f"  Resposta: {json.dumps(data)[:200]}...")
            break
        elif response.status_code == 401:
            print(f"  [ERRO] 401 Unauthorized")
        elif response.status_code == 404:
            print(f"  [AVISO] 404 Not Found")
        else:
            print(f"  [ERRO] {response.status_code}: {response.text[:100]}")
    except Exception as e:
        print(f"  [EXCECAO] {e}")

print("\n" + "=" * 80)
