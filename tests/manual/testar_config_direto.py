#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testa o carregamento direto do config_unificado.env
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import base64
import json

# Limpar variáveis de ambiente relacionadas
for key in ['API_KEY', 'AUTH_TYPE', 'BASE_URL']:
    if key in os.environ:
        del os.environ[key]

# Carregar diretamente do config_unificado.env
project_root = Path(__file__).resolve().parents[2]
unified_path = project_root / 'config_unificado.env'

print("=" * 80)
print("TESTE DIRETO DO ARQUIVO DE CONFIGURACAO")
print("=" * 80)

print(f"\nCarregando arquivo: {unified_path}")
print(f"Arquivo existe: {unified_path.exists()}")

if unified_path.exists():
    # Carregar com override
    load_dotenv(unified_path, override=True)
    
    # Ler diretamente do arquivo também
    print("\nLendo diretamente do arquivo:")
    with open(unified_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('API_KEY='):
                token_from_file = line.split('=', 1)[1]
                print(f"  Token do arquivo (primeiros 50 chars): {token_from_file[:50]}...")
                
                # Decodificar
                try:
                    parts = token_from_file.split('.')
                    if len(parts) == 3:
                        payload = parts[1]
                        payload += '=' * (4 - len(payload) % 4)
                        decoded = base64.urlsafe_b64decode(payload)
                        data = json.loads(decoded)
                        print(f"  Company ID do arquivo: {data.get('company_id')}")
                except Exception as e:
                    print(f"  Erro ao decodificar: {e}")
            elif line.startswith('AUTH_TYPE='):
                auth_from_file = line.split('=', 1)[1]
                print(f"  AUTH_TYPE do arquivo: {auth_from_file}")
    
    print("\nLendo das variaveis de ambiente (apos load_dotenv):")
    api_key_env = os.getenv('API_KEY', '')
    auth_type_env = os.getenv('AUTH_TYPE', '')
    print(f"  API_KEY (primeiros 50 chars): {api_key_env[:50] if api_key_env else 'VAZIO'}...")
    print(f"  AUTH_TYPE: {auth_type_env}")
    
    if api_key_env:
        try:
            parts = api_key_env.split('.')
            if len(parts) == 3:
                payload = parts[1]
                payload += '=' * (4 - len(payload) % 4)
                decoded = base64.urlsafe_b64decode(payload)
                data = json.loads(decoded)
                print(f"  Company ID das variaveis: {data.get('company_id')}")
        except Exception as e:
            print(f"  Erro ao decodificar: {e}")
    
    # Comparar
    if api_key_env and token_from_file:
        if api_key_env == token_from_file:
            print("\n[OK] Token das variaveis e do arquivo sao iguais!")
        else:
            print("\n[ERRO] Token das variaveis e do arquivo sao DIFERENTES!")
            print(f"  Token arquivo (primeiros 50): {token_from_file[:50]}...")
            print(f"  Token env (primeiros 50): {api_key_env[:50]}...")

print("\n" + "=" * 80)
