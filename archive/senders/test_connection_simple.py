#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste simples de conexão com a API Factorial
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import requests

# Adicionar o diretório do projeto ao path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Carregar variáveis de ambiente
env_files = ['config_unificado.env', '.env', 'config.env']
for env_file in env_files:
    if Path(env_file).exists():
        print(f"📝 Carregando {env_file}")
        load_dotenv(env_file, override=True)
        break

def test_api_connection():
    """Testa conexão direta com a API"""
    print("\n" + "="*70)
    print("🧪 TESTE DIRETO DE CONEXÃO COM API FACTORIAL")
    print("="*70)
    
    # Obter configurações
    base_url = os.getenv('BASE_URL')
    api_key = os.getenv('API_KEY')
    auth_type = os.getenv('AUTH_TYPE', 'bearer')
    
    print(f"\n📋 Configurações:")
    print(f"   BASE_URL: {base_url}")
    print(f"   API_KEY: {api_key[:20]}...{api_key[-10:] if len(api_key) > 30 else ''}")
    print(f"   AUTH_TYPE: {auth_type}")
    
    # Preparar headers
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    if auth_type == 'bearer':
        headers['Authorization'] = f'Bearer {api_key}'
        print(f"\n🔐 Usando autenticação Bearer")
    elif auth_type == 'x-api-key':
        headers['x-api-key'] = api_key
        print(f"\n🔐 Usando autenticação x-api-key")
    
    # Testar endpoint simples
    test_url = f"{base_url}/api/2026-07-01/resources/api_public/credentials"
    print(f"\n🌐 Testando URL: {test_url}")
    print(f"📤 Headers: {headers}")
    
    try:
        response = requests.get(test_url, headers=headers, timeout=30)
        print(f"\n📥 Status Code: {response.status_code}")
        print(f"📥 Headers Response: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Conexão estabelecida com sucesso!")
            print(f"📄 Resposta: {response.text[:200]}")
        elif response.status_code == 401:
            print("❌ Erro 401: Não autorizado")
            print(f"📄 Resposta: {response.text}")
            print("\n💡 Possíveis causas:")
            print("   1. Token expirado")
            print("   2. Token inválido")
            print("   3. Formato de autenticação incorreto")
        else:
            print(f"⚠️ Status {response.status_code}: {response.reason}")
            print(f"📄 Resposta: {response.text[:500]}")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        import traceback
        traceback.print_exc()
    
    # Testar endpoint de employees
    print("\n" + "="*70)
    print("🧪 TESTANDO ENDPOINT DE EMPLOYEES")
    print("="*70)
    
    employees_url = f"{base_url}/api/2026-07-01/resources/employees/employees"
    print(f"\n🌐 Testando URL: {employees_url}")
    
    try:
        response = requests.get(
            employees_url, 
            headers=headers, 
            params={'limit': 10},
            timeout=30
        )
        print(f"\n📥 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Funcionários encontrados: {len(data.get('data', []))}")
            if data.get('data'):
                print(f"📋 Primeiros IDs: {[emp.get('id') for emp in data['data'][:5]]}")
        elif response.status_code == 401:
            print("❌ Erro 401: Não autorizado")
            print(f"📄 Resposta: {response.text}")
        else:
            print(f"⚠️ Status {response.status_code}: {response.reason}")
            print(f"📄 Resposta: {response.text[:500]}")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api_connection()

