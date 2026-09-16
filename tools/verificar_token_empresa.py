#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 VERIFICADOR DE TOKEN E EMPRESA
Mostra qual token e empresa estão sendo usados
"""

import base64
import json
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

def decode_jwt(token):
    """Decodifica um token JWT e retorna as informações"""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
        
        # Decodificar o payload (parte do meio)
        payload = parts[1]
        # Adicionar padding se necessário
        payload += '=' * (4 - len(payload) % 4)
        decoded = base64.urlsafe_b64decode(payload)
        payload_data = json.loads(decoded)
        
        return payload_data
    except Exception as e:
        print(f"❌ Erro ao decodificar token: {e}")
        return None

def main():
    # Configurar encoding UTF-8 para Windows
    import sys
    if sys.platform == 'win32':
        try:
            if hasattr(sys.stdout, "reconfigure"):
                sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    
    print("=" * 80)
    print("VERIFICADOR DE TOKEN E EMPRESA")
    print("=" * 80)
    
    # Carregar configurações
    project_root = Path(__file__).resolve().parents[1]
    for unified_path in (
        project_root / "config" / "unificado.env",
        project_root / "config_unificado.env",
    ):
        if unified_path.exists():
            load_dotenv(unified_path, override=True)
            print(f"\n[OK] Arquivo de configuracao encontrado: {unified_path}")
            break
    else:
        print("\n[AVISO] Nenhum arquivo de config encontrado!")
        return
    
    # Verificar token do config_unificado.env
    api_key = os.getenv('API_KEY', '')
    base_url = os.getenv('BASE_URL', '')
    auth_type = os.getenv('AUTH_TYPE', '')
    
    print(f"\nCONFIGURACAO ATUAL:")
    print(f"   BASE_URL: {base_url}")
    print(f"   AUTH_TYPE: {auth_type}")
    print(f"   API_KEY (primeiros 50 chars): {api_key[:50]}...")
    
    current_payload = None
    if api_key:
        current_payload = decode_jwt(api_key)
        if current_payload:
            print(f"\nINFORMACOES DO TOKEN ATUAL:")
            print(f"   Company ID: {current_payload.get('company_id', 'N/A')}")
            print(f"   Cell: {current_payload.get('cell', 'N/A')}")
            
            # Verificar expiração
            iat = current_payload.get('iat', 0)
            exp = current_payload.get('exp', 0)
            if iat:
                print(f"   Emitido em: {datetime.fromtimestamp(iat)}")
            if exp:
                exp_date = datetime.fromtimestamp(exp)
                print(f"   Expira em: {exp_date}")
                current = datetime.now()
                if exp_date < current:
                    print(f"   [AVISO] TOKEN EXPIRADO! (expirou ha {current - exp_date})")
                else:
                    print(f"   [OK] Token valido (valido por mais {exp_date - current})")
    
    # Verificar outros tokens disponíveis
    print(f"\n" + "=" * 80)
    print("OUTROS TOKENS ENCONTRADOS:")
    print("=" * 80)
    
    # Token do apitenantpresales.txt
    presales_path = project_root / 'apitenantpresales.txt'
    presales_token = None
    if presales_path.exists():
        content = presales_path.read_text(encoding='utf-8')
        if 'chave:' in content:
            token_line = [l for l in content.split('\n') if 'chave:' in l.lower()][0]
            presales_token = token_line.split('chave:')[1].strip()
            payload = decode_jwt(presales_token)
            if payload:
                print(f"\n[ARQUIVO] apitenantpresales.txt:")
                print(f"   Company ID: {payload.get('company_id', 'N/A')}")
                print(f"   Nome: cursor (Tenant Case Pre Sales)")
                if payload.get('company_id') == 27275:
                    print(f"   [OK] Este e o token que esta sendo usado nos dados coletados!")
    
    # Token do chaveapiibero.txt
    ibero_path = project_root / 'chaveapiibero.txt'
    ibero_token = None
    if ibero_path.exists():
        ibero_token = ibero_path.read_text(encoding='utf-8').strip()
        payload = decode_jwt(ibero_token)
        if payload:
            print(f"\n[ARQUIVO] chaveapiibero.txt:")
            print(f"   Company ID: {payload.get('company_id', 'N/A')}")
            print(f"   Nome: Ibero")
    
    # Verificar dados coletados
    print(f"\n" + "=" * 80)
    print("DADOS COLETADOS RECENTEMENTE:")
    print("=" * 80)
    
    employees_path = project_root / 'data' / 'raw' / 'employees'
    if employees_path.exists():
        json_files = list(employees_path.glob('*.json'))
        if json_files:
            latest = max(json_files, key=lambda p: p.stat().st_mtime)
            print(f"\n[ARQUIVO] Arquivo mais recente: {latest.name}")
            try:
                data = json.loads(latest.read_text(encoding='utf-8'))
                if isinstance(data, list) and len(data) > 0:
                    first_employee = data[0]
                    company_id = first_employee.get('company_id')
                    print(f"   Company ID nos dados: {company_id}")
                    
                    # Comparar com token atual
                    current_company_id = current_payload.get('company_id') if current_payload else None
                    if current_company_id and current_company_id != company_id:
                        print(f"\n[ATENCAO] INCONSISTENCIA DETECTADA!")
                        print(f"   Token configurado aponta para Company ID: {current_company_id}")
                        print(f"   Dados coletados sao da Company ID: {company_id}")
                        print(f"   [ERRO] Voce pode estar usando o token errado!")
                        
                        # Sugerir qual token usar
                        if company_id == 27275 and presales_token:
                            print(f"\n[RECOMENDACAO]:")
                            print(f"   Use o token do arquivo 'apitenantpresales.txt'")
                            print(f"   Atualize o API_KEY no config_unificado.env com:")
                            print(f"   {presales_token[:50]}...")
                    elif current_company_id == company_id:
                        print(f"   [OK] Token e dados estao consistentes!")
            except Exception as e:
                print(f"   [AVISO] Erro ao ler arquivo: {e}")
    
    print(f"\n" + "=" * 80)

if __name__ == '__main__':
    main()
