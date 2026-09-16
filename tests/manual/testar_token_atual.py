#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testa qual token está sendo usado pelo coletor
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz do projeto ao path
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from ultimate_collector.core.config import Config
from ultimate_collector.core.api_client import APIClient
import base64
import json
from datetime import datetime

def decode_jwt(token):
    """Decodifica um token JWT"""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
        payload = parts[1]
        payload += '=' * (4 - len(payload) % 4)
        decoded = base64.urlsafe_b64decode(payload)
        return json.loads(decoded)
    except Exception as e:
        print(f"Erro ao decodificar: {e}")
        return None

def main():
    print("=" * 80)
    print("TESTE DE TOKEN - Verificando qual token o coletor esta usando")
    print("=" * 80)
    
    # Carregar configuração
    config = Config()
    print(f"\nConfiguracao carregada:")
    print(f"  BASE_URL: {config.BASE_URL}")
    print(f"  AUTH_TYPE: {config.AUTH_TYPE}")
    print(f"  API_KEY (primeiros 50 chars): {config.API_KEY[:50]}...")
    
    # Decodificar token
    if config.API_KEY:
        payload = decode_jwt(config.API_KEY)
        if payload:
            print(f"\nToken decodificado:")
            print(f"  Company ID: {payload.get('company_id', 'N/A')}")
            print(f"  Cell: {payload.get('cell', 'N/A')}")
            exp = payload.get('exp', 0)
            if exp:
                exp_date = datetime.fromtimestamp(exp)
                print(f"  Expira em: {exp_date}")
    
    # Testar conexão com API
    print(f"\n" + "=" * 80)
    print("Testando conexao com API...")
    print("=" * 80)
    
    try:
        client = APIClient()
        
        # Testar endpoint de companies para ver qual empresa retorna
        print("\nFazendo requisicao para /companies/companies...")
        response = client.get('companies/companies')
        
        if response and 'data' in response:
            companies = response.get('data', [])
            if companies:
                company = companies[0]
                print(f"\nEmpresa retornada pela API:")
                print(f"  Company ID: {company.get('company_id', 'N/A')}")
                print(f"  Nome: {company.get('name', 'N/A')}")
                print(f"  Legal Name: {company.get('legal_name', 'N/A')}")
                
                # Comparar com token
                token_company_id = payload.get('company_id') if payload else None
                api_company_id = company.get('company_id')
                
                if token_company_id == api_company_id:
                    print(f"\n[OK] Token e API estao consistentes! (Company ID: {api_company_id})")
                else:
                    print(f"\n[ERRO] INCONSISTENCIA!")
                    print(f"  Token aponta para Company ID: {token_company_id}")
                    print(f"  API retornou Company ID: {api_company_id}")
            else:
                print("\n[AVISO] Nenhuma empresa retornada pela API")
        else:
            print(f"\n[ERRO] Resposta invalida da API: {response}")
            
    except Exception as e:
        print(f"\n[ERRO] Erro ao testar API: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n" + "=" * 80)

if __name__ == '__main__':
    main()
