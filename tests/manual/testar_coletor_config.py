#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testa se o coletor está usando a configuração correta
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz do projeto ao path
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from ultimate_collector.collectors.hr_data_masterultimate import HRDataMasterUltimate
import base64
import json

print("=" * 80)
print("TESTANDO CONFIGURACAO DO COLETOR")
print("=" * 80)

try:
    collector = HRDataMasterUltimate()
    
    print(f"\nConfiguracao do coletor:")
    print(f"  BASE_URL: {collector.config.BASE_URL}")
    print(f"  AUTH_TYPE: {collector.config.AUTH_TYPE}")
    print(f"  API_VERSION: {collector.config.API_VERSION}")
    print(f"  API_KEY (primeiros 50 chars): {collector.config.API_KEY[:50]}...")
    
    # Decodificar token
    if collector.config.API_KEY:
        try:
            parts = collector.config.API_KEY.split('.')
            payload = parts[1]
            payload += '=' * (4 - len(payload) % 4)
            decoded = base64.urlsafe_b64decode(payload)
            data = json.loads(decoded)
            print(f"\nToken decodificado:")
            print(f"  Company ID: {data.get('company_id', 'N/A')}")
            print(f"  Cell: {data.get('cell', 'N/A')}")
            
            if data.get('company_id') == 55229:
                print(f"\n[OK] Token correto! Company ID 55229 (Factorial RH Africa)")
            else:
                print(f"\n[ERRO] Token incorreto! Esperado Company ID 55229, mas encontrado {data.get('company_id')}")
        except Exception as e:
            print(f"\n[ERRO] Erro ao decodificar token: {e}")
    
    # Testar inicialização do cliente
    print(f"\n" + "=" * 80)
    print("Testando inicializacao do cliente...")
    print("=" * 80)
    
    collector.client = None  # Forçar recriação
    collector.config = collector.config.__class__()  # Recriar config
    
    # Verificar novamente
    print(f"\nConfig apos recriacao:")
    print(f"  API_KEY (primeiros 50 chars): {collector.config.API_KEY[:50]}...")
    
    if collector.config.API_KEY:
        try:
            parts = collector.config.API_KEY.split('.')
            payload = parts[1]
            payload += '=' * (4 - len(payload) % 4)
            decoded = base64.urlsafe_b64decode(payload)
            data = json.loads(decoded)
            print(f"  Company ID: {data.get('company_id', 'N/A')}")
        except:
            pass
    
except Exception as e:
    print(f"\n[ERRO] Erro ao testar coletor: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
