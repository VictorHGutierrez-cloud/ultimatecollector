"""
Script interativo para obter token - permite inserir CLIENT_SECRET
"""
import requests
import json

# Credenciais OAuth2
CLIENT_ID = 'NyFzeb2fUEvPKehzOyUh-SGKNy27uUR-KqxW1rhA4l4'
BASE_URL = 'https://api.eu2.demo.factorial.dev'
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

# NOVO código de autorização
AUTHORIZATION_CODE = '-CwopL3NnUktzWfWNHe1kD1ZMB37PBU7f77JSHXSse4'

print("=" * 60)
print("OBTER TOKEN OAUTH2 - FACTORIAL")
print("=" * 60)
print()
print("Dados que temos:")
print(f"  Client ID: {CLIENT_ID}")
print(f"  Authorization Code: {AUTHORIZATION_CODE}")
print()
print("FALTA: CLIENT_SECRET")
print()
print("O CLIENT_SECRET esta na pagina de configuracao")
print("da aplicacao 'Coletor RH 1'.")
print()
print("Procure na mesma pagina onde voce viu o Client ID:")
print("  - Campo 'Client Secret' ou 'Secret'")
print("  - Botao 'Show Secret' ou 'Reveal' (pode estar oculto)")
print("  - Secao 'Credentials' ou 'Authentication'")
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

# Tentar com JSON primeiro
print("Tentando com JSON...")
data_json = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "code": AUTHORIZATION_CODE,
    "grant_type": "authorization_code",
    "redirect_uri": REDIRECT_URI
}

try:
    response = requests.post(
        token_url,
        json=data_json,
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
        
        print(f"Expira em: {expires_in} segundos ({expires_in // 60} minutos)")
        print()
        
        # Testar
        print("Testando token...")
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
        
        print()
        print("=" * 60)
        print("ADICIONE AO config_unificado.env:")
        print("=" * 60)
        print()
        print(f"API_KEY={access_token}")
        print("AUTH_TYPE=bearer")
        print()
        
        # Salvar
        with open('factorial_token_obtained.json', 'w', encoding='utf-8') as f:
            json.dump(token_data, f, indent=2, ensure_ascii=False)
        
        print("Token salvo em: factorial_token_obtained.json")
        
    else:
        print(f"ERRO com JSON: {response.status_code}")
        print(f"Resposta: {response.text[:200]}")
        print()
        print("Tentando com form-urlencoded...")
        
        # Tentar form-urlencoded
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
        else:
            print(f"ERRO: {response2.status_code}")
            print(f"Resposta: {response2.text[:200]}")
            print()
            print("O CLIENT_SECRET pode estar incorreto ou o codigo expirou.")
            
except Exception as e:
    print(f"ERRO: {str(e)}")
    import traceback
    traceback.print_exc()
