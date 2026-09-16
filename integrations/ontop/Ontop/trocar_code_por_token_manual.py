"""
Script para trocar código por token - versão que permite inserir CLIENT_SECRET manualmente
"""
import requests
import json

# Credenciais OAuth2
CLIENT_ID = 'NyFzeb2fUEvPKehzOyUh-SGKNy27uUR-KqxW1rhA4l4'
BASE_URL = 'https://api.eu2.demo.factorial.dev'
REDIRECT_URI = 'https://app.eu2.demo.factorial.dev/'

# Código de autorização
AUTHORIZATION_CODE = 'Iya83zlVbh6csZmlHi6W4XObfs0SdYd6yk5rqivfxsk'

print("=" * 60)
print("TROCAR CODIGO POR TOKEN - FACTORIAL")
print("=" * 60)
print()
print("Client ID: " + CLIENT_ID)
print("Authorization Code: " + AUTHORIZATION_CODE)
print()
print("PRECISO DO CLIENT_SECRET!")
print()
print("O CLIENT_SECRET esta na mesma pagina onde voce viu o CLIENT_ID.")
print("Procure por:")
print("  - Campo 'Client Secret' ou 'Secret'")
print("  - Botao 'Show Secret' ou 'Reveal'")
print("  - Secao 'Credentials' ou 'Authentication'")
print()
print("Se nao encontrar, pode precisar gerar um novo secret.")
print()

CLIENT_SECRET = input("Cole o CLIENT_SECRET aqui: ").strip()

if not CLIENT_SECRET:
    print("ERRO: CLIENT_SECRET nao fornecido")
    exit(1)

print()
print("=" * 60)
print("OBTENDO TOKEN...")
print("=" * 60)
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
        
        print("=" * 60)
        print("ADICIONE AO config_unificado.env:")
        print("=" * 60)
        print()
        print(f"API_KEY={access_token}")
        print("AUTH_TYPE=bearer")
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
            print("SUCESSO! Token funciona!")
        else:
            print(f"AVISO: Status {test_response.status_code}")
        
    else:
        print("ERRO ao obter token")
        print(f"Resposta: {response.text}")
        
except Exception as e:
    print(f"ERRO: {str(e)}")
