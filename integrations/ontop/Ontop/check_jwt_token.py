"""
Script para verificar informações do JWT token
"""
import base64
import json
from pathlib import Path
from datetime import datetime

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

def decode_jwt(token):
    """Decodifica JWT sem verificar assinatura (apenas para inspeção)"""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None, "Token nao e um JWT valido (deve ter 3 partes)"
        
        # Decodificar header
        header_data = parts[0] + '=='
        header = base64.urlsafe_b64decode(header_data)
        header_json = json.loads(header)
        
        # Decodificar payload
        payload_data = parts[1] + '=='
        payload = base64.urlsafe_b64decode(payload_data)
        payload_json = json.loads(payload)
        
        return header_json, payload_json
    except Exception as e:
        return None, str(e)

ENV_CONFIG = load_env_config()
API_KEY = ENV_CONFIG.get('API_KEY')

print("=" * 60)
print("VERIFICACAO DO JWT TOKEN")
print("=" * 60)
print()

if not API_KEY:
    print("ERRO: API_KEY nao encontrada")
elif not API_KEY.startswith('eyJ'):
    print(f"AVISO: API_KEY nao parece ser um JWT (nao comeca com 'eyJ')")
    print(f"Primeiros caracteres: {API_KEY[:20]}...")
else:
    print(f"Token encontrado (primeiros 50 chars): {API_KEY[:50]}...")
    print()
    
    header, payload = decode_jwt(API_KEY)
    
    if isinstance(payload, dict):
        print("PAYLOAD DO TOKEN:")
        print("-" * 60)
        for key, value in payload.items():
            if key == 'exp':
                exp_timestamp = value
                exp_date = datetime.fromtimestamp(exp_timestamp)
                now = datetime.now()
                is_expired = exp_date < now
                status = "EXPIRADO" if is_expired else "VALIDO"
                print(f"{key}: {value} ({exp_date.strftime('%Y-%m-%d %H:%M:%S')}) - {status}")
            elif key == 'iat':
                iat_timestamp = value
                iat_date = datetime.fromtimestamp(iat_timestamp)
                print(f"{key}: {value} ({iat_date.strftime('%Y-%m-%d %H:%M:%S')})")
            else:
                print(f"{key}: {value}")
        
        print()
        print("HEADER DO TOKEN:")
        print("-" * 60)
        if isinstance(header, dict):
            for key, value in header.items():
                print(f"{key}: {value}")
        else:
            print(header)
    else:
        print(f"ERRO ao decodificar: {payload}")

print()
print("=" * 60)
print("CONCLUSOES:")
print("=" * 60)
print("1. Se o token esta EXPIRADO, voce precisa obter um novo token")
print("2. Se o token esta VALIDO mas ainda da erro 401, pode ser:")
print("   - Token nao tem as permissoes necessarias")
print("   - Token e para outro ambiente (prod vs demo)")
print("   - Precisa usar OAuth2 flow completo")
