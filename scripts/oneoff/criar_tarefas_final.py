#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script final para criar tarefas no ambiente demo da Ibero
Testa múltiplos endpoints e métodos
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "https://api.eu2.demo.factorial.dev"
API_KEY = "eyJraWQiOiJmYWN0b3JpYWwtaWQiLCJhbGciOiJFUzI1NiJ9.eyJpYXQiOjE3NjM2NzU2ODgsImV4cCI6MjA3OTI0NTIwOCwianRpIjoiOGJhY2U3ZjItYTczZC00NDA2LWI0YjYtNDYzNTVlMDBmZjBkIiwiY2VsbCI6ImF6dXJlLWRlbW8tZ3djLWV1MiIsImNvbXBhbnlfaWQiOjI4NjkyfQ.gPtpP0-BWj2e3SiBN6dLqSL8Lz1M2LEFVTLg4kcuXUk06bAyH8YgBf5ejwSFG5TSByreYX3SCJVb_VQ9rLzGTQ"

def criar_tarefa_em_endpoint(endpoint, dados_tarefa):
    """Tenta criar uma tarefa em um endpoint específico"""
    url = f"{BASE_URL}/api/2026-07-01/{endpoint}"
    
    headers = {
        'x-api-key': API_KEY,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    try:
        print(f"\n🔄 Tentando POST em: {endpoint}")
        print(f"   URL: {url}")
        print(f"   Dados: {json.dumps(dados_tarefa, indent=2, ensure_ascii=False)}")
        
        response = requests.post(url, headers=headers, json=dados_tarefa, timeout=10)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            resultado = response.json()
            print(f"   ✅ SUCESSO! Tarefa criada!")
            print(f"   Resposta: {json.dumps(resultado, indent=2, ensure_ascii=False)}")
            return True, resultado
        else:
            print(f"   ❌ Erro: {response.status_code}")
            print(f"   Resposta: {response.text[:300]}")
            return False, response.text
            
    except Exception as e:
        print(f"   ❌ Exceção: {e}")
        return False, str(e)

print("=" * 80)
print("🚀 CRIADOR DE TAREFAS - AMBIENTE DEMO IBERO")
print("=" * 80)

# Primeiro, verificar se a API está funcionando
print("\n📋 PASSO 1: Verificando conexão com a API...")
url_test = f"{BASE_URL}/api/2026-07-01/resources/api_public/credentials"
headers = {
    'x-api-key': API_KEY,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

try:
    response = requests.get(url_test, headers=headers, timeout=10)
    if response.status_code == 200:
        data = response.json()
        company_name = data.get('data', [{}])[0].get('name', 'N/A')
        company_id = data.get('data', [{}])[0].get('company_id', 'N/A')
        print(f"✅ API funcionando!")
        print(f"   Empresa: {company_name}")
        print(f"   Company ID: {company_id}")
    else:
        print(f"⚠️  API retornou status {response.status_code}")
except Exception as e:
    print(f"❌ Erro ao conectar: {e}")
    exit(1)

# Lista completa de endpoints para tentar
endpoints_para_testar = [
    # Endpoints diretos
    'tasks',
    'task',
    'tasks/tasks',
    'tasks/task',
    
    # Project Management
    'project_management/tasks',
    'project_management/task',
    'project_management/projects',
    'project_management/project',
    
    # Projects
    'projects',
    'project',
    'projects/tasks',
    'projects/projects',
    
    # Posts (pode incluir tarefas)
    'posts',
    'post',
    'posts/posts',
    
    # Outros
    'todos',
    'todo',
    'items',
    'item',
]

# Diferentes formatos de dados para testar
formatos_dados = [
    {
        'nome': 'Formato 1: title + description',
        'dados': {
            'title': 'Revisar documentação da API',
            'description': 'Revisar e atualizar a documentação da API da Factorial'
        }
    },
    {
        'nome': 'Formato 2: name + description',
        'dados': {
            'name': 'Implementar integração de tarefas',
            'description': 'Desenvolver integração completa para criação de tarefas via API'
        }
    },
    {
        'nome': 'Formato 3: title + body',
        'dados': {
            'title': 'Teste de tarefa',
            'body': 'Corpo da tarefa de teste'
        }
    },
    {
        'nome': 'Formato 4: task simples',
        'dados': {
            'task': {
                'title': 'Tarefa de teste',
                'description': 'Descrição da tarefa'
            }
        }
    },
]

print("\n" + "=" * 80)
print("📝 PASSO 2: Tentando criar tarefas em todos os endpoints possíveis...")
print("=" * 80)

tarefas_criadas = []

for endpoint in endpoints_para_testar:
    print(f"\n{'='*80}")
    print(f"📍 Testando endpoint: {endpoint}")
    print(f"{'='*80}")
    
    for formato in formatos_dados:
        print(f"\n   📌 {formato['nome']}")
        sucesso, resultado = criar_tarefa_em_endpoint(endpoint, formato['dados'])
        
        if sucesso:
            tarefas_criadas.append({
                'endpoint': endpoint,
                'formato': formato['nome'],
                'resultado': resultado
            })
            print(f"\n   ✅ TAREFA CRIADA COM SUCESSO!")
            break  # Se funcionou, não precisa testar outros formatos
    
    if tarefas_criadas and tarefas_criadas[-1]['endpoint'] == endpoint:
        break  # Se encontrou um que funciona, pode parar

# Resumo final
print("\n" + "=" * 80)
print("📊 RESUMO FINAL")
print("=" * 80)

if tarefas_criadas:
    print(f"\n✅ Total de tarefas criadas: {len(tarefas_criadas)}")
    for tarefa in tarefas_criadas:
        print(f"\n   📌 Endpoint: {tarefa['endpoint']}")
        print(f"   📋 Formato: {tarefa['formato']}")
        print(f"   📄 ID/Título: {tarefa['resultado'].get('id', tarefa['resultado'].get('title', 'N/A'))}")
else:
    print("\n❌ Nenhuma tarefa foi criada com sucesso.")
    print("\n💡 Possíveis razões:")
    print("   1. O recurso de tarefas pode não estar disponível neste ambiente demo")
    print("   2. A chave API pode não ter permissões para criar tarefas")
    print("   3. O endpoint de tarefas pode ter um nome diferente")
    print("   4. Pode ser necessário habilitar o recurso de tarefas no ambiente")
    print("\n📚 Próximos passos:")
    print("   - Verificar a documentação da API Factorial")
    print("   - Verificar se o recurso 'tasks' está incluído no escopo da chave API")
    print("   - Contatar suporte da Factorial para confirmar disponibilidade")

print("\n" + "=" * 80)


