"""
Script para testar diferentes métodos de autenticação na API Factorial
"""
import requests
import os
import json
from pathlib import Path

def load_env_config():
    """Carrega configurações do arquivo .env"""
    config = {}
    env_files = [
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
CLIENT_ID = ENV_CONFIG.get('CLIENT_ID')
CLIENT_SECRET = ENV_CONFIG.get('CLIENT_SECRET')
TOKEN_URL = ENV_CONFIG.get('TOKEN_URL') or f"{BASE_URL}/oauth/token"

print("=" * 60)
print("TESTANDO METODOS DE AUTENTICACAO - FACTORIAL API")
print("=" * 60)
print(f"Base URL: {BASE_URL}")
print()

# Método 1: API Key como x-api-key
print("METODO 1: API Key como x-api-key")
print("-" * 60)
if API_KEY:
    headers = {
        'x-api-key': API_KEY,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    try:
        url = f"{BASE_URL}/employees"
        response = requests.get(url, headers=headers, params={'limit': 1}, timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("SUCESSO! API Key funciona como x-api-key")
            data = response.json()
            print(f"Total de funcionarios: {data.get('meta', {}).get('total', 0)}")
        else:
            print(f"Falhou: {response.text[:200]}")
    except Exception as e:
        print(f"Erro: {str(e)}")
else:
    print("API_KEY nao encontrada")
print()

# Método 2: API Key como Bearer (JWT)
print("METODO 2: API Key como Bearer (JWT)")
print("-" * 60)
if API_KEY and API_KEY.startswith('eyJ'):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    try:
        url = f"{BASE_URL}/employees"
        response = requests.get(url, headers=headers, params={'limit': 1}, timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("SUCESSO! JWT funciona como Bearer")
            data = response.json()
            print(f"Total de funcionarios: {data.get('meta', {}).get('total', 0)}")
        else:
            print(f"Falhou: {response.text[:200]}")
    except Exception as e:
        print(f"Erro: {str(e)}")
else:
    print("API_KEY nao e um JWT ou nao encontrada")
print()

# Método 3: OAuth2 Client Credentials (se disponível)
print("METODO 3: OAuth2 Client Credentials")
print("-" * 60)
if CLIENT_ID and CLIENT_SECRET:
    try:
        # Tentar obter token via OAuth2
        token_data = {
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
        print(f"Obtendo token de: {TOKEN_URL}")
        token_response = requests.post(TOKEN_URL, data=token_data, timeout=5)
        print(f"Status: {token_response.status_code}")
        
        if token_response.status_code == 200:
            token_info = token_response.json()
            access_token = token_info.get('access_token')
            print(f"Token obtido com sucesso!")
            print(f"Tipo: {token_info.get('token_type', 'N/A')}")
            print(f"Expira em: {token_info.get('expires_in', 'N/A')} segundos")
            
            # Testar com o token
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            url = f"{BASE_URL}/employees"
            response = requests.get(url, headers=headers, params={'limit': 1}, timeout=5)
            print(f"Teste com token - Status: {response.status_code}")
            if response.status_code == 200:
                print("SUCESSO! OAuth2 funciona!")
                data = response.json()
                print(f"Total de funcionarios: {data.get('meta', {}).get('total', 0)}")
            else:
                print(f"Falhou: {response.text[:200]}")
        else:
            print(f"Falhou ao obter token: {token_response.text[:200]}")
    except Exception as e:
        print(f"Erro: {str(e)}")
else:
    print("CLIENT_ID e CLIENT_SECRET nao encontrados")
print()

print("=" * 60)
print("CONCLUSAO")
print("=" * 60)
print("Use o metodo que funcionou acima para configurar os scripts principais")
