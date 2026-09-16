#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para descobrir todos os recursos disponíveis na API
"""

import requests
import json

BASE_URL = "https://api.eu2.demo.factorial.dev"
API_KEY = "eyJraWQiOiJmYWN0b3JpYWwtaWQiLCJhbGciOiJFUzI1NiJ9.eyJpYXQiOjE3NjM2NzU2ODgsImV4cCI6MjA3OTI0NTIwOCwianRpIjoiOGJhY2U3ZjItYTczZC00NDA2LWI0YjYtNDYzNTVlMDBmZjBkIiwiY2VsbCI6ImF6dXJlLWRlbW8tZ3djLWV1MiIsImNvbXBhbnlfaWQiOjI4NjkyfQ.gPtpP0-BWj2e3SiBN6dLqSL8Lz1M2LEFVTLg4kcuXUk06bAyH8YgBf5ejwSFG5TSByreYX3SCJVb_VQ9rLzGTQ"

headers = {
    'x-api-key': API_KEY,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

print("=" * 80)
print("🔍 DESCOBRINDO RECURSOS DISPONÍVEIS NA API")
print("=" * 80)

# Primeiro, verificar o endpoint de credentials para ver informações
print("\n📋 Verificando informações de credenciais...")
url = f"{BASE_URL}/api/2026-07-01/resources/api_public/credentials"
response = requests.get(url, headers=headers, timeout=10)

if response.status_code == 200:
    data = response.json()
    print(f"✅ Credenciais obtidas com sucesso!")
    print(f"   Company ID: {data.get('data', [{}])[0].get('company_id') if data.get('data') else 'N/A'}")
    print(f"   Legal Name: {data.get('data', [{}])[0].get('legal_name') if data.get('data') else 'N/A'}")
    print(f"\n   Resposta completa:")
    print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])

# Lista extensa de recursos possíveis da Factorial
recursos_possiveis = [
    # Recursos principais
    'employees',
    'companies',
    'locations',
    'departments',
    'teams',
    'shifts',
    'attendance',
    'time_off',
    'expenses',
    'documents',
    'contracts',
    'recruitment',
    'performance',
    'trainings',
    'finance',
    'banking',
    'payroll',
    'custom_fields',
    'holidays',
    
    # Tarefas e projetos (muitas variações)
    'tasks',
    'task',
    'todos',
    'todo',
    'projects',
    'project',
    'project_management',
    'project_management/tasks',
    'project_management/projects',
    'posts',
    'post',
    'items',
    'item',
    
    # Outros
    'notifications',
    'messages',
    'comments',
    'files',
    'uploads',
]

print("\n" + "=" * 80)
print("🔎 TESTANDO RECURSOS INDIVIDUAIS")
print("=" * 80)

recursos_funcionais = []

for recurso in recursos_possiveis:
    url = f"{BASE_URL}/api/2026-07-01/{recurso}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        status = response.status_code
        
        if status == 200:
            print(f"\n✅ {recurso} - FUNCIONAL!")
            try:
                data = response.json()
                if isinstance(data, dict):
                    if 'data' in data:
                        print(f"   Tipo: {type(data['data'])}")
                        if isinstance(data['data'], list):
                            print(f"   Total de itens: {len(data['data'])}")
                            if len(data['data']) > 0:
                                print(f"   Estrutura do primeiro item: {list(data['data'][0].keys())[:10]}")
                        else:
                            print(f"   Dados: {list(data.keys())}")
                    else:
                        print(f"   Chaves: {list(data.keys())[:10]}")
                elif isinstance(data, list):
                    print(f"   Lista com {len(data)} itens")
                    if len(data) > 0 and isinstance(data[0], dict):
                        print(f"   Estrutura: {list(data[0].keys())[:10]}")
            except:
                print(f"   Resposta: {response.text[:200]}")
            recursos_funcionais.append(recurso)
        elif status == 401:
            print(f"🔐 {recurso} - Não autenticado")
        elif status == 403:
            print(f"🚫 {recurso} - Sem permissão")
        elif status == 404:
            pass  # Não mostrar 404s
        elif status == 405:
            print(f"⚠️  {recurso} - Método não permitido (405) - pode aceitar POST")
        elif status in [400, 422]:
            print(f"⚠️  {recurso} - Status {status} - pode precisar de parâmetros")
            
    except Exception as e:
        pass

# Testar POST nos recursos funcionais que podem aceitar criação
print("\n" + "=" * 80)
print("📝 TESTANDO CRIAÇÃO (POST) NOS RECURSOS FUNCIONAIS")
print("=" * 80)

# Recursos que podem aceitar POST
recursos_para_post = [
    'tasks',
    'posts',
    'todos',
    'projects',
    'project_management/tasks',
]

for recurso in recursos_para_post:
    url = f"{BASE_URL}/api/2026-07-01/{recurso}"
    
    # Dados de teste
    test_data = {
        'title': 'Tarefa de Teste',
        'description': 'Criada via API'
    }
    
    try:
        response = requests.post(url, headers=headers, json=test_data, timeout=10)
        status = response.status_code
        
        if status in [200, 201]:
            print(f"\n✅ POST {recurso} - SUCESSO!")
            print(f"   Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        elif status == 400:
            print(f"\n⚠️  POST {recurso} - Bad Request (400)")
            print(f"   Resposta: {response.text[:300]}")
        elif status == 404:
            print(f"\n❌ POST {recurso} - Não encontrado (404)")
        elif status == 405:
            print(f"\n⚠️  POST {recurso} - Método não permitido (405)")
        elif status == 422:
            print(f"\n⚠️  POST {recurso} - Erro de validação (422)")
            print(f"   Resposta: {response.text[:300]}")
            
    except Exception as e:
        print(f"\n❌ POST {recurso} - Erro: {e}")

# Resumo
print("\n" + "=" * 80)
print("📊 RESUMO")
print("=" * 80)

if recursos_funcionais:
    print(f"\n✅ Recursos GET funcionais encontrados ({len(recursos_funcionais)}):")
    for recurso in recursos_funcionais:
        print(f"   - {recurso}")
else:
    print("\n❌ Nenhum recurso GET funcional encontrado")

print("=" * 80)


