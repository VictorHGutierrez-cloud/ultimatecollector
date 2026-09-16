#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔑 VERIFICADOR DE API KEY - Testa se a chave está funcionando
"""

import requests
import json
from datetime import datetime

def check_api_key():
    """Verifica se a API key está funcionando"""
    print("🔑 VERIFICANDO API KEY")
    print("=" * 40)
    
    # Sua API key atual
    api_key = "eyJraWQiOiJmYWN0b3JpYWwtaWQiLCJhbGciOiJFUzI1NiJ9.eyJpYXQiOjE3NTY5NDkwMzgsImV4cCI6MjA3MjUxODU1OCwianRpIjoiNDI5ZWI2NGEtOTY5Yy00ZTdhLThkYWMtZTJhMTI1ZWE4OTE4IiwiY2VsbCI6ImRlbW8tZ3djLWV1MiIsImNjbXBhbnlfaWQiOjk3NjF9.vnGqiLgmbXz86roQaFHJrzY3fEXSVVwrkzxc9D-77KRtMoxNq2kkSyVCIw-5eRxL3gX8SJLynEkSsPxTfHfpzA"
    
    # Decodificar o JWT para ver informações
    try:
        import base64
        
        # JWT tem 3 partes separadas por ponto
        parts = api_key.split('.')
        if len(parts) == 3:
            # Decodificar o payload (parte do meio)
            payload = parts[1]
            # Adicionar padding se necessário
            payload += '=' * (4 - len(payload) % 4)
            decoded = base64.b64decode(payload)
            payload_data = json.loads(decoded)
            
            print("📋 INFORMAÇÕES DA API KEY:")
            print(f"   🏢 Company ID: {payload_data.get('company_id', 'N/A')}")
            print(f"   📅 Emitido em: {datetime.fromtimestamp(payload_data.get('iat', 0))}")
            print(f"   ⏰ Expira em: {datetime.fromtimestamp(payload_data.get('exp', 0))}")
            print(f"   🏷️ Cell: {payload_data.get('cell', 'N/A')}")
            
            # Verificar se expirou
            exp_timestamp = payload_data.get('exp', 0)
            current_timestamp = datetime.now().timestamp()
            
            if exp_timestamp < current_timestamp:
                print("❌ API KEY EXPIRADA!")
                print(f"   Expirou em: {datetime.fromtimestamp(exp_timestamp)}")
                print(f"   Hoje é: {datetime.now()}")
            else:
                print("✅ API KEY VÁLIDA!")
                print(f"   Válida até: {datetime.fromtimestamp(exp_timestamp)}")
                
        else:
            print("❌ Formato de API key inválido!")
            
    except Exception as e:
        print(f"❌ Erro ao decodificar API key: {e}")
    
    # Testar diferentes URLs
    print(f"\n🌐 TESTANDO DIFERENTES URLs:")
    
    urls_to_test = [
        "https://api.eu2.demo.factorial.dev",
        "https://api.factorial.dev", 
        "https://api.eu.factorial.dev",
        "https://api.us.factorial.dev"
    ]
    
    for url in urls_to_test:
        print(f"\n🔍 Testando: {url}")
        try:
            headers = {
                'x-api-key': api_key,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            # Testar endpoint básico
            response = requests.get(f"{url}/api/2026-07-01", headers=headers, timeout=10)
            
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print(f"   ✅ FUNCIONA! Use esta URL: {url}")
                return url
            elif response.status_code == 401:
                print(f"   🔒 401 - Sem permissão")
            elif response.status_code == 404:
                print(f"   ❌ 404 - Não encontrado")
            else:
                print(f"   ⚠️ {response.status_code} - {response.reason}")
                
        except Exception as e:
            print(f"   ❌ Erro: {str(e)[:50]}...")
    
    return None

if __name__ == "__main__":
    working_url = check_api_key()
    
    if working_url:
        print(f"\n🎯 SOLUÇÃO ENCONTRADA!")
        print(f"   Use esta URL: {working_url}")
        print(f"   Atualize o arquivo de configuração com esta URL")
    else:
        print(f"\n❌ NENHUMA URL FUNCIONOU!")
        print(f"   Sua API key pode estar expirada ou inválida")
        print(f"   Entre em contato com o suporte da Factorial")
