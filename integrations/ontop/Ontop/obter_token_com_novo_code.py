"""
Script para trocar um NOVO código de autorização por token
Execute este script DEPOIS de obter um novo código
"""
import requests
import json

# Credenciais OAuth2
CLIENT_ID = 'NyFzeb2fUEvPKehzOyUh-SGKNy27uUR-KqxW1rhA4l4'
CLIENT_SECRET = 'ZGzrs5ADw0S349CPD7MRLmhCykijTOLBS2x9ptRwuvA'
BASE_URL = 'https://api.eu2.demo.factorial.dev'
REDIRECT_URI = 'https://app.eu2.demo.factorial.dev/'

print("=" * 60)
print("OBTER TOKEN COM NOVO CODIGO")
print("=" * 60)
print()
print("IMPORTANTE: Use um CODIGO NOVO (codigos sao de uso unico)")
print()
print("1. Execute: python get_oauth2_token_simple.py")
print("2. Copie a URL e cole no navegador")
print("3. Faca login e autorize")
print("4. Copie o NOVO codigo da URL")
print("5. Cole aqui quando solicitado")
print()
print("=" * 60)
print()

# Obter novo código do usuário
print("Cole o NOVO codigo de autorizacao aqui:")
AUTHORIZATION_CODE = input("Codigo: ").strip()

if not AUTHORIZATION_CODE:
    print("ERRO: Codigo nao fornecido")
    exit(1)

# Limpar código
AUTHORIZATION_CODE = AUTHORIZATION_CODE.replace(' ', '').replace('\n', '').replace('\r', '')

print()
print(f"Codigo recebido: {AUTHORIZATION_CODE[:20]}...")
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

print("Obtendo token...")
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
        
        print("=" * 60)
        print("SUCESSO! TOKEN OBTIDO")
        print("=" * 60)
        print()
        print(f"Access Token:")
        print(access_token)
        print()
        
        if refresh_token:
            print(f"Refresh Token:")
            print(refresh_token)
            print()
        
        # Testar
        print("Testando token...")
        test_headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        test_url = f"{BASE_URL}/api/2026-07-01/resources/employees/employees"
        test_response = requests.get(test_url, headers=test_headers, params={'limit': 1}, timeout=10)
        
        if test_response.status_code == 200:
            test_data = test_response.json()
            total = test_data.get('meta', {}).get('total', 0)
            print(f"SUCESSO! Token funciona! Total de funcionarios: {total}")
        else:
            print(f"AVISO: Status {test_response.status_code}")
        
        print()
        print("=" * 60)
        print("ADICIONE AO config_unificado.env:")
        print("=" * 60)
        print()
        print(f"API_KEY={access_token}")
        print("AUTH_TYPE=bearer")
        print()
        
    else:
        print("ERRO ao obter token")
        print(f"Resposta: {response.text}")
        
except Exception as e:
    print(f"ERRO: {str(e)}")
