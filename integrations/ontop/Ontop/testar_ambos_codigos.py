"""
Testa ambos os códigos (USUARIO e COMPANY) para ver qual funciona
"""
import requests
import json

# Credenciais OAuth2
CLIENT_ID = 'NyFzeb2fUEvPKehzOyUh-SGKNy27uUR-KqxW1rhA4l4'
# O que você chamou de "USUARIO" - pode ser CLIENT_SECRET ou código
CLIENT_SECRET_CANDIDATO_1 = 'ZGzrs5ADw0S349CPD7MRLmhCykijTOLBS2x9ptRwuvA'
# Código COMPANY
CODE_COMPANY = 'JLg1v36G13SNUP7GFWF27tA8aEePdTcepc2nO31H_sk'
# Código USUARIO (se for código)
CODE_USUARIO = 'ZGzrs5ADw0S349CPD7MRLmhCykijTOLBS2x9ptRwuvA'

BASE_URL = 'https://api.eu2.demo.factorial.dev'
REDIRECT_URI = 'https://app.eu2.demo.factorial.dev/'

print("=" * 60)
print("TESTANDO AMBOS OS CODIGOS")
print("=" * 60)
print()

# Teste 1: CODE_COMPANY com CLIENT_SECRET_CANDIDATO_1
print("TESTE 1: CODE_COMPANY com CLIENT_SECRET candidato")
print("-" * 60)
token_url = f"{BASE_URL}/oauth/token"

data1 = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET_CANDIDATO_1,
    'code': CODE_COMPANY,
    'redirect_uri': REDIRECT_URI,
    'grant_type': 'authorization_code'
}

try:
    response1 = requests.post(token_url, data=data1, headers={'Content-Type': 'application/x-www-form-urlencoded'}, timeout=10)
    print(f"Status: {response1.status_code}")
    if response1.status_code == 200:
        print("SUCESSO! Token obtido!")
        token_data = response1.json()
        print(f"Access Token: {token_data.get('access_token', '')[:50]}...")
    else:
        print(f"ERRO: {response1.text[:200]}")
except Exception as e:
    print(f"ERRO: {str(e)}")

print()

# Teste 2: CODE_USUARIO com CLIENT_SECRET_CANDIDATO_1
print("TESTE 2: CODE_USUARIO com CLIENT_SECRET candidato")
print("-" * 60)
data2 = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET_CANDIDATO_1,
    'code': CODE_USUARIO,
    'redirect_uri': REDIRECT_URI,
    'grant_type': 'authorization_code'
}

try:
    response2 = requests.post(token_url, data=data2, headers={'Content-Type': 'application/x-www-form-urlencoded'}, timeout=10)
    print(f"Status: {response2.status_code}")
    if response2.status_code == 200:
        print("SUCESSO! Token obtido!")
        token_data = response2.json()
        print(f"Access Token: {token_data.get('access_token', '')[:50]}...")
    else:
        print(f"ERRO: {response2.text[:200]}")
except Exception as e:
    print(f"ERRO: {str(e)}")

print()
print("=" * 60)
print("IMPORTANTE:")
print("=" * 60)
print("Se ambos falharem, o CLIENT_SECRET pode estar incorreto.")
print("O CLIENT_SECRET deve estar em um campo separado na pagina")
print("da aplicacao, nao nos codigos de autorizacao.")
print()
print("Procure por:")
print("- Campo 'Client Secret'")
print("- Botao 'Show Secret' ou 'Reveal'")
print("- Secao 'Credentials'")
