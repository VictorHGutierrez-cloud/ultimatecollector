"""
Script para testar a estrutura da API e encontrar os endpoints corretos
"""
import requests
import os
from pathlib import Path

def load_env_config():
    """Carrega configurações do arquivo .env"""
    config = {}
    env_files = [
        Path('.env'),
        Path('config_unificado.env'),
        Path('../config_unificado.env'),
        Path('../../config_unificado.env')
    ]
    
    for file_path in env_files:
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
            break
    return config

ENV_CONFIG = load_env_config()
API_KEY = ENV_CONFIG.get('API_KEY') or os.getenv('API_KEY')
BASE_URL = ENV_CONFIG.get('BASE_URL') or 'https://api.factorialhr.com'
API_VERSION = ENV_CONFIG.get('API_VERSION') or '2026-07-01'
AUTH_TYPE = ENV_CONFIG.get('AUTH_TYPE', 'bearer').lower()

# Testar diferentes formatos de autenticação
auth_variations = []
if AUTH_TYPE == 'x-api-key':
    auth_variations = [
        {'x-api-key': API_KEY},
        {'X-API-Key': API_KEY},
        {'X-Api-Key': API_KEY},
        {'Authorization': f'x-api-key {API_KEY}'},
    ]
else:
    auth_variations = [
        {'Authorization': f'Bearer {API_KEY}'},
    ]

print("=" * 60)
print("TESTANDO ESTRUTURA DA API")
print("=" * 60)
print(f"Base URL: {BASE_URL}")
print(f"API Version: {API_VERSION}")
print(f"Auth Type: {AUTH_TYPE}")
print()

import json

# Testar diferentes formatos de endpoint e autenticação
endpoints_to_test = [
    f"/api/{API_VERSION}/resources/employees",
    f"/api/{API_VERSION}/employees",
    f"/api/v1/employees",
    f"/employees",
]

found = False
for endpoint in endpoints_to_test:
    if found:
        break
    for auth_header in auth_variations:
        url = f"{BASE_URL}{endpoint}"
        headers = {**auth_header, 'Content-Type': 'application/json', 'Accept': 'application/json'}
        print(f"Testando: {url}")
        print(f"  Auth: {list(auth_header.keys())[0]}")
        try:
            response = requests.get(url, headers=headers, params={'limit': 1}, timeout=5)
            print(f"  Status: {response.status_code}")
            if response.status_code == 200:
                print(f"  SUCESSO! Endpoint: {endpoint}, Auth: {list(auth_header.keys())[0]}")
                data = response.json()
                print(f"  Resposta: {str(data)[:200]}...")
                found = True
                break
            elif response.status_code == 401:
                print(f"  Auth incorreta")
            elif response.status_code == 404:
                print(f"  Endpoint nao encontrado")
            else:
                print(f"  Resposta: {response.text[:200]}")
        except Exception as e:
            print(f"  Erro: {str(e)}")
    print()
