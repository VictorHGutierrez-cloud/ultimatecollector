"""
Script para obter token OAuth2 da Factorial usando Authorization Code Flow
Baseado no processo que funcionou anteriormente
"""
import requests
import webbrowser
from pathlib import Path
import os

def load_env_config():
    """Carrega configurações do arquivo .env"""
    config = {}
    env_files = [
        Path('config_unificado.env'),
        Path('../config_unificado.env'),
        Path('../../config_unificado.env')
    ]
    
    for file_path in env_files:
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
            break
    return config

ENV_CONFIG = load_env_config()

# Credenciais OAuth2 - NOVO CLIENT_ID
CLIENT_ID = 'NyFzeb2fUEvPKehzOyUh-SGKNy27uUR-KqxW1rhA4l4'
# CLIENT_SECRET precisa ser fornecido (não está no .env por segurança)
CLIENT_SECRET = ENV_CONFIG.get('CLIENT_SECRET') or os.getenv('CLIENT_SECRET')
BASE_URL = ENV_CONFIG.get('BASE_URL') or 'https://api.eu2.demo.factorial.dev'
REDIRECT_URI = 'https://app.eu2.demo.factorial.dev/'

# Scopes completos
SCOPES = [
    'banking',
    'company_holidays',
    'company_legal_entities',
    'company_locations',
    'contracts',
    'custom_fields',
    'documents',
    'employees',
    'employee_updates',
    'expenses',
    'finance',
    'job_catalog',
    'marketplace',
    'payroll',
    'payroll_supplements',
    'performance',
    'posts',
    'project_management_expenses',
    'project_management_projects',
    'project_management_time',
    'recruitment',
    'shift_management',
    'tasks',
    'time_off',
    'time_tracking',
    'trainings'
]

def generate_authorization_url():
    """Gera a URL de autorização OAuth2"""
    scope_string = '+'.join(SCOPES)
    
    auth_url = (
        f"{BASE_URL}/oauth/authorize?"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"response_type=code&"
        f"scope={scope_string}"
    )
    
    return auth_url

def exchange_code_for_token(authorization_code):
    """Troca o código de autorização por um access token"""
    token_url = f"{BASE_URL}/oauth/token"
    
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': authorization_code,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    try:
        print(f"\nTrocando codigo por token...")
        print(f"URL: {token_url}")
        
        response = requests.post(token_url, data=data, headers=headers, timeout=10)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            return token_data
        else:
            print(f"ERRO: {response.text}")
            return None
            
    except Exception as e:
        print(f"ERRO ao obter token: {str(e)}")
        return None

def test_token(access_token):
    """Testa se o token funciona"""
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    # Testar endpoint de employees
    test_url = f"{BASE_URL}/api/2026-07-01/resources/employees/employees"
    
    try:
        print(f"\nTestando token...")
        print(f"URL: {test_url}")
        
        response = requests.get(test_url, headers=headers, params={'limit': 1}, timeout=10)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            total = data.get('meta', {}).get('total', 0)
            print(f"SUCESSO! Token funciona!")
            print(f"Total de funcionarios: {total}")
            return True
        else:
            print(f"ERRO: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"ERRO ao testar token: {str(e)}")
        return False

def main():
    """Função principal"""
    import sys
    
    print("=" * 60)
    print("OBTER TOKEN OAUTH2 - FACTORIAL")
    print("=" * 60)
    print()
    
    # Verificar se código foi passado como argumento
    authorization_code = None
    if len(sys.argv) > 1 and sys.argv[1] == '--code':
        if len(sys.argv) > 2:
            authorization_code = sys.argv[2]
        else:
            print("ERRO: Use --code SEU_CODIGO")
            return
    
    # Variável global precisa ser atualizada
    global CLIENT_SECRET
    
    if not CLIENT_SECRET:
        print("AVISO: CLIENT_SECRET nao encontrado no .env")
        print("Digite o CLIENT_SECRET agora (ou configure no .env):")
        try:
            CLIENT_SECRET = input("CLIENT_SECRET: ").strip()
            if not CLIENT_SECRET:
                print("ERRO: CLIENT_SECRET e obrigatorio")
                return
        except (EOFError, KeyboardInterrupt):
            print("\nERRO: CLIENT_SECRET nao fornecido")
            print("\nConfigure no config_unificado.env:")
            print("CLIENT_SECRET=seu_client_secret_aqui")
            return
    
    # Passo 1: Gerar URL de autorização
    print("PASSO 1: Gerando URL de autorizacao...")
    auth_url = generate_authorization_url()
    
    print("\n" + "=" * 60)
    print("URL DE AUTORIZACAO:")
    print("=" * 60)
    print(auth_url)
    print()
    
    # Tentar abrir no navegador
    try:
        print("Abrindo URL no navegador...")
        webbrowser.open(auth_url)
        print("URL aberta no navegador!")
    except:
        print("Nao foi possivel abrir o navegador automaticamente.")
        print("Copie a URL acima e abra manualmente no navegador.")
    
    print()
    print("=" * 60)
    print("INSTRUCOES:")
    print("=" * 60)
    print("1. Faca login como ADMINISTRADOR na Factorial")
    print("2. Autorize as permissoes da aplicacao")
    print("3. Voce sera redirecionado para uma URL como:")
    print("   https://app.eu2.demo.factorial.dev/?code=XXXXX")
    print("4. Copie o codigo da URL (parte depois de 'code=')")
    print()
    
    # Passo 2: Obter código do usuário (se não foi passado como argumento)
    if not authorization_code:
        print()
        print("Aguardando codigo de autorizacao...")
        print("(Pressione Ctrl+C se quiser cancelar)")
        print()
        
        try:
            authorization_code = input("Cole o codigo de autorizacao aqui: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nOperacao cancelada.")
            print("\nPara usar o codigo depois, execute:")
            print(f"python get_oauth2_token.py --code SEU_CODIGO_AQUI")
            return
        
        if not authorization_code:
            print("ERRO: Codigo nao fornecido")
            return
    
    # Passo 3: Trocar código por token
    print()
    print("=" * 60)
    print("PASSO 2: Obtendo access token...")
    print("=" * 60)
    
    token_data = exchange_code_for_token(authorization_code)
    
    if not token_data:
        print("ERRO: Nao foi possivel obter o token")
        return
    
    access_token = token_data.get('access_token')
    refresh_token = token_data.get('refresh_token')
    expires_in = token_data.get('expires_in')
    token_type = token_data.get('token_type', 'Bearer')
    
    print()
    print("=" * 60)
    print("TOKEN OBTIDO COM SUCESSO!")
    print("=" * 60)
    print(f"Token Type: {token_type}")
    print(f"Expira em: {expires_in} segundos ({expires_in // 60} minutos)")
    print(f"Access Token: {access_token[:50]}...")
    if refresh_token:
        print(f"Refresh Token: {refresh_token[:50]}...")
    print()
    
    # Passo 4: Testar token
    print("=" * 60)
    print("PASSO 3: Testando token...")
    print("=" * 60)
    
    if test_token(access_token):
        print()
        print("=" * 60)
        print("CONFIGURACAO PARA O ARQUIVO .env")
        print("=" * 60)
        print()
        print("Adicione estas linhas ao seu config_unificado.env:")
        print()
        print(f"API_KEY={access_token}")
        print("AUTH_TYPE=bearer")
        print()
        
        if refresh_token:
            print(f"REFRESH_TOKEN={refresh_token}")
            print()
        
        print("Depois disso, os scripts devem funcionar!")
    else:
        print("AVISO: Token obtido mas teste falhou. Verifique as permissoes.")

if __name__ == '__main__':
    main()
