"""
Script para inserir dados de teste na API Factorial
Cria Supplements e Additional Compensations para testar o relatório SQL

PRÉ-REQUISITOS:
1. Ter um arquivo com a API key do Factorial (ou usar variável de ambiente)
2. Ter funcionários ativos no Factorial
3. Ter policy periods configurados
4. Ter taxonomies disponíveis

USO:
    python test_factorial_data_insert.py

CONFIGURAÇÃO:
    - Ajuste FACTORIAL_API_KEY no código ou use variável de ambiente
    - Ajuste BASE_URL se necessário (padrão: https://api.factorialhr.com)
"""

import requests
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path

# ============================================
# CONFIGURAÇÕES - Carregar do arquivo .env
# ============================================

def load_env_config():
    """Carrega configurações do arquivo .env"""
    config = {}
    
    # Tentar encontrar arquivo .env
    env_files = [
        Path('.env'),
        Path('config_unificado.env'),
        Path('../config_unificado.env'),
        Path('../../config_unificado.env')
    ]
    
    env_file = None
    for file_path in env_files:
        if file_path.exists():
            env_file = file_path
            break
    
    if env_file:
        print(f"Carregando configuracoes de: {env_file}")
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    else:
        print("AVISO: Arquivo .env nao encontrado, usando variaveis de ambiente")
    
    return config

# Carregar configurações
ENV_CONFIG = load_env_config()

# API Key do Factorial (do .env ou variável de ambiente)
API_KEY = ENV_CONFIG.get('API_KEY') or os.getenv('FACTORIAL_API_KEY') or os.getenv('API_KEY')

# Base URL da API Factorial (do .env ou padrão)
BASE_URL = ENV_CONFIG.get('BASE_URL') or os.getenv('FACTORIAL_BASE_URL') or 'https://api.factorialhr.com'

# Versão da API (do .env ou padrão)
API_VERSION = ENV_CONFIG.get('API_VERSION') or os.getenv('API_VERSION') or '2026-07-01'

# Tipo de autenticação (do .env ou padrão)
AUTH_TYPE = ENV_CONFIG.get('AUTH_TYPE', 'bearer').lower()

# Headers padrão - Priorizar AUTH_TYPE do config
if AUTH_TYPE == 'x-api-key':
    # Usar x-api-key no header (sem Bearer)
    HEADERS = {
        'x-api-key': API_KEY,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
elif AUTH_TYPE == 'bearer' or (API_KEY and API_KEY.startswith('eyJ')):
    # JWT token - usar Bearer
    HEADERS = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
else:
    # Usar Bearer token (padrão)
    HEADERS = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }


# ============================================
# FUNÇÕES AUXILIARES
# ============================================

