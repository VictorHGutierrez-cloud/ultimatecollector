"""
Script para obter token usando JSON (como na documentação)
"""
import requests
import json

# Credenciais OAuth2
CLIENT_ID = 'NyFzeb2fUEvPKehzOyUh-SGKNy27uUR-KqxW1rhA4l4'
CLIENT_SECRET = 'ZGzrs5ADw0S349CPD7MRLmhCykijTOLBS2x9ptRwuvA'
BASE_URL = 'https://api.eu2.demo.factorial.dev'
REDIRECT_URI = 'https://app.eu2.demo.factorial.dev/'

# NOVO código de autorização
AUTHORIZATION_CODE = '_VHApnKN7M_MumxA3dYks4ooObEcqOlLnXGoKzzBSEM'

print("=" * 60)
print("OBTENDO TOKEN COM JSON (como na documentacao)")
print("=" * 60)
print()
print(f"Client ID: {CLIENT_ID}")
print(f"Authorization Code: {AUTHORIZATION_CODE[:20]}...")
print()

token_url = f"{BASE_URL}/oauth/token"

# Tentar primeiro com JSON (como na documentação)
print("Tentativa 1: Usando JSON (Content-Type: application/json)")
print("-" * 60)

data_json = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "code": AUTHORIZATION_CODE,
    "grant_type": "authorization_code",
    "redirect_uri": REDIRECT_URI
}

headers_json = {
    'Content-Type': 'application/json'
}

try:
    response = requests.post(token_url, json=data_json, headers=headers_json, timeout=10)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get('access_token')
        refresh_token = token_data.get('refresh_token')
        expires_in = token_data.get('expires_in')
        token_type = token_data.get('token_type', 'Bearer')
        
        print()
        print("=" * 60)
        print("SUCESSO! TOKEN OBTIDO COM JSON")
        print("=" * 60)
        print()
        print(f"Token Type: {token_type}")
        print(f"Expira em: {expires_in} segundos ({expires_in // 60} minutos)")
        print()
        print(f"Access Token:")
        print(access_token)
        print()
        
        if refresh_token:
            print(f"Refresh Token:")
            print(refresh_token)
            print()
        
        # Testar token
        print("=" * 60)
        print("TESTANDO TOKEN...")
        print("=" * 60)
        print()
        
        test_headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        test_url = f"{BASE_URL}/api/2026-07-01/resources/employees/employees"
        test_response = requests.get(test_url, headers=test_headers, params={'limit': 1}, timeout=10)
        
        print(f"Status: {test_response.status_code}")
        
        if test_response.status_code == 200:
            test_data = test_response.json()
            total = test_data.get('meta', {}).get('total', 0)
            print()
            print("=" * 60)
            print("SUCESSO! TOKEN FUNCIONA!")
            print("=" * 60)
            print(f"Total de funcionarios: {total}")
            print()
        else:
            print(f"AVISO: Token obtido mas teste retornou {test_response.status_code}")
            print(f"Resposta: {test_response.text[:200]}")
        
        print()
        print("=" * 60)
        print("CONFIGURACAO PARA config_unificado.env")
        print("=" * 60)
        print()
        print("Adicione ou atualize estas linhas:")
        print()
        print(f"API_KEY={access_token}")
        print("AUTH_TYPE=bearer")
        print()
        
        if refresh_token:
            print(f"REFRESH_TOKEN={refresh_token}")
            print()
        
        # Salvar token
        token_info = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires_in': expires_in,
            'token_type': token_type
        }
        
        with open('factorial_token_obtained.json', 'w', encoding='utf-8') as f:
            json.dump(token_info, f, indent=2, ensure_ascii=False)
        
        print("Token salvo em: factorial_token_obtained.json")
        
    else:
        print(f"ERRO: {response.text[:300]}")
        print()
        print("Tentando com form-urlencoded (formato alternativo)...")
        print("-" * 60)
        
        # Tentar com form-urlencoded como fallback
        data_form = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': AUTHORIZATION_CODE,
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI
        }
        
        headers_form = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        response2 = requests.post(token_url, data=data_form, headers=headers_form, timeout=10)
        print(f"Status: {response2.status_code}")
        
        if response2.status_code == 200:
            token_data = response2.json()
            access_token = token_data.get('access_token')
            print()
            print("SUCESSO! Token obtido com form-urlencoded")
            print(f"Access Token: {access_token}")
        else:
            print(f"ERRO: {response2.text[:300]}")
            print()
            print("Nenhum formato funcionou. Possiveis causas:")
            print("1. CLIENT_SECRET incorreto")
            print("2. Codigo de autorizacao expirado ou ja usado")
            print("3. Redirect URI nao corresponde")
        
except Exception as e:
    print(f"ERRO: {str(e)}")
    import traceback
    traceback.print_exc()
