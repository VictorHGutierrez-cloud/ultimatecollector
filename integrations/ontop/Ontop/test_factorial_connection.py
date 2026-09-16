"""
Script de diagnóstico para testar a conexão com a API Factorial
Use este script para identificar problemas antes de executar o script principal
"""

import requests
import os
import json
from pathlib import Path

def load_env_config():
    """Carrega configurações do arquivo .env"""
    config = {}
    
    # Tentar encontrar arquivo .env
    env_files = [
        Path('.env'),
        Path('config_unificado.env'),
        Path('../config_unificado.env'),
        Path('../../config_unificado.env')
    ]
    
    env_file = None
    for file_path in env_files:
        if file_path.exists():
            env_file = file_path
            break
    
    if env_file:
        print(f"Carregando configuracoes de: {env_file}")
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    else:
        print("AVISO: Arquivo .env nao encontrado, usando variaveis de ambiente")
    
    return config

# Carregar configurações
ENV_CONFIG = load_env_config()

# Configurações
API_KEY = ENV_CONFIG.get('API_KEY') or os.getenv('FACTORIAL_API_KEY') or os.getenv('API_KEY')
BASE_URL = ENV_CONFIG.get('BASE_URL') or os.getenv('FACTORIAL_BASE_URL') or 'https://api.factorialhr.com'
API_VERSION = ENV_CONFIG.get('API_VERSION') or os.getenv('API_VERSION') or '2026-07-01'
AUTH_TYPE = ENV_CONFIG.get('AUTH_TYPE', 'bearer').lower()

# Headers - Se a API_KEY começa com 'eyJ' é um JWT e deve usar Bearer
if API_KEY and API_KEY.startswith('eyJ'):
    # JWT token - sempre usar Bearer
    HEADERS = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
elif AUTH_TYPE == 'x-api-key':
    HEADERS = {
        'x-api-key': API_KEY,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
else:
    HEADERS = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

def test_connection():
    """Testa a conexão básica com a API"""
    print("=" * 60)
    print("TESTE DE CONEXAO - API FACTORIAL")
    print("=" * 60)
    print()
    
    # 1. Verificar API Key
    print("1. Verificando API Key...")
    if not API_KEY:
        print("   ERRO: API Key nao configurada!")
        print("   Configure no arquivo config_unificado.env ou use variavel de ambiente")
        return False
    else:
        masked_key = API_KEY[:8] + '...' + API_KEY[-4:] if len(API_KEY) > 12 else '***'
        print(f"   OK: API Key configurada: {masked_key}")
        print(f"   Base URL: {BASE_URL}")
        print(f"   Versao API: {API_VERSION}")
        print(f"   Tipo de Auth: {AUTH_TYPE}")
    print()
    
    # 2. Testar endpoint simples (employees)
    print("2. Testando endpoint de funcionarios...")
    try:
        # Tentar diferentes formatos de endpoint (formato correto do coletor anterior)
        endpoints = [
            f"{BASE_URL}/api/{API_VERSION}/resources/employees/employees",
            f"{BASE_URL}/api/{API_VERSION}/resources/employees",
            f"{BASE_URL}/employees",
            f"{BASE_URL}/api/employees",
        ]
        
        response = None
        working_url = None
        for url in endpoints:
            print(f"   Tentando: {url}")
            test_response = requests.get(url, headers=HEADERS, params={'limit': 1}, timeout=5)
            print(f"   Status: {test_response.status_code}")
            if test_response.status_code == 200:
                response = test_response
                working_url = url
                print(f"   SUCESSO! Endpoint valido: {url}")
                break
            elif test_response.status_code == 401:
                print(f"   Auth incorreta para: {url}")
            elif test_response.status_code == 404:
                print(f"   Endpoint nao encontrado: {url}")
            else:
                print(f"   Status inesperado: {test_response.status_code}")
        
        if not response:
            print("   ERRO: Nenhum endpoint valido encontrado ou autenticacao falhou")
            return False
        
        url = working_url
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            total = data.get('meta', {}).get('total', 0)
            print(f"   OK: Conexao OK! Total de funcionarios: {total}")
        elif response.status_code == 401:
            print("   ERRO 401: API Key invalida ou expirada")
            print(f"   Resposta: {response.text}")
            return False
        elif response.status_code == 403:
            print("   ERRO 403: Sem permissao para acessar este recurso")
            print(f"   Resposta: {response.text}")
            return False
        else:
            print(f"   AVISO: Status inesperado: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("   ERRO: Erro de conexao - Nao foi possivel conectar a API")
        print("   Verifique sua conexao com a internet")
        return False
    except requests.exceptions.Timeout:
        print("   ERRO: Timeout - A requisicao demorou muito")
        return False
    except Exception as e:
        print(f"   ERRO inesperado: {str(e)}")
        return False
    
    print()
    
    # 3. Testar endpoint de policy periods
    print("3. Testando endpoint de policy periods...")
    try:
        url = f"{BASE_URL}/api/{API_VERSION}/resources/payroll/policy_periods"
        response = requests.get(url, headers=HEADERS, params={'limit': 1})
        
        if response.status_code == 200:
            data = response.json()
            total = len(data.get('data', []))
            print(f"   OK: Policy periods acessiveis! Encontrados: {total}")
        else:
            print(f"   AVISO: Status: {response.status_code}")
            print(f"   Resposta: {response.text}")
            
    except Exception as e:
        print(f"   AVISO: Erro: {str(e)}")
    
    print()
    
    # 4. Testar endpoint de taxonomies
    print("4. Testando endpoint de taxonomies...")
    try:
        url = f"{BASE_URL}/api/{API_VERSION}/resources/contracts/taxonomies"
        response = requests.get(url, headers=HEADERS, params={'limit': 1})
        
        if response.status_code == 200:
            data = response.json()
            total = len(data.get('data', []))
            print(f"   OK: Taxonomies acessiveis! Encontradas: {total}")
        else:
            print(f"   AVISO: Status: {response.status_code}")
            print(f"   Resposta: {response.text}")
            
    except Exception as e:
        print(f"   AVISO: Erro: {str(e)}")
    
    print()
    print("=" * 60)
    print("TESTE CONCLUIDO")
    print("=" * 60)
    print()
    print("Se todos os testes passaram, voce pode executar o script principal:")
    print("   python test_factorial_data_insert.py")
    
    return True

if __name__ == '__main__':
    test_connection()
