"""
Script definitivo para obter token - testa todas as possibilidades
"""
import requests
import json

# Credenciais OAuth2
CLIENT_ID = 'NyFzeb2fUEvPKehzOyUh-SGKNy27uUR-KqxW1rhA4l4'
BASE_URL = 'https://api.eu2.demo.factorial.dev'
REDIRECT_URI = 'https://app.eu2.demo.factorial.dev/'

# NOVO código de autorização
AUTHORIZATION_CODE = '_VHApnKN7M_MumxA3dYks4ooObEcqOlLnXGoKzzBSEM'

# Possíveis CLIENT_SECRETs para testar
CLIENT_SECRETS_TO_TEST = [
    'ZGzrs5ADw0S349CPD7MRLmhCykijTOLBS2x9ptRwuvA',  # O que você chamou de "CODIGO AUTORIZAÇÃO"
    # Adicione outros aqui se tiver
]

print("=" * 60)
print("OBTER TOKEN - TESTE DEFINITIVO")
print("=" * 60)
print()
print("Client ID: " + CLIENT_ID)
print("Authorization Code: " + AUTHORIZATION_CODE)
print()
print("IMPORTANTE: O CLIENT_SECRET e DIFERENTE do codigo de autorizacao!")
print()
print("O CLIENT_SECRET deve estar na pagina de configuracao")
print("da aplicacao 'Coletor RH 1', em um campo separado.")
print()
print("Procure por:")
print("  - Campo 'Client Secret' ou 'Secret'")
print("  - Botao 'Show Secret' ou 'Reveal'")
print("  - Secao 'Credentials'")
print("  - Pode estar oculto (clique para revelar)")
print()

# Se não tiver CLIENT_SECRET, pedir
if not CLIENT_SECRETS_TO_TEST or len(CLIENT_SECRETS_TO_TEST) == 0:
    print("Digite o CLIENT_SECRET:")
    secret = input("CLIENT_SECRET: ").strip()
    if secret:
        CLIENT_SECRETS_TO_TEST = [secret]

token_url = f"{BASE_URL}/oauth/token"

# Testar cada CLIENT_SECRET
for i, CLIENT_SECRET in enumerate(CLIENT_SECRETS_TO_TEST, 1):
    print()
    print("=" * 60)
    print(f"TESTE {i}: CLIENT_SECRET = {CLIENT_SECRET[:20]}...")
    print("=" * 60)
    print()
    
    # Teste 1: JSON
    print("Tentativa 1: JSON")
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
            
            print("SUCESSO! Token obtido com JSON!")
            print()
            print(f"Access Token:")
            print(access_token)
            print()
            
            # Testar
            test_headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            test_url = f"{BASE_URL}/api/2026-07-01/resources/employees/employees"
            test_response = requests.get(test_url, headers=test_headers, params={'limit': 1}, timeout=10)
            
            if test_response.status_code == 200:
                test_data = test_response.json()
                total = test_data.get('meta', {}).get('total', 0)
                print(f"SUCESSO! Token funciona! Total: {total}")
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
                print(f"AVISO: Token obtido mas teste falhou: {test_response.status_code}")
        else:
            print(f"Falhou: {response.status_code} - {response.text[:200]}")
            
            # Teste 2: Form-urlencoded
            print()
            print("Tentativa 2: Form-urlencoded")
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
                print(f"Falhou: {response2.status_code} - {response2.text[:200]}")
                
    except Exception as e:
        print(f"ERRO: {str(e)}")

print()
print("=" * 60)
print("NENHUM CLIENT_SECRET FUNCIONOU")
print("=" * 60)
print()
print("Por favor, encontre o CLIENT_SECRET correto na pagina")
print("de configuracao da aplicacao e execute novamente.")
print()
print("Ou me envie o CLIENT_SECRET correto para eu testar.")
