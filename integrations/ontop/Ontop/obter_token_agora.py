"""
Script direto para trocar código por token - sem interação
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
print("OBTENDO ACCESS TOKEN - FACTORIAL")
print("=" * 60)
print()
print(f"Client ID: {CLIENT_ID}")
print(f"Client Secret: {CLIENT_SECRET[:20]}...")
print(f"Authorization Code: {AUTHORIZATION_CODE[:20]}...")
print()

# Trocar código por token
token_url = f"{BASE_URL}/oauth/token"

data = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'code': AUTHORIZATION_CODE,
    'redirect_uri': REDIRECT_URI,
    'grant_type': 'authorization_code'
}

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

print("Fazendo requisicao...")
print(f"URL: {token_url}")
print()

try:
    response = requests.post(token_url, data=data, headers=headers, timeout=10)
    
    print(f"Status Code: {response.status_code}")
    print()
    
    if response.status_code == 200:
        token_data = response.json()
        
        access_token = token_data.get('access_token')
        refresh_token = token_data.get('refresh_token')
        expires_in = token_data.get('expires_in')
        token_type = token_data.get('token_type', 'Bearer')
        scope = token_data.get('scope', '')
        
        print("=" * 60)
        print("SUCESSO! TOKEN OBTIDO")
        print("=" * 60)
        print()
        print(f"Token Type: {token_type}")
        print(f"Expira em: {expires_in} segundos ({expires_in // 60} minutos)")
        print(f"Scopes: {scope[:100]}...")
        print()
        print(f"Access Token:")
        print(access_token)
        print()
        
        if refresh_token:
            print(f"Refresh Token:")
            print(refresh_token)
            print()
        
        # Testar o token
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
        print(f"Testando: {test_url}")
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
            print(f"Resposta: {test_response.text[:300]}")
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
        
        print("Depois disso, execute:")
        print("  python test_factorial_connection.py")
        print()
        
        # Salvar em arquivo
        token_info = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires_in': expires_in,
            'token_type': token_type,
            'scope': scope
        }
        
        with open('factorial_token_obtained.json', 'w', encoding='utf-8') as f:
            json.dump(token_info, f, indent=2, ensure_ascii=False)
        
        print("Token salvo em: factorial_token_obtained.json")
        
    else:
        print("=" * 60)
        print("ERRO ao obter token")
        print("=" * 60)
        print()
        print(f"Resposta: {response.text}")
        print()
        print("Possiveis causas:")
        print("1. Codigo de autorizacao ja foi usado (codigos sao de uso unico)")
        print("2. Codigo expirou (geralmente expira em poucos minutos)")
        print("3. CLIENT_SECRET incorreto")
        print("4. Redirect URI nao corresponde")
        print()
        print("SOLUCAO:")
        print("1. Gere um NOVO codigo de autorizacao")
        print("2. Execute: python get_oauth2_token_simple.py")
        print("3. Use o novo codigo neste script")
        
except Exception as e:
    print(f"ERRO: {str(e)}")
    import traceback
    traceback.print_exc()
