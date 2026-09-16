#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para descobrir o endpoint correto da API de tarefas da Factorial
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

# Lista de endpoints possíveis para testar
endpoints_to_test = [
    # Versões da API
    'api/2026-07-01/tasks',
    'api/2024-11-01/tasks',
    'api/v1/tasks',
    'api/v2/tasks',
    
    # Com prefixos diferentes
    'api/2026-07-01/project_management/tasks',
    'api/2026-07-01/projects/tasks',
    'api/v1/project_management/tasks',
    
    # Endpoints diretos
    'tasks',
    'project_management/tasks',
    'projects/tasks',
    
    # Outras variações
    'api/2026-07-01/task',
    'api/2026-07-01/todos',
    'api/2026-07-01/items',
]

print("=" * 70)
print("🔍 DESCOBRINDO ENDPOINT DE TAREFAS DA FACTORIAL")
print("=" * 70)

working_endpoints = []

for endpoint in endpoints_to_test:
    url = f"{BASE_URL}/{endpoint}"
    
    try:
        # Testar GET primeiro
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f"\n✅ GET funcionou: {url}")
            print(f"   Status: {response.status_code}")
            try:
                data = response.json()
                print(f"   Resposta: {json.dumps(data, indent=2)[:200]}...")
            except:
                print(f"   Resposta: {response.text[:200]}")
            working_endpoints.append(('GET', endpoint))
        elif response.status_code == 401:
            print(f"🔐 {url} - Requer autenticação (401)")
        elif response.status_code == 403:
            print(f"🚫 {url} - Sem permissão (403)")
        elif response.status_code == 404:
            pass  # Não mostrar 404s para não poluir
        else:
            print(f"⚠️  {url} - Status: {response.status_code}")
            
    except Exception as e:
        pass  # Ignorar erros de conexão

# Testar também POST em alguns endpoints comuns
print("\n" + "=" * 70)
print("📝 TESTANDO CRIAÇÃO DE TAREFAS (POST)")
print("=" * 70)

post_endpoints = [
    'api/2026-07-01/tasks',
    'api/2026-07-01/project_management/tasks',
    'api/v1/tasks',
]

for endpoint in post_endpoints:
    url = f"{BASE_URL}/{endpoint}"
    
    task_data = {
        'title': 'Teste de Tarefa',
        'description': 'Tarefa de teste criada via API'
    }
    
    try:
        response = requests.post(url, headers=headers, json=task_data, timeout=10)
        
        if response.status_code in [200, 201]:
            print(f"\n✅ POST funcionou: {url}")
            print(f"   Status: {response.status_code}")
            try:
                data = response.json()
                print(f"   Resposta: {json.dumps(data, indent=2)}")
            except:
                print(f"   Resposta: {response.text}")
            working_endpoints.append(('POST', endpoint))
        elif response.status_code == 400:
            print(f"⚠️  {url} - Bad Request (400)")
            print(f"   Resposta: {response.text[:200]}")
        elif response.status_code == 401:
            print(f"🔐 {url} - Requer autenticação (401)")
        elif response.status_code == 403:
            print(f"🚫 {url} - Sem permissão (403)")
            
    except Exception as e:
        print(f"❌ {url} - Erro: {e}")

# Verificar recursos disponíveis na API
print("\n" + "=" * 70)
print("📚 VERIFICANDO RECURSOS DISPONÍVEIS NA API")
print("=" * 70)

resources_to_check = [
    'api/2026-07-01',
    'api/2026-07-01/resources',
]

for resource in resources_to_check:
    url = f"{BASE_URL}/{resource}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f"\n✅ {url}")
            try:
                data = response.json()
                print(f"   Resposta: {json.dumps(data, indent=2)[:500]}...")
            except:
                print(f"   Resposta: {response.text[:500]}")
    except Exception as e:
        pass

print("\n" + "=" * 70)
if working_endpoints:
    print("✅ ENDPOINTS FUNCIONAIS ENCONTRADOS:")
    for method, endpoint in working_endpoints:
        print(f"   {method}: {endpoint}")
else:
    print("❌ Nenhum endpoint funcional encontrado")
    print("💡 Pode ser que:")
    print("   - O endpoint de tarefas tenha outro nome")
    print("   - A API de tarefas não esteja disponível neste ambiente")
    print("   - Seja necessário usar outro método de autenticação")
print("=" * 70)


