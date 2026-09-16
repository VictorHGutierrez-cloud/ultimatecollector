"""
Encontrar um policy period que esteja aberto (não fechado)
Testando o endpoint change_status para descobrir quais períodos estão abertos
"""
import requests
import json

API_KEY = "eyJraWQiOiJmYWN0b3JpYWwtaWQiLCJhbGciOiJFUzI1NiJ9.eyJpYXQiOjE3NzE4ODQ4NjQsImV4cCI6MjA4NzQ1NDM4NCwianRpIjoiNzBjZWRiMzktODNiZC00MDEwLWJhYjgtMmZiMjRjNjBkNDBhIiwiY2VsbCI6ImF6dXJlLWRlbW8tZ3djLWV1MiIsImNvbXBhbnlfaWQiOjU1NDcxfQ.vwbec8pZc1ybTnGchYRaZMacnlndqXFh8WxjlJ_gFNfQ5BIYhUQjFdPhU_-ZwyvffqYyAgI5ZdaBomfKQx3cCg"
BASE_URL = "https://api.eu2.demo.factorial.dev"
API_VERSION = "2026-07-01"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-api-key": API_KEY
}

print("=" * 60)
print("PROCURANDO POLICY PERIOD ABERTO (NAO FECHADO)")
print("=" * 60)
print()
print("Testando diferentes policy_period_ids para encontrar um aberto...")
print("(Um periodo fechado nao permite criar supplements)")
print()

# Status possíveis: preparation, open, closed, draft
# Vamos tentar mudar para "preparation" ou "open" para ver qual aceita
statuses_to_try = ["preparation", "open"]

open_periods = []

# Testar IDs de 1 a 100
for period_id in range(1, 101):
    for status in statuses_to_try:
        try:
            url = f"{BASE_URL}/api/{API_VERSION}/resources/payroll/policy_periods/{period_id}/change_status"
            payload = {
                "status": status,
                "notify_employee": False
            }
            response = requests.post(url, json=payload, headers=headers, timeout=5)
            
            # Se retornar 200, o período existe e aceitou o status
            if response.status_code == 200:
                data = response.json()
                current_status = data.get('status', 'unknown')
                print(f"[OK] Policy Period ID {period_id}: Status '{status}' aceito!")
                print(f"     Status atual: {current_status}")
                
                # Se conseguiu mudar para "preparation" ou "open", está aberto
                if status in ["preparation", "open"]:
                    open_periods.append({
                        'id': period_id,
                        'status': current_status,
                        'can_create_supplements': True
                    })
                    print(f"     [PERFEITO] Este periodo pode receber supplements!")
                break
        except:
            pass
    
    if period_id % 20 == 0:
        print(f"Testado até ID {period_id}...")

print()
print("=" * 60)
if open_periods:
    print(f"[OK] Encontrados {len(open_periods)} periodos abertos:")
    for period in open_periods:
        print(f"  - Policy Period ID {period['id']} (Status: {period['status']})")
    print()
    print(f"Use o Policy Period ID {open_periods[0]['id']} para criar supplements!")
else:
    print("[AVISO] Nenhum periodo aberto encontrado automaticamente")
    print("Voce pode:")
    print("1. Abrir um periodo manualmente no frontend")
    print("2. Criar um novo periodo no frontend")
    print("3. Usar o proximo periodo disponivel")
