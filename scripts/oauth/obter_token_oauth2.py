#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para obter token OAuth2 da Factorial
Usa Authorization Code Flow
"""

import requests
import json
import webbrowser
from urllib.parse import urlencode, parse_qs, urlparse

# Configurações da aplicação OAuth2
CLIENT_ID = "BFBMBN9v0DIN00xRjKJJNEP44nN_rqqV_1wGZvHtUcc"
CLIENT_SECRET = "w8FPABgXQy3RtRC1ngXFksR1nvXsV0SWnafL7-CUL8E"
REDIRECT_URI = "https://app.eu2.demo.factorial.dev/"
AUTHORIZATION_URL = "https://app.eu2.demo.factorial.dev/oauth/authorize"
TOKEN_URL = "https://api.eu2.demo.factorial.dev/oauth/token"

# Scopes necessários
SCOPES = [
    "banking",
    "company_holidays",
    "company_legal_entities",
    "company_locations",
    "contracts",
    "custom_fields",
    "documents",
    "employees",
    "employee_updates",
    "expenses",
    "finance",
    "job_catalog",
    "marketplace",
    "payroll",
    "payroll_supplements",
    "performance",
    "posts",
    "project_management_expenses",
    "project_management_projects",
    "project_management_time",
    "recruitment",
    "shift_management",
    "tasks",
    "time_off",
    "time_tracking",
    "trainings"
]

def gerar_url_autorizacao():
    """Gera URL de autorização OAuth2"""
    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': ' '.join(SCOPES),
        'resource_owner_type': 'company'  # Para obter token da empresa
    }
    
    url = f"{AUTHORIZATION_URL}?{urlencode(params)}"
    return url

def obter_token_com_code(authorization_code):
    """Troca o authorization code por um access token"""
    data = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': authorization_code,
        'redirect_uri': REDIRECT_URI
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    try:
        response = requests.post(TOKEN_URL, data=data, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro ao obter token: {response.status_code}")
            print(f"Resposta: {response.text}")
            return None
    except Exception as e:
        print(f"Exceção ao obter token: {e}")
        return None

def main():
    print("=" * 80)
    print("OBTER TOKEN OAUTH2 - FACTORIAL")
    print("=" * 80)
    
    print("\n[PASSO 1] Gerando URL de autorizacao...")
    auth_url = gerar_url_autorizacao()
    
    print(f"\nURL de autorizacao gerada:")
    print(f"{auth_url}")
    
    print("\n[PASSO 2] Abrindo navegador para autorizacao...")
    print("Apos autorizar, voce sera redirecionado para uma URL.")
    print("Copie a URL completa do redirecionamento (ela contem o codigo de autorizacao).")
    
    try:
        webbrowser.open(auth_url)
    except:
        print("Nao foi possivel abrir o navegador automaticamente.")
        print("Por favor, copie e cole a URL acima no seu navegador.")
    
    print("\n[PASSO 3] Cole a URL de redirecionamento aqui:")
    redirect_url = input("URL: ").strip()
    
    # Extrair o código da URL
    try:
        parsed = urlparse(redirect_url)
        params = parse_qs(parsed.query)
        
        if 'code' in params:
            authorization_code = params['code'][0]
            print(f"\n[OK] Codigo de autorizacao extraido: {authorization_code[:20]}...")
        else:
            print("\n[ERRO] Nao foi possivel encontrar o codigo de autorizacao na URL.")
            print("Certifique-se de copiar a URL completa do redirecionamento.")
            return
    except Exception as e:
        print(f"\n[ERRO] Erro ao processar URL: {e}")
        return
    
    print("\n[PASSO 4] Obtendo access token...")
    token_data = obter_token_com_code(authorization_code)
    
    if token_data:
        access_token = token_data.get('access_token')
        refresh_token = token_data.get('refresh_token')
        expires_in = token_data.get('expires_in')
        
        print("\n[OK] Token obtido com sucesso!")
        print(f"\nAccess Token (primeiros 50 chars): {access_token[:50]}...")
        print(f"Expira em: {expires_in} segundos ({expires_in/3600:.1f} horas)")
        
        print("\n" + "=" * 80)
        print("ATUALIZE O config_unificado.env COM:")
        print("=" * 80)
        print(f"API_KEY={access_token}")
        print(f"AUTH_TYPE=bearer")
        print("\n" + "=" * 80)
        
        # Testar o token
        print("\n[PASSO 5] Testando token...")
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        test_url = "https://api.eu2.demo.factorial.dev/companies/companies"
        response = requests.get(test_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and len(data['data']) > 0:
                company = data['data'][0]
                print(f"[OK] Token funcionando! Company ID: {company.get('company_id')}")
                print(f"Nome: {company.get('name')}")
        else:
            print(f"[AVISO] Teste retornou status {response.status_code}")
    else:
        print("\n[ERRO] Nao foi possivel obter o token.")

if __name__ == '__main__':
    main()