def make_request(method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
    """
    Faz uma requisição à API Factorial
    
    Args:
        method: Método HTTP (GET, POST, PUT, DELETE)
        endpoint: Endpoint da API (sem base URL, já com formato completo)
        data: Dados para enviar no body (opcional)
    
    Returns:
        Resposta da API como dicionário
    """
    # Se o endpoint já começa com 'api/', usar direto, senão adicionar o prefixo
    if endpoint.startswith('api/'):
        url = f"{BASE_URL}/{endpoint}"
    else:
        url = f"{BASE_URL}/api/{API_VERSION}/resources/{endpoint}"
    
    response = None
    try:
        if method == 'GET':
            response = requests.get(url, headers=HEADERS, params=data)
        elif method == 'POST':
            response = requests.post(url, headers=HEADERS, json=data)
        elif method == 'PUT':
            response = requests.put(url, headers=HEADERS, json=data)
        elif method == 'DELETE':
            response = requests.delete(url, headers=HEADERS)
        else:
            raise ValueError(f"Método HTTP não suportado: {method}")
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as e:
        if response is not None:
            print(f"[ERRO] Erro HTTP {response.status_code}: {response.text}")
            try:
                error_detail = response.json()
                print(f"   Detalhes: {json.dumps(error_detail, indent=2, ensure_ascii=False)}")
            except:
                pass
        else:
            print(f"[ERRO] Erro HTTP: {str(e)}")
        raise
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Erro na requisição: {str(e)}")
        raise
    except Exception as e:
        print(f"[ERRO] Erro inesperado: {str(e)}")
        raise


def get_active_employees() -> List[Dict]:
    """
    Busca todos os funcionários ativos
    
    Returns:
        Lista de funcionários ativos
    """
    print(" Buscando funcionários ativos...")
    
    try:
        # Buscar todos os funcionários e filtrar os ativos
        # Endpoint correto: api/{version}/resources/employees/employees
        response = make_request('GET', f'api/{API_VERSION}/resources/employees/employees')
        all_employees = response.get('data', [])
        
        # Filtrar apenas os ativos - tentar diferentes campos
        active_employees = []
        for emp in all_employees:
            # Tentar diferentes campos que podem indicar status ativo
            status = emp.get('status') or emp.get('active') or emp.get('is_active')
            if status == 'active' or status == True or status == 'true':
                active_employees.append(emp)
        
        # Se não encontrou nenhum ativo, usar todos (pode ser que não tenha campo status)
        if not active_employees and all_employees:
            print(f"[AVISO] Nenhum funcionario com status='active' encontrado. Usando todos os funcionarios disponiveis.")
            active_employees = all_employees
        
        print(f"[OK] Encontrados {len(active_employees)} funcionarios ativos (de {len(all_employees)} total)")
        return active_employees
    except Exception as e:
        print(f"[ERRO] Erro ao buscar funcionários: {str(e)}")
        return []


def get_policy_periods() -> List[Dict]:
    """
    Busca os policy periods disponíveis
    
    Returns:
        Lista de policy periods
    """
    print(" Buscando policy periods...")
    
    try:
        # Endpoint correto: api/{version}/resources/payroll/policy_periods
        response = make_request('GET', f'api/{API_VERSION}/resources/payroll/policy_periods')
        periods = response.get('data', [])
        print(f"[OK] Encontrados {len(periods)} policy periods")
        return periods
    except Exception as e:
        print(f"[ERRO] Erro ao buscar policy periods: {str(e)}")
        return []


def get_taxonomies() -> List[Dict]:
    """
    Busca as taxonomies disponíveis (tipos de compensação)
    
    Returns:
        Lista de taxonomies
    """
    print(" Buscando taxonomies...")
    
    try:
        # Endpoint correto: api/{version}/resources/contracts/taxonomies
        response = make_request('GET', f'api/{API_VERSION}/resources/contracts/taxonomies')
        taxonomies = response.get('data', [])
        print(f"[OK] Encontradas {len(taxonomies)} taxonomies")
        return taxonomies
    except Exception as e:
        print(f"[ERRO] Erro ao buscar taxonomies: {str(e)}")
        return []


def get_employee_contracts(employee_id: int) -> List[Dict]:
    """
    Busca os contratos de um funcionário
    
    Args:
        employee_id: ID do funcionário
    
    Returns:
        Lista de contratos (contract versions)
    """
    try:
        # Endpoint correto: api/{version}/resources/contracts/contract_versions
        # A API pode aceitar employee_ids como array ou como parâmetro único
        try:
            response = make_request('GET', f'api/{API_VERSION}/resources/contracts/contract_versions', {
                'employee_ids[]': [employee_id]
            })
        except:
            # Tentar formato alternativo
            response = make_request('GET', f'api/{API_VERSION}/resources/contracts/contract_versions', {
                'employee_id': employee_id
            })
        
        contracts = response.get('data', [])
        return contracts
    except Exception as e:
        print(f"[AVISO] Erro ao buscar contratos do funcionário {employee_id}: {str(e)}")
        return []


# ============================================
# FUNÇÕES DE CRIAÇÃO
# ============================================

def create_supplement(
    employee_id: int,
    amount_in_cents: int,
    effective_on: str,
    contracts_taxonomy_id: int,
    payroll_policy_period_id: Optional[int] = None,
    unit: str = 'money',
    contracts_compensation_id: Optional[int] = None,
    worked_days: Optional[int] = None
) -> Optional[Dict]:
    """
    Cria um Supplement (Suplemento)
    
    Args:
        employee_id: ID do funcionário
        amount_in_cents: Valor em centavos (ex: 50000 = $500.00)
        effective_on: Data efetiva no formato YYYY-MM-DD
        contracts_taxonomy_id: ID da taxonomy
        payroll_policy_period_id: ID do policy period
        unit: Unidade (padrão: 'money')
        contracts_compensation_id: ID da compensação (opcional)
        worked_days: Dias trabalhados (opcional)
    
    Returns:
        Dados do supplement criado ou None em caso de erro
    """
    data = {
        'employee_id': employee_id,
        'amount_in_cents': amount_in_cents,
        'effective_on': effective_on,
        'contracts_taxonomy_id': contracts_taxonomy_id,
        'payroll_policy_period_id': payroll_policy_period_id,
        'unit': unit
    }
    
    if contracts_compensation_id:
        data['contracts_compensation_id'] = contracts_compensation_id
    
    if worked_days:
        data['worked_days'] = worked_days
    
    try:
        print(f"  Criando supplement para funcionario {employee_id}...")
        # Endpoint correto: api/{version}/resources/payroll/supplements
        response = make_request('POST', f'api/{API_VERSION}/resources/payroll/supplements', data)
        print(f"  [OK] Supplement criado com sucesso (ID: {response.get('id', 'N/A')})")
        return response
    except Exception as e:
        print(f"  [ERRO] Erro ao criar supplement: {str(e)}")
        return None


def create_additional_compensation(
    contract_version_id: int,
    contracts_taxonomy_id: int,
    amount: int,
    unit: str = 'money',
    description: Optional[str] = None,
    compensation_type: Optional[str] = None,
    first_payment_on: Optional[str] = None,
    starts_on: Optional[str] = None,
    recurrence: Optional[str] = None,
    recurrence_count: Optional[int] = None
) -> Optional[Dict]:
    """
    Cria uma Additional Compensation (Compensação Adicional)
    
    Args:
        contract_version_id: ID da versão do contrato
        contracts_taxonomy_id: ID da taxonomy
        amount: Valor em centavos
        unit: Unidade (padrão: 'money')
        description: Descrição (opcional)
        compensation_type: Tipo de compensação (opcional)
        first_payment_on: Data do primeiro pagamento YYYY-MM-DD (opcional)
        starts_on: Data de início YYYY-MM-DD (opcional)
        recurrence: Recorrência (opcional)
        recurrence_count: Contagem de recorrência (opcional)
    
    Returns:
        Dados da compensação criada ou None em caso de erro
    """
    data = {
        'contract_version_id': contract_version_id,
        'contracts_taxonomy_id': contracts_taxonomy_id,
        'amount': amount,
        'unit': unit
    }
    
    if description:
        data['description'] = description
    
    # NÃO incluir compensation_type - não está na lista válida e causa erro 422
    # if compensation_type:
    #     data['compensation_type'] = compensation_type
    
    if first_payment_on:
        data['first_payment_on'] = first_payment_on
    
    if starts_on:
        data['starts_on'] = starts_on
    
    if recurrence:
        data['recurrence'] = recurrence
    
    if recurrence_count:
        data['recurrence_count'] = recurrence_count
    
    try:
        print(f"  Criando additional compensation para contrato {contract_version_id}...")
        # Endpoint correto: api/{version}/resources/contracts/compensations
        response = make_request('POST', f'api/{API_VERSION}/resources/contracts/compensations', data)
        print(f"  [OK] Additional compensation criada com sucesso (ID: {response.get('id', 'N/A')})")
        return response
    except Exception as e:
        print(f"  [ERRO] Erro ao criar additional compensation: {str(e)}")
        return None


# ============================================
# FUNÇÃO PRINCIPAL
# ============================================

def main():
    """
    Função principal que cria dados de teste
    """
    print("=" * 60)
    print("INICIANDO CRIACAO DE DADOS DE TESTE - FACTORIAL")
    print("=" * 60)
    print()
    
    # Verificar API key
    if not API_KEY:
        print("[ERRO] ERRO: API Key não configurada!")
        print()
        print("Como configurar:")
        print("   1. Adicione API_KEY no arquivo config_unificado.env")
        print("   2. Ou use variável de ambiente: $env:API_KEY = 'sua_chave'")
        print("   3. Ou use: $env:FACTORIAL_API_KEY = 'sua_chave'")
        return
    
    # Mostrar configuração (parcialmente mascarada)
    masked_key = API_KEY[:8] + '...' + API_KEY[-4:] if len(API_KEY) > 12 else '***'
    print(f"API Key configurada: {masked_key}")
    print(f" Base URL: {BASE_URL}")
    print(f" Versão API: {API_VERSION}")
    print(f" Tipo de Autenticação: {AUTH_TYPE}")
    print()
    
    # 1. Buscar dados necessários
    employees = get_active_employees()
    if not employees:
        print("[ERRO] Nenhum funcionário ativo encontrado. Abortando...")
        return
    
    # Policy periods: descobrir através de supplements ou usar ID padrão
    # IMPORTANTE: O periodo precisa estar ABERTO (status "preparation" ou "open")
    # Periodos FECHADOS nao permitem criar supplements
    policy_periods = get_policy_periods()
    
    # Permitir passar policy_period_id via variável de ambiente ou argumento
    import sys
    env_policy_period_id = ENV_CONFIG.get('POLICY_PERIOD_ID')
    
    if env_policy_period_id:
        policy_period_id = int(env_policy_period_id)
        print(f"[INFO] Usando Policy Period ID do config: {policy_period_id}")
    elif len(sys.argv) > 1:
        try:
            policy_period_id = int(sys.argv[1])
            print(f"[INFO] Usando Policy Period ID do argumento: {policy_period_id}")
        except:
            policy_period_id = 1
            print("[AVISO] Argumento invalido. Usando ID 1...")
    elif not policy_periods:
        policy_period_id = 1  # ID padrão
        print("[AVISO] Usando Policy Period ID 1 (padrao)")
        print("[AVISO] CERTIFIQUE-SE que este periodo esta ABERTO no frontend!")
    else:
        policy_period_id = policy_periods[0]['id']
    
    taxonomies = get_taxonomies()
    if not taxonomies:
        print("[ERRO] Nenhuma taxonomy encontrada. Abortando...")
        return
    
    print()
    print("=" * 60)
    print("DADOS ENCONTRADOS")
    print("=" * 60)
    print(f"Funcionarios: {len(employees)}")
    print(f"Policy Periods: {len(policy_periods) if policy_periods else 0}")
    print(f"Taxonomies: {len(taxonomies)}")
    print()
    
    # 2. Preparar dados para criação
    # Usar os primeiros registros encontrados
    selected_employee = employees[0]
    selected_taxonomy = taxonomies[0]
    
    employee_id = selected_employee['id']
    taxonomy_id = selected_taxonomy['id']
    
    print(f"Funcionario selecionado: {selected_employee.get('full_name', 'N/A')} (ID: {employee_id})")
    print(f"Policy Period selecionado: ID {policy_period_id}")
    print(f"Taxonomy selecionada: {selected_taxonomy.get('name', 'N/A')} (ID: {taxonomy_id})")
    print()
    
    # 3. Buscar contratos do funcionário
    contracts = get_employee_contracts(employee_id)
    if not contracts:
        print("[AVISO] Nenhum contrato encontrado para o funcionário. Pulando criação de additional compensations.")
        contract_version_id = None
    else:
        contract_version_id = contracts[0]['id']
        print(f" Contrato selecionado: ID {contract_version_id}")
    print()
    
    # 4. Criar Supplements
    print("=" * 60)
    print(" CRIANDO SUPPLEMENTS")
    print("=" * 60)
    
    # Criar 3 supplements com datas diferentes (últimos 6 meses)
    supplements_created = []
    base_date = datetime.now()
    
    for i in range(3):
        # Data retrocedendo 2 meses por vez
        date = base_date - timedelta(days=60 * i)
        effective_on = date.strftime('%Y-%m-%d')
        
        # Valor variável: $100, $200, $300
        amount_in_cents = (i + 1) * 10000  # 10000 = $100.00
        
        supplement = create_supplement(
            employee_id=employee_id,
            amount_in_cents=amount_in_cents,
            effective_on=effective_on,
            contracts_taxonomy_id=taxonomy_id,
            payroll_policy_period_id=policy_period_id,
            unit='money'
        )
        
        if supplement:
            supplements_created.append(supplement)
    
    print()
    print(f"[OK] Total de supplements criados: {len(supplements_created)}")
    print()
    
    # 5. Criar Additional Compensations (se houver contrato)
    additional_compensations_created = []
    
    if contract_version_id:
        print("=" * 60)
        print(" CRIANDO ADDITIONAL COMPENSATIONS")
        print("=" * 60)
        
        # Criar 2 additional compensations
        for i in range(2):
            # Data retrocedendo 3 meses por vez
            date = base_date - timedelta(days=90 * i)
            first_payment_on = date.strftime('%Y-%m-%d')
            
            # Valor variável: $150, $250
            amount = (i + 1.5) * 10000  # 15000 = $150.00, 25000 = $250.00
            
            compensation = create_additional_compensation(
                contract_version_id=contract_version_id,
                contracts_taxonomy_id=taxonomy_id,
                amount=int(amount),
                unit='money',
                description=f'Test Additional Compensation {i + 1}',
                first_payment_on=first_payment_on
                # Removido compensation_type - não está na lista válida
            )
            
            if compensation:
                additional_compensations_created.append(compensation)
        
        print()
        print(f"[OK] Total de additional compensations criadas: {len(additional_compensations_created)}")
        print()
    
    # 6. Resumo final
    print("=" * 60)
    print("RESUMO FINAL")
    print("=" * 60)
    print(f"[OK] Supplements criados: {len(supplements_created)}")
    print(f"[OK] Additional Compensations criadas: {len(additional_compensations_created)}")
    print()
    print("Agora voce pode executar o SQL de relatorio para verificar os dados!")
    print()
    
    # Salvar IDs criados em arquivo JSON para referência
    summary = {
        'created_at': datetime.now().isoformat(),
        'employee_id': employee_id,
        'supplements': [s.get('id') for s in supplements_created],
        'additional_compensations': [c.get('id') for c in additional_compensations_created]
    }
    
    with open('factorial_test_data_created.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(" Resumo salvo em: factorial_test_data_created.json")


if __name__ == '__main__':
    main()
