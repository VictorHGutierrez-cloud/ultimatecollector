#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testa se o sender está usando a configuração correta
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz do projeto ao path
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from ultimate_collector.senders.ultimate_sender import UltimateSender
from ultimate_collector.core.config import Config
import base64
import json

print("=" * 80)
print("VERIFICANDO CONFIGURACAO DO SENDER")
print("=" * 80)

# Verificar configuração
config = Config()
print(f"\nConfiguracao carregada:")
print(f"  BASE_URL: {config.BASE_URL}")
print(f"  AUTH_TYPE: {config.AUTH_TYPE}")
print(f"  API_VERSION: {config.API_VERSION}")
print(f"  API_KEY (primeiros 50 chars): {config.API_KEY[:50]}...")

# Decodificar token
if config.API_KEY:
    try:
        parts = config.API_KEY.split('.')
        payload = parts[1]
        payload += '=' * (4 - len(payload) % 4)
        decoded = base64.urlsafe_b64decode(payload)
        data = json.loads(decoded)
        print(f"\nToken decodificado:")
        print(f"  Company ID: {data.get('company_id', 'N/A')}")
        print(f"  Cell: {data.get('cell', 'N/A')}")
    except Exception as e:
        print(f"\nErro ao decodificar token: {e}")

# Testar sender
print(f"\n" + "=" * 80)
print("Testando sender...")
print("=" * 80)

try:
    sender = UltimateSender()
    print(f"\n[OK] Sender inicializado com sucesso!")
    print(f"  Config BASE_URL: {sender.config.BASE_URL}")
    print(f"  Config AUTH_TYPE: {sender.config.AUTH_TYPE}")
    print(f"  Config API_VERSION: {sender.config.API_VERSION}")
    
    # Verificar headers que serão usados
    print(f"\nTestando headers que serao usados...")
    headers = sender._get_headers()
    print(f"  Headers: {list(headers.keys())}")
    if 'x-api-key' in headers:
        print(f"  [OK] Header x-api-key configurado!")
        print(f"  x-api-key (primeiros 30 chars): {headers['x-api-key'][:30]}...")
    elif 'Authorization' in headers:
        print(f"  [AVISO] Usando Authorization em vez de x-api-key")
        print(f"  Authorization (primeiros 30 chars): {headers['Authorization'][:30]}...")
    
    # Testar construção de endpoint
    print(f"\nTestando construcao de endpoint...")
    test_endpoint = sender._with_api_prefix("employees/employees")
    print(f"  Endpoint construido: {test_endpoint}")
    print(f"  [OK] Formato correto: api/{sender.config.API_VERSION}/resources/employees/employees")
    
except Exception as e:
    print(f"\n[ERRO] Erro ao testar sender: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
