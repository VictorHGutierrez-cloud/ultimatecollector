"""
Obter token OAuth2 usando redirect URI localhost
Para uso interno, podemos usar http://localhost como redirect URI
"""
import requests
import json
import sys
from urllib.parse import urlparse, parse_qs

# Credenciais OAuth2
CLIENT_ID = 'NyFzeb2fUEvPKehzOyUh-SGKNy27uUR-KqxW1rhA4l4'
BASE_URL = 'https://api.eu2.demo.factorial.dev'
REDIRECT_URI = 'http://localhost:8080/callback'  # Redirect URI localhost
AUTHORIZATION_CODE = '-CwopL3NnUktzWfWNHe1kD1ZMB37PBU7f77JSHXSse4'

print("=" * 60)
print("OBTER TOKEN OAUTH2 - COM LOCALHOST")
print("=" * 60)
print()
print("IMPORTANTE: Para uso interno, voce pode:")
print("1. Gerar API Key manualmente no frontend do Factorial")
print("2. Usar este script com CLIENT_SECRET")
print()
print("Dados:")
print(f"  Client ID: {CLIENT_ID}")
print(f"  Authorization Code: {AUTHORIZATION_CODE}")
print(f"  Redirect URI: {REDIRECT_URI}")
print()

# Tentar CLIENT_SECRET do config antigo (pode não funcionar)
CLIENT_SECRETS = [
    'w8FPABgXQy3RtRC1ngXFksR1nvXsV0SWnafL7-CUL8E',  # Do config antigo
]

if len(sys.argv) > 1:
    CLIENT_SECRETS.insert(0, sys.argv[1])
    print(f"Usando CLIENT_SECRET fornecido via argumento")
else:
    print("Testando com CLIENT_SECRETs conhecidos...")
    print("(Para usar outro, execute: python obter_token_localhost.py SEU_CLIENT_SECRET)")

print()
print("Tentando obter token...")
print()

token_url = f"{BASE_URL}/oauth/token"

for i, CLIENT_SECRET in enumerate(CLIENT_SECRETS, 1):
    print(f"Teste {i}: CLIENT_SECRET = {CLIENT_SECRET[:20]}...")
    print()
    
    # Tentar com JSON
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
                print(f"Resposta: {test_response.text[:200]}")
            
            print()
            print("=" * 60)
            print("ADICIONE AO config_unificado.env:")
            print("=" * 60)
            print()
            print(f"FACTORIAL_API_KEY={access_token}")
            print("FACTORIAL_AUTH_TYPE=bearer")
            print()
            
            with open('factorial_token.json', 'w', encoding='utf-8') as f:
                json.dump(token_data, f, indent=2, ensure_ascii=False)
            
            print("Token salvo em: factorial_token.json")
            exit(0)
            
        else:
            print(f"ERRO: Status {response.status_code}")
            print(f"Resposta: {response.text[:300]}")
            print()
            
            # Tentar com redirect URI diferente
            if REDIRECT_URI != 'urn:ietf:wg:oauth:2.0:oob':
                print("Tentando com redirect_uri = urn:ietf:wg:oauth:2.0:oob...")
                data2 = {
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "code": AUTHORIZATION_CODE,
                    "grant_type": "authorization_code",
                    "redirect_uri": "urn:ietf:wg:oauth:2.0:oob"
                }
                
                response2 = requests.post(
                    token_url,
                    json=data2,
                    headers={'Content-Type': 'application/json'},
                    timeout=10
                )
                
                if response2.status_code == 200:
                    token_data = response2.json()
                    access_token = token_data.get('access_token')
                    print("SUCESSO com urn:ietf:wg:oauth:2.0:oob!")
                    print(f"Access Token: {access_token}")
                    
                    with open('factorial_token.json', 'w', encoding='utf-8') as f:
                        json.dump(token_data, f, indent=2, ensure_ascii=False)
                    exit(0)
                else:
                    print(f"ERRO: {response2.text[:300]}")
            
    except Exception as e:
        print(f"ERRO: {str(e)}")
        import traceback
        traceback.print_exc()

print()
print("=" * 60)
print("NAO FOI POSSIVEL OBTER O TOKEN")
print("=" * 60)
print()
print("OPCOES:")
print()
print("1. ENCONTRAR O CLIENT_SECRET CORRETO")
print("   - Vá na pagina de configuracao da aplicacao")
print("   - Procure por 'Client Secret' ou 'Secret'")
print("   - Pode estar oculto (botao 'Show' ou 'Reveal')")
print()
print("2. GERAR API KEY MANUALMENTE (MAIS SIMPLES PARA USO INTERNO)")
print("   - Acesse o frontend do Factorial")
print("   - Vá em Settings > API")
print("   - Clique em 'Generate API Key'")
print("   - Copie a API Key gerada")
print("   - Use no config_unificado.env como:")
print("     API_KEY=sua_api_key_aqui")
print("     AUTH_TYPE=x-api-key")
print()
print("3. VERIFICAR SE O REDIRECT_URI ESTA CORRETO NA APLICACAO")
print("   - O redirect_uri usado aqui deve estar configurado")
print("   - na aplicacao OAuth2 no Factorial")
print("   - Pode ser: http://localhost, http://localhost:8080/callback,")
print("     ou urn:ietf:wg:oauth:2.0:oob")
