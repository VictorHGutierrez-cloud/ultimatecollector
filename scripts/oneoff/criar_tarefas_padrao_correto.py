#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar tarefas usando o padrão correto da API Factorial
Padrão: categoria/recurso (ex: employees/employees)
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "https://api.eu2.demo.factorial.dev"
API_KEY = "eyJraWQiOiJmYWN0b3JpYWwtaWQiLCJhbGciOiJFUzI1NiJ9.eyJpYXQiOjE3NjM2NzU2ODgsImV4cCI6MjA3OTI0NTIwOCwianRpIjoiOGJhY2U3ZjItYTczZC00NDA2LWI0YjYtNDYzNTVlMDBmZjBkIiwiY2VsbCI6ImF6dXJlLWRlbW8tZ3djLWV1MiIsImNvbXBhbnlfaWQiOjI4NjkyfQ.gPtpP0-BWj2e3SiBN6dLqSL8Lz1M2LEFVTLg4kcuXUk06bAyH8YgBf5ejwSFG5TSByreYX3SCJVb_VQ9rLzGTQ"

headers = {
    'x-api-key': API_KEY,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def testar_endpoint_get(endpoint):
    """Testa um endpoint GET"""
    url = f"{BASE_URL}/api/2026-07-01/{endpoint}"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def criar_tarefa(endpoint, dados):
    """Tenta criar uma tarefa em um endpoint"""
    url = f"{BASE_URL}/api/2026-07-01/{endpoint}"
    
    try:
        response = requests.post(url, headers=headers, json=dados, timeout=10)
        
        if response.status_code in [200, 201]:
            return response.json()
        else:
            return {
                'status': response.status_code,
                'error': response.text
            }
    except Exception as e:
        return {'error': str(e)}

print("=" * 80)
print("🚀 CRIADOR DE TAREFAS - PADRÃO CORRETO DA API FACTORIAL")
print("=" * 80)

# Primeiro, testar endpoints relacionados a tarefas/projetos usando o padrão categoria/recurso
endpoints_tarefas = [
    # Padrão categoria/recurso
    'tasks/tasks',
    'tasks/task',
    'project_management/tasks',
    'project_management/task',
    'project_management/projects',
    'project_management/project',
    'projects/tasks',
    'projects/task',
    'projects/projects',
    'posts/posts',
    'posts/post',
    'todos/todos',
    'todos/todo',
    
    # Variações
    'project_management/tasks/tasks',
    'project_management/projects/projects',
]

print("\n📋 PASSO 1: Testando endpoints GET para entender estrutura...")
print("-" * 80)

endpoints_funcionais = []

for endpoint in endpoints_tarefas:
    print(f"\n🔄 Testando GET: {endpoint}")
    resultado = testar_endpoint_get(endpoint)
    
    if resultado:
        print(f"✅ Endpoint funcional: {endpoint}")
        if isinstance(resultado, dict):
            if 'data' in resultado:
                print(f"   Total de itens: {len(resultado['data']) if isinstance(resultado['data'], list) else 'N/A'}")
                if isinstance(resultado['data'], list) and len(resultado['data']) > 0:
                    print(f"   Estrutura do primeiro item: {list(resultado['data'][0].keys())[:10]}")
        endpoints_funcionais.append(endpoint)
    else:
        print(f"❌ Não funcional ou não encontrado")

# Agora tentar criar tarefas
print("\n" + "=" * 80)
print("📝 PASSO 2: Tentando criar tarefas...")
print("=" * 80)

# Dados de teste para criação
tarefas_teste = [
    {
        'title': 'Revisar documentação da API',
        'description': 'Revisar e atualizar a documentação da API da Factorial'
    },
    {
        'name': 'Tarefa de Teste',
        'description': 'Criada via API'
    },
    {
        'title': 'Implementar integração',
        'body': 'Desenvolver integração completa'
    },
]

# Se encontrou endpoints funcionais, tentar criar neles
if endpoints_funcionais:
    print(f"\n✅ Encontrados {len(endpoints_funcionais)} endpoints funcionais!")
    print("   Tentando criar tarefas nesses endpoints...\n")
    
    for endpoint in endpoints_funcionais:
        print(f"\n{'='*80}")
        print(f"📌 Tentando criar tarefa em: {endpoint}")
        print(f"{'='*80}")
        
        for i, dados_tarefa in enumerate(tarefas_teste, 1):
            print(f"\n   Teste {i}: {json.dumps(dados_tarefa, ensure_ascii=False)}")
            resultado = criar_tarefa(endpoint, dados_tarefa)
            
            if 'error' not in resultado and resultado.get('status') not in [400, 404, 422]:
                print(f"   ✅ SUCESSO! Tarefa criada!")
                print(f"   Resposta: {json.dumps(resultado, indent=2, ensure_ascii=False)}")
                break
            else:
                print(f"   ⚠️  Status: {resultado.get('status', 'N/A')}")
                if 'error' in resultado:
                    print(f"   Erro: {resultado['error'][:200]}")
else:
    # Se não encontrou endpoints funcionais, tentar criar mesmo assim
    print("\n⚠️  Nenhum endpoint GET funcional encontrado.")
    print("   Tentando criar tarefas mesmo assim nos endpoints mais prováveis...\n")
    
    endpoints_para_tentar = [
        'tasks/tasks',
        'project_management/tasks',
        'projects/projects',
        'posts/posts',
    ]
    
    for endpoint in endpoints_para_tentar:
        print(f"\n{'='*80}")
        print(f"📌 Tentando criar tarefa em: {endpoint}")
        print(f"{'='*80}")
        
        dados_tarefa = {
            'title': 'Tarefa de Teste',
            'description': 'Criada via API para teste'
        }
        
        resultado = criar_tarefa(endpoint, dados_tarefa)
        
        if 'error' not in resultado and resultado.get('status') not in [400, 404, 422]:
            print(f"✅ SUCESSO! Tarefa criada em {endpoint}!")
            print(f"Resposta: {json.dumps(resultado, indent=2, ensure_ascii=False)}")
        else:
            print(f"Status: {resultado.get('status', 'N/A')}")
            if 'error' in resultado:
                print(f"Erro: {resultado['error'][:300]}")

print("\n" + "=" * 80)
print("✅ PROCESSO CONCLUÍDO!")
print("=" * 80)


