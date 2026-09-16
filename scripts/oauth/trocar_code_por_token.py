#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Troca o código de autorização OAuth2 por um access token
"""

import requests
import json

# Configurações
CLIENT_ID = "BFBMBN9v0DIN00xRjKJJNEP44nN_rqqV_1wGZvHtUcc"
CLIENT_SECRET = "w8FPABgXQy3RtRC1ngXFksR1nvXsV0SWnafL7-CUL8E"
REDIRECT_URI = "https://app.eu2.demo.factorial.dev/"
TOKEN_URL = "https://api.eu2.demo.factorial.dev/oauth/token"

# Código de autorização fornecido
AUTHORIZATION_CODE = "QhHO4a0kqnich7XWkt4PGwzrfMkmK8lyQZgpEV2-Hnc"

print("=" * 80)
print("TROCANDO CODIGO DE AUTORIZACAO POR ACCESS TOKEN")
print("=" * 80)

# Preparar dados para a requisição
data = {
    'grant_type': 'authorization_code',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'code': AUTHORIZATION_CODE,
    'redirect_uri': REDIRECT_URI
}

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

print(f"\nFazendo requisicao para: {TOKEN_URL}")
print(f"Codigo de autorizacao: {AUTHORIZATION_CODE[:20]}...")

try:
    response = requests.post(TOKEN_URL, data=data, headers=headers, timeout=10)
    
    print(f"\nStatus: {response.status_code}")
    
    if response.status_code == 200:
        token_data = response.json()
        
        access_token = token_data.get('access_token')
        refresh_token = token_data.get('refresh_token')
        expires_in = token_data.get('expires_in')
        token_type = token_data.get('token_type', 'Bearer')
        scope = token_data.get('scope', '')
        
        print("\n[OK] Token obtido com sucesso!")
        print(f"\nAccess Token (primeiros 50 chars): {access_token[:50]}...")
        print(f"Token Type: {token_type}")
        print(f"Expira em: {expires_in} segundos ({expires_in/3600:.1f} horas)")
        if refresh_token:
            print(f"Refresh Token: {refresh_token[:30]}...")
        if scope:
            print(f"Scopes: {scope[:100]}...")
        
        print("\n" + "=" * 80)
        print("ATUALIZE O config_unificado.env COM:")
        print("=" * 80)
        print(f"API_KEY={access_token}")
        print(f"AUTH_TYPE=bearer")
        print("\n" + "=" * 80)
        
        # Testar o token
        print("\n[TESTE] Testando token com API...")
        test_headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        test_url = "https://api.eu2.demo.factorial.dev/companies/companies"
        test_response = requests.get(test_url, headers=test_headers, timeout=10)
        
        print(f"Status do teste: {test_response.status_code}")
        
        if test_response.status_code == 200:
            test_data = test_response.json()
            if 'data' in test_data and len(test_data['data']) > 0:
                company = test_data['data'][0]
                print(f"\n[OK] Token funcionando perfeitamente!")
                print(f"Company ID: {company.get('company_id')}")
                print(f"Nome: {company.get('name')}")
                print(f"Legal Name: {company.get('legal_name')}")
            else:
                print(f"[AVISO] Resposta vazia: {test_data}")
        else:
            print(f"[ERRO] Teste falhou: {test_response.status_code}")
            print(f"Resposta: {test_response.text[:200]}")
            
    else:
        print(f"\n[ERRO] Falha ao obter token: {response.status_code}")
        print(f"Resposta: {response.text}")
        
except Exception as e:
    print(f"\n[EXCECAO] Erro: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
