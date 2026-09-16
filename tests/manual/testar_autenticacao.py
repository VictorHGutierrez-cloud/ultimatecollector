#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar diferentes métodos de autenticação
"""

import requests
import json

BASE_URL = "https://api.eu2.demo.factorial.dev"
API_KEY = "eyJraWQiOiJmYWN0b3JpYWwtaWQiLCJhbGciOiJFUzI1NiJ9.eyJpYXQiOjE3NjM2NzU2ODgsImV4cCI6MjA3OTI0NTIwOCwianRpIjoiOGJhY2U3ZjItYTczZC00NDA2LWI0YjYtNDYzNTVlMDBmZjBkIiwiY2VsbCI6ImF6dXJlLWRlbW8tZ3djLWV1MiIsImNvbXBhbnlfaWQiOjI4NjkyfQ.gPtpP0-BWj2e3SiBN6dLqSL8Lz1M2LEFVTLg4kcuXUk06bAyH8YgBf5ejwSFG5TSByreYX3SCJVb_VQ9rLzGTQ"

# Testar diferentes métodos de autenticação
auth_methods = [
    {
        'name': 'Bearer Token',
        'headers': {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    },
    {
        'name': 'x-api-key Header',
        'headers': {
            'x-api-key': API_KEY,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    },
    {
        'name': 'Authorization Header (sem Bearer)',
        'headers': {
            'Authorization': API_KEY,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    },
    {
        'name': 'X-API-Key Header',
        'headers': {
            'X-API-Key': API_KEY,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    },
]

# Endpoints para testar
test_endpoints = [
    'api/2026-07-01/employees',
    'api/2026-07-01/companies',
    'api/2026-07-01/resources/api_public/credentials',
    'api/2026-07-01',
]

print("=" * 80)
print("🔐 TESTANDO DIFERENTES MÉTODOS DE AUTENTICAÇÃO")
print("=" * 80)

working_auth = None

for auth in auth_methods:
    print(f"\n{'='*80}")
    print(f"🔑 Testando: {auth['name']}")
    print(f"{'='*80}")
    
    for endpoint in test_endpoints:
        url = f"{BASE_URL}/{endpoint}"
        
        try:
            response = requests.get(url, headers=auth['headers'], timeout=10)
            status = response.status_code
            
            if status == 200:
                print(f"\n✅ SUCESSO com {auth['name']} em {endpoint}!")
                print(f"   URL: {url}")
                try:
                    data = response.json()
                    if isinstance(data, dict):
                        print(f"   Chaves: {list(data.keys())[:10]}")
                    elif isinstance(data, list):
                        print(f"   Lista com {len(data)} itens")
                    print(f"   Resposta (primeiros 300 chars): {str(data)[:300]}")
                except:
                    print(f"   Resposta: {response.text[:300]}")
                
                if not working_auth:
                    working_auth = auth
                    
            elif status == 401:
                print(f"🔐 {endpoint} - Não autenticado (401)")
            elif status == 403:
                print(f"🚫 {endpoint} - Sem permissão (403)")
            elif status == 404:
                print(f"❓ {endpoint} - Não encontrado (404)")
            else:
                print(f"⚠️  {endpoint} - Status {status}")
                print(f"   Resposta: {response.text[:150]}")
                
        except Exception as e:
            print(f"❌ {endpoint} - Erro: {e}")

# Se encontrou um método que funciona, testar criação de tarefas
if working_auth:
    print("\n" + "=" * 80)
    print("📝 TESTANDO CRIAÇÃO DE TAREFAS COM AUTENTICAÇÃO FUNCIONAL")
    print("=" * 80)
    
    task_endpoints = [
        'api/2026-07-01/tasks',
        'api/2026-07-01/projects',
        'api/2026-07-01/posts',
    ]
    
    for endpoint in task_endpoints:
        url = f"{BASE_URL}/{endpoint}"
        test_data = {
            'title': 'Tarefa de Teste',
            'description': 'Criada via API para teste'
        }
        
        try:
            print(f"\n🔄 Tentando POST em {endpoint}...")
            response = requests.post(
                url, 
                headers=working_auth['headers'], 
                json=test_data, 
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                print(f"✅ Tarefa criada com sucesso em {endpoint}!")
                print(f"   Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
            else:
                print(f"⚠️  Status {response.status_code}")
                print(f"   Resposta: {response.text[:300]}")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
else:
    print("\n" + "=" * 80)
    print("❌ NENHUM MÉTODO DE AUTENTICAÇÃO FUNCIONOU")
    print("=" * 80)
    print("\n💡 Possíveis problemas:")
    print("   1. A chave API pode estar expirada")
    print("   2. A chave pode não ter as permissões necessárias")
    print("   3. O ambiente demo pode ter configurações diferentes")
    print("   4. Pode ser necessário usar OAuth2 em vez de API Key")

print("\n" + "=" * 80)


