#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar todos os endpoints disponíveis na API Factorial
e descobrir onde criar tarefas
"""

import requests
import json

BASE_URL = "https://api.eu2.demo.factorial.dev"
API_KEY = "eyJraWQiOiJmYWN0b3JpYWwtaWQiLCJhbGciOiJFUzI1NiJ9.eyJpYXQiOjE3NjM2NzU2ODgsImV4cCI6MjA3OTI0NTIwOCwianRpIjoiOGJhY2U3ZjItYTczZC00NDA2LWI0YjYtNDYzNTVlMDBmZjBkIiwiY2VsbCI6ImF6dXJlLWRlbW8tZ3djLWV1MiIsImNvbXBhbnlfaWQiOjI4NjkyfQ.gPtpP0-BWj2e3SiBN6dLqSL8Lz1M2LEFVTLg4kcuXUk06bAyH8YgBf5ejwSFG5TSByreYX3SCJVb_VQ9rLzGTQ"

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# Lista extensa de endpoints para testar
endpoints_to_test = [
    # Endpoints base
    '',
    'api',
    'api/2026-07-01',
    'api/v1',
    
    # Recursos principais
    'api/2026-07-01/employees',
    'api/2026-07-01/companies',
    'api/2026-07-01/locations',
    'api/2026-07-01/departments',
    'api/2026-07-01/teams',
    
    # Tarefas e projetos (várias variações)
    'api/2026-07-01/tasks',
    'api/2026-07-01/task',
    'api/2026-07-01/projects',
    'api/2026-07-01/project',
    'api/2026-07-01/project_management/tasks',
    'api/2026-07-01/project_management/projects',
    'api/2026-07-01/project_management',
    'api/2026-07-01/posts',  # Posts podem incluir tarefas
    'api/2026-07-01/todos',
    'api/2026-07-01/items',
    
    # Outros recursos
    'api/2026-07-01/time_off',
    'api/2026-07-01/attendance',
    'api/2026-07-01/expenses',
    'api/2026-07-01/documents',
    'api/2026-07-01/contracts',
    'api/2026-07-01/recruitment',
    'api/2026-07-01/performance',
    'api/2026-07-01/trainings',
    'api/2026-07-01/finance',
    
    # Recursos da API
    'api/2026-07-01/resources',
    'api/2026-07-01/resources/api_public',
    'api/2026-07-01/resources/api_public/credentials',
]

print("=" * 80)
print("🔍 TESTANDO TODOS OS ENDPOINTS DISPONÍVEIS NA API FACTORIAL")
print("=" * 80)

working_endpoints = []
post_endpoints = []

for endpoint in endpoints_to_test:
    url = f"{BASE_URL}/{endpoint}" if endpoint else BASE_URL
    
    try:
        # Testar GET
        response = requests.get(url, headers=headers, timeout=10)
        
        status = response.status_code
        
        if status == 200:
            print(f"\n✅ GET {endpoint or '(raiz)'}")
            print(f"   URL: {url}")
            try:
                data = response.json()
                # Mostrar estrutura se for um objeto/dicionário
                if isinstance(data, dict):
                    keys = list(data.keys())[:10]  # Primeiras 10 chaves
                    print(f"   Chaves: {keys}")
                    if 'data' in data:
                        print(f"   Tipo de dados: {type(data['data'])}")
                        if isinstance(data['data'], list) and len(data['data']) > 0:
                            print(f"   Primeiro item: {list(data['data'][0].keys())[:5]}")
                elif isinstance(data, list):
                    print(f"   Lista com {len(data)} itens")
                    if len(data) > 0:
                        print(f"   Primeiro item: {list(data[0].keys())[:5] if isinstance(data[0], dict) else data[0]}")
                else:
                    print(f"   Resposta: {str(data)[:200]}")
            except:
                print(f"   Resposta: {response.text[:200]}")
            working_endpoints.append(('GET', endpoint))
            
        elif status == 401:
            print(f"🔐 {endpoint or '(raiz)'} - Requer autenticação")
        elif status == 403:
            print(f"🚫 {endpoint or '(raiz)'} - Sem permissão")
        elif status == 404:
            pass  # Não mostrar 404s
        elif status in [400, 405, 422]:
            print(f"⚠️  {endpoint or '(raiz)'} - Status {status}")
            print(f"   Resposta: {response.text[:150]}")
            
    except Exception as e:
        pass

# Agora testar POST em endpoints promissores
print("\n" + "=" * 80)
print("📝 TESTANDO CRIAÇÃO (POST) EM ENDPOINTS PROMISSORES")
print("=" * 80)

post_candidates = [
    'api/2026-07-01/tasks',
    'api/2026-07-01/projects',
    'api/2026-07-01/project_management/tasks',
    'api/2026-07-01/posts',
    'api/2026-07-01/todos',
]

for endpoint in post_candidates:
    url = f"{BASE_URL}/{endpoint}"
    
    # Dados de teste simples
    test_data = {
        'title': 'Tarefa de Teste',
        'description': 'Criada via API'
    }
    
    try:
        response = requests.post(url, headers=headers, json=test_data, timeout=10)
        status = response.status_code
        
        if status in [200, 201]:
            print(f"\n✅ POST {endpoint} - SUCESSO!")
            print(f"   Status: {status}")
            try:
                data = response.json()
                print(f"   Resposta: {json.dumps(data, indent=2, ensure_ascii=False)}")
            except:
                print(f"   Resposta: {response.text}")
            post_endpoints.append(endpoint)
        elif status == 400:
            print(f"\n⚠️  POST {endpoint} - Bad Request (400)")
            print(f"   Resposta: {response.text[:300]}")
        elif status == 401:
            print(f"\n🔐 POST {endpoint} - Requer autenticação")
        elif status == 403:
            print(f"\n🚫 POST {endpoint} - Sem permissão")
        elif status == 422:
            print(f"\n⚠️  POST {endpoint} - Erro de validação (422)")
            print(f"   Resposta: {response.text[:300]}")
            
    except Exception as e:
        print(f"\n❌ POST {endpoint} - Erro: {e}")

# Resumo final
print("\n" + "=" * 80)
print("📊 RESUMO")
print("=" * 80)

if working_endpoints:
    print(f"\n✅ Endpoints GET funcionais encontrados: {len(working_endpoints)}")
    for method, endpoint in working_endpoints[:10]:  # Mostrar primeiros 10
        print(f"   - {endpoint or '(raiz)'}")
    if len(working_endpoints) > 10:
        print(f"   ... e mais {len(working_endpoints) - 10}")
else:
    print("\n❌ Nenhum endpoint GET funcional encontrado")

if post_endpoints:
    print(f"\n✅ Endpoints POST funcionais para criar tarefas:")
    for endpoint in post_endpoints:
        print(f"   - {endpoint}")
else:
    print("\n❌ Nenhum endpoint POST funcional encontrado para criar tarefas")
    print("\n💡 Próximos passos:")
    print("   1. Verificar documentação da API Factorial")
    print("   2. Verificar se o recurso de tarefas está habilitado")
    print("   3. Verificar permissões da chave API")

print("=" * 80)


