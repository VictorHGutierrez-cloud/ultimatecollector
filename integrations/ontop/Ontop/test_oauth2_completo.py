"""
Teste completo OAuth2 - gera URL, obtém código e troca por token
"""
import requests
import webbrowser
from urllib.parse import urlparse, parse_qs

# Credenciais OAuth2
CLIENT_ID = 'NyFzeb2fUEvPKehzOyUh-SGKNy27uUR-KqxW1rhA4l4'
CLIENT_SECRET = 'ZGzrs5ADw0S349CPD7MRLmhCykijTOLBS2x9ptRwuvA'
BASE_URL = 'https://api.eu2.demo.factorial.dev'
REDIRECT_URI = 'https://app.eu2.demo.factorial.dev/'

# Scopes
SCOPES = [
    'banking', 'company_holidays', 'company_legal_entities', 'company_locations',
    'contracts', 'custom_fields', 'documents', 'employees', 'employee_updates',
    'expenses', 'finance', 'job_catalog', 'marketplace', 'payroll',
    'payroll_supplements', 'performance', 'posts', 'project_management_expenses',
    'project_management_projects', 'project_management_time', 'recruitment',
    'shift_management', 'tasks', 'time_off', 'time_tracking', 'trainings'
]

print("=" * 60)
print("TESTE COMPLETO OAUTH2 - FACTORIAL")
print("=" * 60)
print()

# Passo 1: Gerar URL
print("PASSO 1: Gerando URL de autorizacao...")
scope_string = '+'.join(SCOPES)
auth_url = (
    f"{BASE_URL}/oauth/authorize?"
    f"client_id={CLIENT_ID}&"
    f"redirect_uri={REDIRECT_URI}&"
    f"response_type=code&"
    f"scope={scope_string}"
)

print("\nURL DE AUTORIZACAO:")
print("=" * 60)
print(auth_url)
print()
print("Copie esta URL e cole no navegador")
print("OU pressione Enter para tentar abrir automaticamente...")
input()

try:
    webbrowser.open(auth_url)
    print("URL aberta no navegador!")
except:
    print("Nao foi possivel abrir automaticamente")

print()
print("=" * 60)
print("INSTRUCOES:")
print("=" * 60)
print("1. Faca login como ADMINISTRADOR")
print("2. Autorize as permissoes")
print("3. Voce sera redirecionado para uma URL como:")
print("   https://app.eu2.demo.factorial.dev/?code=XXXXX")
print("4. Copie o CODIGO COMPLETO da URL")
print()

# Passo 2: Obter código
code = input("Cole o NOVO codigo de autorizacao aqui: ").strip()

if not code:
    print("ERRO: Codigo nao fornecido")
    exit(1)

# Limpar código (remover espaços, quebras de linha, etc)
code = code.replace(' ', '').replace('\n', '').replace('\r', '')

print()
print(f"Codigo recebido: {code[:20]}...")
print()

# Passo 3: Trocar código por token
print("=" * 60)
print("PASSO 2: Trocando codigo por token...")
print("=" * 60)
print()

token_url = f"{BASE_URL}/oauth/token"

# Tentar diferentes formatos de dados
data_formats = [
    # Formato 1: application/x-www-form-urlencoded (padrão)
    {
        'data': {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code,
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'authorization_code'
        },
        'headers': {'Content-Type': 'application/x-www-form-urlencoded'}
    },
    # Formato 2: JSON (menos comum, mas vamos testar)
    {
        'json': {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code,
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'authorization_code'
        },
        'headers': {'Content-Type': 'application/json'}
    }
]

token_obtained = False

for i, format_config in enumerate(data_formats, 1):
    print(f"Tentativa {i}: {format_config['headers']['Content-Type']}")
    
    try:
        if 'data' in format_config:
            response = requests.post(
                token_url,
                data=format_config['data'],
                headers=format_config['headers'],
                timeout=10
            )
        else:
            response = requests.post(
                token_url,
                json=format_config['json'],
                headers=format_config['headers'],
                timeout=10
            )
        
        print(f"  Status: {response.status_code}")
        
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
            
            print(f"Expira em: {expires_in} segundos ({expires_in // 60} minutos)")
            print()
            
            # Testar token
            print("=" * 60)
            print("TESTANDO TOKEN...")
            print("=" * 60)
            print()
            
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
                print(f"SUCESSO! Token funciona!")
                print(f"Total de funcionarios: {total}")
            else:
                print(f"AVISO: Token obtido mas teste falhou")
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
            
            token_obtained = True
            break
        else:
            print(f"  ERRO: {response.text[:200]}")
            print()
            
    except Exception as e:
        print(f"  ERRO: {str(e)}")
        print()

if not token_obtained:
    print()
    print("=" * 60)
    print("ERRO: Nao foi possivel obter o token")
    print("=" * 60)
    print()
    print("Possiveis causas:")
    print("1. Codigo de autorizacao ja foi usado (codigos sao de uso unico)")
    print("2. Codigo expirou (geralmente expira em poucos minutos)")
    print("3. CLIENT_SECRET incorreto")
    print("4. Redirect URI nao corresponde exatamente")
    print()
    print("SOLUCAO: Gere um NOVO codigo de autorizacao e tente novamente")
