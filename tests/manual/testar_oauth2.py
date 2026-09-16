#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testa OAuth2 para obter um token válido
"""

import requests
import json

BASE_URL = "https://api.eu2.demo.factorial.dev"
CLIENT_ID = "OrfZ4a1ghePikdXTBzveMLVShNAqxIQtQIlqGVM2TGU"
CLIENT_SECRET = "w8FPABgXQy3RtRC1ngXFksR1nvXsV0SWnafL7-CUL8E"
TOKEN_URL = f"{BASE_URL}/oauth/token"

print("=" * 80)
print("TESTANDO OAUTH2")
print("=" * 80)

# Tentar obter token via OAuth2
print(f"\nObtendo token OAuth2 de: {TOKEN_URL}")

try:
    response = requests.post(
        TOKEN_URL,
        data={
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        timeout=10
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get('access_token')
        print(f"[OK] Token obtido com sucesso!")
        print(f"Token (primeiros 50 chars): {access_token[:50]}...")
        
        # Testar usar o token
        print(f"\nTestando token com endpoint /companies/companies...")
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        test_url = f"{BASE_URL}/companies/companies"
        test_response = requests.get(test_url, headers=headers, timeout=10)
        print(f"Status: {test_response.status_code}")
        
        if test_response.status_code == 200:
            data = test_response.json()
            if 'data' in data and len(data['data']) > 0:
                company = data['data'][0]
                print(f"[OK] Sucesso! Company ID: {company.get('company_id')}")
                print(f"Nome: {company.get('name')}")
                print(f"Legal Name: {company.get('legal_name')}")
        else:
            print(f"[ERRO] {test_response.status_code}: {test_response.text[:200]}")
    else:
        print(f"[ERRO] Falha ao obter token: {response.status_code}")
        print(f"Resposta: {response.text[:200]}")
        
except Exception as e:
    print(f"[EXCECAO] {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
