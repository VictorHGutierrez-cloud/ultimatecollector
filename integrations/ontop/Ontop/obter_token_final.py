"""
Obter token OAuth2 com CLIENT_SECRET correto
"""
import requests
import json
import sys

# Credenciais OAuth2
CLIENT_ID = 'NyFzeb2fUEvPKehzOyUh-SGKNy27uUR-KqxW1rhA4l4'
BASE_URL = 'https://api.eu2.demo.factorial.dev'
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
AUTHORIZATION_CODE = '-CwopL3NnUktzWfWNHe1kD1ZMB37PBU7f77JSHXSse4'

print("=" * 60)
print("OBTER TOKEN OAUTH2 - FACTORIAL")
print("=" * 60)
print()

# Solicitar CLIENT_SECRET
if len(sys.argv) > 1:
    CLIENT_SECRET = sys.argv[1]
    print(f"Usando CLIENT_SECRET fornecido via argumento")
else:
    CLIENT_SECRET = input("Cole o CLIENT_SECRET aqui: ").strip()

if not CLIENT_SECRET:
    print("ERRO: CLIENT_SECRET nao pode estar vazio!")
    exit(1)

print()
print("Tentando obter token...")
print()

token_url = f"{BASE_URL}/oauth/token"

# Tentar com JSON primeiro
data = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "code": AUTHORIZATION_CODE,
    "grant_type": "authorization_code",
    "redirect_uri": REDIRECT_URI
}

try:
    response = requests.post(
        token_url,
        json=data,
        headers={'Content-Type': 'application/json'},
        timeout=10
    )
    
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
        
        if expires_in:
            print(f"Expira em: {expires_in} segundos ({expires_in // 3600} horas)")
            print()
        
        # Testar token
        print("Testando token com API...")
        test_headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        test_url = f"{BASE_URL}/api/2026-07-01/resources/employees/employees"
        test_response = requests.get(test_url, headers=test_headers, params={'limit': 1}, timeout=10)
        
        if test_response.status_code == 200:
            test_data = test_response.json()
            total = test_data.get('meta', {}).get('total', 0)
            print(f"SUCESSO! Token funciona! Total de funcionarios: {total}")
        else:
            print(f"AVISO: Status {test_response.status_code}")
            print(f"Resposta: {test_response.text[:200]}")
        
        print()
        print("=" * 60)
        print("ADICIONE AO config_unificado.env:")
        print("=" * 60)
        print()
        print(f"FACTORIAL_API_KEY={access_token}")
        print("FACTORIAL_AUTH_TYPE=bearer")
        print()
        
        # Salvar token
        with open('factorial_token.json', 'w', encoding='utf-8') as f:
            json.dump(token_data, f, indent=2, ensure_ascii=False)
        
        print("Token salvo em: factorial_token.json")
        print()
        print("=" * 60)
        
    else:
        print(f"ERRO: Status {response.status_code}")
        print(f"Resposta: {response.text}")
        print()
        
        # Tentar form-urlencoded
        print("Tentando com form-urlencoded...")
        data_form = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': AUTHORIZATION_CODE,
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI
        }
        
        response2 = requests.post(
            token_url,
            data=data_form,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=10
        )
        
        if response2.status_code == 200:
            token_data = response2.json()
            access_token = token_data.get('access_token')
            print("SUCESSO! Token obtido com form-urlencoded!")
            print(f"Access Token: {access_token}")
            
            with open('factorial_token.json', 'w', encoding='utf-8') as f:
                json.dump(token_data, f, indent=2, ensure_ascii=False)
        else:
            print(f"ERRO: Status {response2.status_code}")
            print(f"Resposta: {response2.text}")
            print()
            print("Verifique se o CLIENT_SECRET esta correto!")

except Exception as e:
    print(f"ERRO: {str(e)}")
    import traceback
    traceback.print_exc()