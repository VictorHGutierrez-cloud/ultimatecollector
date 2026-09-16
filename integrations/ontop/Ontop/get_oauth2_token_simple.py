"""
Script simplificado - apenas gera a URL de autorização OAuth2
Use este script se o outro não funcionar interativamente
"""
from pathlib import Path

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

# Credenciais OAuth2
CLIENT_ID = 'NyFzeb2fUEvPKehzOyUh-SGKNy27uUR-KqxW1rhA4l4'
BASE_URL = ENV_CONFIG.get('BASE_URL') or 'https://api.eu2.demo.factorial.dev'
REDIRECT_URI = 'https://app.eu2.demo.factorial.dev/'

# Scopes completos
SCOPES = [
    'banking', 'company_holidays', 'company_legal_entities', 'company_locations',
    'contracts', 'custom_fields', 'documents', 'employees', 'employee_updates',
    'expenses', 'finance', 'job_catalog', 'marketplace', 'payroll',
    'payroll_supplements', 'performance', 'posts', 'project_management_expenses',
    'project_management_projects', 'project_management_time', 'recruitment',
    'shift_management', 'tasks', 'time_off', 'time_tracking', 'trainings'
]

# Gerar URL
scope_string = '+'.join(SCOPES)
auth_url = (
    f"{BASE_URL}/oauth/authorize?"
    f"client_id={CLIENT_ID}&"
    f"redirect_uri={REDIRECT_URI}&"
    f"response_type=code&"
    f"scope={scope_string}"
)

print("=" * 60)
print("URL DE AUTORIZACAO OAUTH2 - FACTORIAL")
print("=" * 60)
print()
print("1. Copie a URL abaixo:")
print()
print(auth_url)
print()
print("2. Cole no navegador e faca login como ADMINISTRADOR")
print("3. Autorize as permissoes")
print("4. Copie o codigo da URL de redirecionamento")
print("5. Use o codigo no script get_oauth2_token.py")
print()
print("=" * 60)
