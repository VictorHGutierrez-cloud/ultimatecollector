#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 ENCONTRADOR DE URL CORRETA - Testa diferentes variações
"""

import requests
import json

def find_correct_url():
    """Encontra a URL correta da API Factorial"""
    print("🌐 PROCURANDO URL CORRETA DA API FACTORIAL")
    print("=" * 50)
    
    api_key = "eyJraWQiOiJmYWN0b3JpYWwtaWQiLCJhbGciOiJFUzI1NiJ9.eyJpYXQiOjE3NTY5NDkwMzgsImV4cCI6MjA3MjUxODU1OCwianRpIjoiNDI5ZWI2NGEtOTY5Yy00ZTdhLThkYWMtZTJhMTI1ZWE4OTE4IiwiY2VsbCI6ImRlbW8tZ3djLWV1MiIsImNjbXBhbnlfaWQiOjk3NjF9.vnGqiLgmbXz86roQaFHJrzY3fEXSVVwrkzxc9D-77KRtMoxNq2kkSyVCIw-5eRxL3gX8SJLynEkSsPxTfHfpzA"
    
    # URLs para testar
    urls_to_test = [
        # URLs base
        "https://api.factorialhr.com",
        "https://api.factorialhr.com/api",
        "https://api.factorialhr.com/api/v1",
        "https://api.factorialhr.com/api/2026-07-01",
        
        # URLs com subdomínios
        "https://api.eu.factorialhr.com",
        "https://api.us.factorialhr.com",
        "https://api.eu2.factorialhr.com",
        
        # URLs demo
        "https://demo.factorialhr.com/api",
        "https://demo.factorialhr.com/api/v1",
        "https://demo.factorialhr.com/api/2026-07-01",
        
        # URLs com factorial.dev
        "https://api.factorial.dev",
        "https://api.eu.factorial.dev",
        "https://api.us.factorial.dev",
        "https://api.eu2.factorial.dev",
        
        # URLs com factorial.com
        "https://api.factorial.com",
        "https://api.eu.factorial.com",
        "https://api.us.factorial.com",
        "https://api.eu2.factorial.com",
    ]
    
    headers = {
        'x-api-key': api_key,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    working_urls = []
    
    for url in urls_to_test:
        print(f"\n🔍 Testando: {url}")
        
        try:
            # Testar endpoint raiz
            response = requests.get(url, headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ FUNCIONA! (200 OK)")
                working_urls.append((url, "200 OK"))
                
                # Testar endpoint de recursos
                resources_url = f"{url}/resources/employees/employees"
                try:
                    res_response = requests.get(resources_url, headers=headers, timeout=10)
                    print(f"   📊 Recursos: {res_response.status_code}")
                    if res_response.status_code == 200:
                        print(f"   🎯 PERFEITO! Esta é a URL correta!")
                        return url
                except:
                    pass
                    
            elif response.status_code == 401:
                print(f"   🔒 401 - Sem permissão (mas URL existe)")
                working_urls.append((url, "401 - URL existe"))
            elif response.status_code == 404:
                print(f"   ❌ 404 - Não encontrado")
            else:
                print(f"   ⚠️ {response.status_code} - {response.reason}")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Erro de conexão")
        except requests.exceptions.Timeout:
            print(f"   ⏰ Timeout")
        except Exception as e:
            print(f"   ❌ Erro: {str(e)[:30]}...")
    
    print(f"\n📊 RESUMO:")
    if working_urls:
        print(f"   URLs que responderam:")
        for url, status in working_urls:
            print(f"   • {url} - {status}")
    else:
        print(f"   ❌ Nenhuma URL funcionou")
    
    return working_urls[0][0] if working_urls else None

if __name__ == "__main__":
    correct_url = find_correct_url()
    
    if correct_url:
        print(f"\n🎯 URL CORRETA ENCONTRADA: {correct_url}")
        print(f"\n📝 Para corrigir, atualize o arquivo de configuração com:")
        print(f"   BASE_URL = '{correct_url}'")
    else:
        print(f"\n❌ Não foi possível encontrar a URL correta")
        print(f"   Verifique a documentação da Factorial ou contate o suporte")
