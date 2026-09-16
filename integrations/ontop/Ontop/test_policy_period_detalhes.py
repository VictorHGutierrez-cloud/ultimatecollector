"""
Testar policy period com diferentes status e ver resposta de erro
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

# Testar alguns IDs com diferentes status
test_ids = [1, 10, 50, 100]
statuses = ["preparation", "open", "closed", "draft"]

print("=" * 60)
print("TESTANDO POLICY PERIODS COM DIFERENTES STATUS")
print("=" * 60)
print()

for test_id in test_ids:
    print(f"Testando ID {test_id}:")
    for status in statuses:
        try:
            url = f"{BASE_URL}/api/{API_VERSION}/resources/payroll/policy_periods/{test_id}/change_status"
            payload = {
                "status": status,
                "notify_employee": False
            }
            response = requests.post(url, json=payload, headers=headers, timeout=5)
            
            if response.status_code != 400 and response.status_code != 404:
                print(f"  Status '{status}': {response.status_code}")
                print(f"  Resposta: {response.text[:200]}")
                if response.status_code == 200:
                    print(f"  [OK] ID {test_id} com status '{status}' FUNCIONOU!")
                    data = response.json()
                    print(f"  Dados: {json.dumps(data, indent=2)[:300]}")
                    break
            elif response.status_code == 400:
                # Verificar se o erro é sobre status inválido ou ID não encontrado
                error_text = response.text
                if "not found" in error_text.lower() or "does not exist" in error_text.lower():
                    # ID não existe, pular
                    break
        except Exception as e:
            pass
    print()

print()
print("Se nenhum funcionou, o policy period precisa ser criado manualmente no frontend")
print("ou o endpoint GET precisa estar disponivel para listar os existentes")
