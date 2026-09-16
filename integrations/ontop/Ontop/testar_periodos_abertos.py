"""
Testar diferentes policy_period_ids para ver qual está aberto
Tentando criar um supplement em cada período para descobrir qual funciona
"""
import requests
import json
from datetime import datetime, timedelta

API_KEY = "eyJraWQiOiJmYWN0b3JpYWwtaWQiLCJhbGciOiJFUzI1NiJ9.eyJpYXQiOjE3NzE4ODQ4NjQsImV4cCI6MjA4NzQ1NDM4NCwianRpIjoiNzBjZWRiMzktODNiZC00MDEwLWJhYjgtMmZiMjRjNjBkNDBhIiwiY2VsbCI6ImF6dXJlLWRlbW8tZ3djLWV1MiIsImNvbXBhbnlfaWQiOjU1NDcxfQ.vwbec8pZc1ybTnGchYRaZMacnlndqXFh8WxjlJ_gFNfQ5BIYhUQjFdPhU_-ZwyvffqYyAgI5ZdaBomfKQx3cCg"
BASE_URL = "https://api.eu2.demo.factorial.dev"
API_VERSION = "2026-07-01"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-api-key": API_KEY
}

# Dados de teste
employee_id = 1792913
taxonomy_id = 1519835
effective_on = datetime.now().strftime('%Y-%m-%d')

print("=" * 60)
print("TESTANDO POLICY PERIODS PARA ENCONTRAR UM ABERTO")
print("=" * 60)
print()
print("Tentando criar um supplement em cada periodo...")
print("(Apenas periodos ABERTOS permitem criar supplements)")
print()

open_periods = []

# Testar IDs de 1 a 50
for period_id in range(1, 51):
    try:
        url = f"{BASE_URL}/api/{API_VERSION}/resources/payroll/supplements"
        payload = {
            'employee_id': employee_id,
            'amount_in_cents': 1000,  # Valor pequeno para teste
            'effective_on': effective_on,
            'contracts_taxonomy_id': taxonomy_id,
            'payroll_policy_period_id': period_id,
            'unit': 'money'
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        
        # Se retornar 201 (Created) ou 200, o período está aberto!
        if response.status_code == 201 or response.status_code == 200:
            data = response.json()
            supplement_id = data.get('id')
            print(f"[OK] Policy Period ID {period_id} ESTA ABERTO!")
            print(f"     Supplement criado com sucesso! ID: {supplement_id}")
            open_periods.append(period_id)
            
            # Deletar o supplement de teste
            try:
                delete_url = f"{BASE_URL}/api/{API_VERSION}/resources/payroll/supplements/{supplement_id}"
                requests.delete(delete_url, headers=headers, timeout=5)
                print(f"     (Supplement de teste deletado)")
            except:
                pass
            
            break  # Encontrou um aberto, pode parar
        elif response.status_code == 400:
            # Invalid parameters - período pode estar fechado ou dados inválidos
            error_text = response.text
            if "closed" in error_text.lower() or "period" in error_text.lower():
                # Provavelmente fechado
                pass
    except Exception as e:
        pass
    
    if period_id % 10 == 0:
        print(f"Testado até ID {period_id}...")

print()
print("=" * 60)
if open_periods:
    print(f"[OK] Encontrado periodo aberto: ID {open_periods[0]}")
    print()
    print("Use este ID no script:")
    print(f"  python test_factorial_data_insert.py {open_periods[0]}")
    print()
    print("Ou adicione ao config_unificado.env:")
    print(f"  POLICY_PERIOD_ID={open_periods[0]}")
else:
    print("[AVISO] Nenhum periodo aberto encontrado nos primeiros 50")
    print()
    print("Voce precisa:")
    print("1. Abrir um periodo no frontend do Factorial")
    print("2. Me passar o ID do periodo aberto")
    print("3. Ou adicionar POLICY_PERIOD_ID=XXX no config_unificado.env")
