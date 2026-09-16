"""
Script para obter token quando você tiver o CLIENT_SECRET correto
"""
import requests
import json

# Credenciais OAuth2
CLIENT_ID = 'NyFzeb2fUEvPKehzOyUh-SGKNy27uUR-KqxW1rhA4l4'
BASE_URL = 'https://api.eu2.demo.factorial.dev'
REDIRECT_URI = 'https://app.eu2.demo.factorial.dev/'

# NOVO código de autorização
AUTHORIZATION_CODE = '_VHApnKN7M_MumxA3dYks4ooObEcqOlLnXGoKzzBSEM'

print("=" * 60)
print("OBTER TOKEN COM CLIENT_SECRET")
print("=" * 60)
print()
print("Client ID: " + CLIENT_ID)
print("Authorization Code: " + AUTHORIZATION_CODE)
print()
print("O CLIENT_SECRET deve estar na pagina de configuracao")
print("da aplicacao 'Coletor RH 1'.")
print()
print("Procure por:")
print("  - Campo 'Client Secret'")
print("  - Botao 'Show Secret' ou 'Reveal'")
print("  - Pode estar oculto (clique para mostrar)")
print()
print("O CLIENT_SECRET e DIFERENTE do codigo de autorizacao!")
print()

CLIENT_SECRET = input("Cole o CLIENT_SECRET aqui: ").strip()

if not CLIENT_SECRET:
    print("ERRO: CLIENT_SECRET nao fornecido")
    exit(1)

# Limpar espaços
CLIENT_SECRET = CLIENT_SECRET.replace(' ', '').replace('\n', '').replace('\r', '')

print()
print("Obtendo token...")
print()

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
    
    print(f"Status: {response.status_code}")
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
        
        print(f"Expira em: {expires_in} segundos ({expires_in // 60} minutos)")
        print()
        
        # Testar token
        print("Testando token...")
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
        
        print("Depois disso, execute:")
        print("  python test_factorial_connection.py")
        print()
        
        # Salvar
        token_info = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires_in': expires_in
        }
        
        with open('factorial_token_obtained.json', 'w', encoding='utf-8') as f:
            json.dump(token_info, f, indent=2, ensure_ascii=False)
        
        print("Token salvo em: factorial_token_obtained.json")
        
    else:
        print("ERRO ao obter token")
        print(f"Resposta: {response.text}")
        print()
        print("Possiveis causas:")
        print("1. CLIENT_SECRET incorreto")
        print("2. Codigo de autorizacao ja foi usado ou expirou")
        print("3. Redirect URI nao corresponde")
        
except Exception as e:
    print(f"ERRO: {str(e)}")
    import traceback
    traceback.print_exc()
