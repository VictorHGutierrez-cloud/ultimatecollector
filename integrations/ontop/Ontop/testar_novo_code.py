"""
Testar com novo código e redirect_uri correto
"""
import requests
import json

# Credenciais OAuth2
CLIENT_ID = 'NyFzeb2fUEvPKehzOyUh-SGKNy27uUR-KqxW1rhA4l4'
BASE_URL = 'https://api.eu2.demo.factorial.dev'
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'  # Redirect URI correto!

# NOVO código de autorização
AUTHORIZATION_CODE = '-CwopL3NnUktzWfWNHe1kD1ZMB37PBU7f77JSHXSse4'

# CLIENT_SECRETs para testar (o que você tinha antes)
CLIENT_SECRETS = [
    'ZGzrs5ADw0S349CPD7MRLmhCykijTOLBS2x9ptRwuvA',
]

print("=" * 60)
print("TESTANDO COM NOVO CODIGO E REDIRECT_URI CORRETO")
print("=" * 60)
print()
print(f"Client ID: {CLIENT_ID}")
print(f"Authorization Code: {AUTHORIZATION_CODE}")
print(f"Redirect URI: {REDIRECT_URI}")
print()

token_url = f"{BASE_URL}/oauth/token"

for i, CLIENT_SECRET in enumerate(CLIENT_SECRETS, 1):
    print(f"Teste {i}: CLIENT_SECRET = {CLIENT_SECRET[:20]}...")
    print()
    
    # Teste com JSON
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
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('access_token')
            refresh_token = token_data.get('refresh_token')
            expires_in = token_data.get('expires_in')
            
            print()
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
            
            # Testar token
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
                print(f"SUCESSO! Token funciona! Total: {total}")
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
            exit(0)
            
        else:
            print(f"ERRO: {response.text[:300]}")
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
                exit(0)
            else:
                print(f"ERRO: {response2.text[:300]}")
                
    except Exception as e:
        print(f"ERRO: {str(e)}")

print()
print("=" * 60)
print("IMPORTANTE: PRECISA DO CLIENT_SECRET")
print("=" * 60)
print()
print("SIM, voce PRECISA do CLIENT_SECRET para obter o token!")
print()
print("O CLIENT_SECRET e obrigatorio no fluxo OAuth2.")
print("Ele deve estar na pagina de configuracao da aplicacao.")
print()
print("Procure na pagina 'Edit application' por:")
print("  - Campo 'Client Secret'")
print("  - Botao 'Show Secret' ou 'Reveal'")
print("  - Secao 'Credentials'")
print()
print("Quando encontrar, execute:")
print("  python obter_token_interativo.py")
print()
print("Ou me envie o CLIENT_SECRET e eu obtenho o token para voce!")
