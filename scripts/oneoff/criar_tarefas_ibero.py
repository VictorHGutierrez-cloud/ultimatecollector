#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar tarefas no ambiente demo da Ibero (Factorial)
"""

import requests
import json
from datetime import datetime, timedelta

# Configurações da API
BASE_URL = "https://api.eu2.demo.factorial.dev"
API_KEY = "eyJraWQiOiJmYWN0b3JpYWwtaWQiLCJhbGciOiJFUzI1NiJ9.eyJpYXQiOjE3NjM2NzU2ODgsImV4cCI6MjA3OTI0NTIwOCwianRpIjoiOGJhY2U3ZjItYTczZC00NDA2LWI0YjYtNDYzNTVlMDBmZjBkIiwiY2VsbCI6ImF6dXJlLWRlbW8tZ3djLWV1MiIsImNvbXBhbnlfaWQiOjI4NjkyfQ.gPtpP0-BWj2e3SiBN6dLqSL8Lz1M2LEFVTLg4kcuXUk06bAyH8YgBf5ejwSFG5TSByreYX3SCJVb_VQ9rLzGTQ"

def criar_tarefa(titulo, descricao=None, assignee_id=None, due_date=None, project_id=None):
    """
    Cria uma tarefa na Factorial
    
    Parâmetros:
    - titulo: Título da tarefa (obrigatório)
    - descricao: Descrição da tarefa (opcional)
    - assignee_id: ID do funcionário responsável (opcional)
    - due_date: Data de vencimento no formato YYYY-MM-DD (opcional)
    - project_id: ID do projeto (opcional)
    """
    
    # Headers da requisição
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    # Dados da tarefa
    task_data = {
        'title': titulo
    }
    
    # Adicionar campos opcionais se fornecidos
    if descricao:
        task_data['description'] = descricao
    
    if assignee_id:
        task_data['assignee_id'] = assignee_id
    
    if due_date:
        task_data['due_date'] = due_date
    
    if project_id:
        task_data['project_id'] = project_id
    
    # Endpoint da API (tentando diferentes versões)
    endpoints = [
        'api/2026-07-01/tasks',
        'api/v1/tasks',
        'tasks'
    ]
    
    for endpoint in endpoints:
        url = f"{BASE_URL}/{endpoint}"
        
        try:
            print(f"\n🔄 Tentando criar tarefa em: {url}")
            print(f"📝 Dados: {json.dumps(task_data, indent=2, ensure_ascii=False)}")
            
            response = requests.post(url, headers=headers, json=task_data, timeout=30)
            
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code in [200, 201]:
                result = response.json()
                print(f"✅ Tarefa criada com sucesso!")
                print(f"📄 Resposta: {json.dumps(result, indent=2, ensure_ascii=False)}")
                return result
            else:
                print(f"❌ Erro: {response.status_code}")
                print(f"📄 Resposta: {response.text}")
                # Se não funcionou, tenta o próximo endpoint
                continue
                
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")
            continue
    
    print("\n❌ Não foi possível criar a tarefa em nenhum endpoint testado")
    return None

def listar_tarefas():
    """
    Lista tarefas existentes para entender a estrutura
    """
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    endpoints = [
        'api/2026-07-01/tasks',
        'api/v1/tasks',
        'tasks'
    ]
    
    for endpoint in endpoints:
        url = f"{BASE_URL}/{endpoint}"
        
        try:
            print(f"\n🔄 Tentando listar tarefas em: {url}")
            
            response = requests.get(url, headers=headers, timeout=30)
            
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Tarefas encontradas!")
                print(f"📄 Resposta: {json.dumps(result, indent=2, ensure_ascii=False)}")
                return result
            else:
                print(f"📄 Resposta: {response.text}")
                continue
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            continue
    
    return None

def listar_funcionarios():
    """
    Lista funcionários para obter IDs para atribuir tarefas
    """
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    url = f"{BASE_URL}/api/2026-07-01/employees"
    
    try:
        print(f"\n🔄 Listando funcionários...")
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Funcionários encontrados: {len(result.get('data', []))}")
            return result
        else:
            print(f"❌ Erro: {response.status_code}")
            print(f"📄 Resposta: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

def main():
    """
    Função principal - cria algumas tarefas de exemplo
    """
    print("=" * 60)
    print("🚀 CRIADOR DE TAREFAS - AMBIENTE DEMO IBERO")
    print("=" * 60)
    
    # Primeiro, vamos listar tarefas existentes para entender a estrutura
    print("\n📋 PASSO 1: Listando tarefas existentes...")
    listar_tarefas()
    
    # Listar funcionários para ter IDs disponíveis
    print("\n👥 PASSO 2: Listando funcionários...")
    funcionarios = listar_funcionarios()
    
    # Criar algumas tarefas de exemplo
    print("\n📝 PASSO 3: Criando tarefas de exemplo...")
    
    # Tarefa 1: Simples
    print("\n" + "-" * 60)
    print("📌 Tarefa 1: Tarefa Simples")
    print("-" * 60)
    criar_tarefa(
        titulo="Revisar documentação da API",
        descricao="Revisar e atualizar a documentação da API da Factorial"
    )
    
    # Tarefa 2: Com data de vencimento
    print("\n" + "-" * 60)
    print("📌 Tarefa 2: Tarefa com Prazo")
    print("-" * 60)
    data_vencimento = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    criar_tarefa(
        titulo="Implementar integração de tarefas",
        descricao="Desenvolver integração completa para criação de tarefas via API",
        due_date=data_vencimento
    )
    
    # Tarefa 3: Com funcionário (se houver funcionários)
    if funcionarios and 'data' in funcionarios and len(funcionarios['data']) > 0:
        print("\n" + "-" * 60)
        print("📌 Tarefa 3: Tarefa Atribuída")
        print("-" * 60)
        primeiro_funcionario = funcionarios['data'][0]
        funcionario_id = primeiro_funcionario.get('id')
        funcionario_nome = primeiro_funcionario.get('first_name', 'Funcionário')
        
        criar_tarefa(
            titulo=f"Teste de atribuição para {funcionario_nome}",
            descricao="Tarefa de teste criada via API",
            assignee_id=funcionario_id
        )
    
    print("\n" + "=" * 60)
    print("✅ PROCESSO CONCLUÍDO!")
    print("=" * 60)

if __name__ == "__main__":
    main()


