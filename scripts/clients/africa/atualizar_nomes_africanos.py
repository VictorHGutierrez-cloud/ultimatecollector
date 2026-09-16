#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para atualizar nomes de colaboradores sem nomes africanos
Gera nomes africanos apropriados baseados no gênero e faz push na API Factorial

Uso:
    python atualizar_nomes_africanos.py [--teste] [--sim]
    
    --teste: Executa em modo teste (não atualiza na API)
    --sim: Pula confirmação e executa diretamente
"""

import csv
import random
import time
import sys
import argparse
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from ultimate_collector.core.api_client import APIClient
from ultimate_collector.core.config import Config

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Nomes africanos por gênero (diversos países africanos)
NOMES_AFRICANOS_FEMININO = [
    # África Ocidental
    'Amina', 'Fatou', 'Aissatou', 'Mariama', 'Awa', 'Ndeye', 'Khadija', 'Aissata',
    'Zainab', 'Hawa', 'Aicha', 'Binta', 'Sira', 'Aissata', 'Maimouna', 'Ramatou',
    # África Oriental
    'Nia', 'Zola', 'Thandi', 'Busisiwe', 'Naledi', 'Lindiwe', 'Nomsa', 'Sibongile',
    'Amara', 'Ifeoma', 'Adanna', 'Chioma', 'Ngozi', 'Amina', 'Zara', 'Kemi',
    # África Central
    'Mireille', 'Grace', 'Patience', 'Joy', 'Hope', 'Faith', 'Mercy', 'Peace',
    # África do Sul
    'Lerato', 'Palesa', 'Tshepo', 'Kgotso', 'Thabo', 'Kgosi', 'Lebo', 'Tumi'
]

NOMES_AFRICANOS_MASCULINO = [
    # África Ocidental
    'Kwame', 'Kofi', 'Ayo', 'Chike', 'Tunde', 'Babatunde', 'Adebayo', 'Olumide',
    'Ibrahim', 'Mohamed', 'Amadou', 'Moussa', 'Ousmane', 'Mamadou', 'Sekou', 'Bakary',
    # África Oriental
    'Taye', 'Abebe', 'Kebede', 'Haile', 'Yonas', 'Elias', 'Daniel', 'Solomon',
    'Mandla', 'Themba', 'Sipho', 'Thabo', 'Lungile', 'Bongani', 'Sizwe', 'Jabulani',
    # África Central
    'Jean', 'Pierre', 'Paul', 'Joseph', 'David', 'Samuel', 'Emmanuel', 'Gabriel',
    # África do Sul
    'Kgosi', 'Tshepo', 'Kgotso', 'Lebo', 'Tumi', 'Bongani', 'Sipho', 'Jabulani'
]

SOBRENOMES_AFRICANOS = [
    # África Ocidental
    'Mensah', 'Okafor', 'Obi', 'Traoré', 'Diop', 'Sow', 'Ndiaye', 'Toure', 'Diallo',
    'Camara', 'Keita', 'Sangare', 'Konate', 'Ba', 'Fall', 'Ndiaye', 'Sarr', 'Thiam',
    'Gueye', 'Faye', 'Nkosi', 'Mabena', 'Dlamini', 'Khumalo', 'Mthembu', 'Ndlovu',
    # África Oriental
    'Abebe', 'Kebede', 'Haile', 'Tesfaye', 'Gebre', 'Tadesse', 'Assefa', 'Mengistu',
    # África Central
    'Mukasa', 'Nkunda', 'Kabila', 'Lumumba', 'Mobutu', 'Kasa-Vubu',
    # África do Sul
    'Nkosi', 'Dlamini', 'Khumalo', 'Mthembu', 'Ndlovu', 'Mabena', 'Zulu', 'Xhosa'
]

def is_nome_africano(nome):
    """Verifica se o nome parece ser africano"""
    if not nome:
        return False
    
    nome_lower = nome.lower().strip()
    
    nomes_africanos_comuns = [
        'ayo', 'kwame', 'chike', 'nia', 'amina', 'kone', 'mensah', 'okafor', 
        'obi', 'traore', 'diop', 'sow', 'ndiaye', 'toure', 'diallo',
        'camara', 'keita', 'sangare', 'konate', 'ba', 'fall', 'ndoye',
        'sarr', 'thiam', 'gueye', 'faye', 'ndaw', 'seck', 'nkosi',
        'abebe', 'taye', 'zola', 'thandi', 'busisiwe', 'naledi'
    ]
    
    for nome_africano in nomes_africanos_comuns:
        if nome_africano in nome_lower:
            return True
    
    return False

def gerar_nome_africano(genero, nome_original=None):
    """
    Gera um nome africano apropriado baseado no gênero
    Tenta manter alguma similaridade com o nome original quando possível
    """
    genero_lower = genero.lower().strip() if genero else 'male'
    
    if genero_lower in ['female', 'f', 'feminino', 'mulher']:
        primeiro_nome = random.choice(NOMES_AFRICANOS_FEMININO)
    else:
        primeiro_nome = random.choice(NOMES_AFRICANOS_MASCULINO)
    
    sobrenome = random.choice(SOBRENOMES_AFRICANOS)
    
    return primeiro_nome, sobrenome

def ler_colaboradores_csv(arquivo_csv):
    """Lê o CSV e retorna lista de colaboradores sem nomes africanos"""
    colaboradores_para_atualizar = []
    
    try:
        with open(arquivo_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                emp_id = row.get('id', '').strip()
                first_name = row.get('first_name', '').strip()
                last_name = row.get('last_name', '').strip()
                full_name = row.get('full_name', '').strip()
                gender = row.get('gender', '').strip()
                active = row.get('active', '').strip().lower() == 'true'
                
                if not emp_id:
                    continue
                
                # Verificar se tem nome africano
                tem_nome_africano = (
                    is_nome_africano(first_name) or 
                    is_nome_africano(last_name) or
                    is_nome_africano(full_name)
                )
                
                # Se NÃO tem nome africano e está ativo, adiciona à lista
                if not tem_nome_africano and active:
                    colaboradores_para_atualizar.append({
                        'id': emp_id,
                        'first_name': first_name,
                        'last_name': last_name,
                        'full_name': full_name,
                        'gender': gender,
                        'access_id': row.get('access_id', '').strip()
                    })
        
        return colaboradores_para_atualizar
    
    except Exception as e:
        print(f"[ERRO] Erro ao ler CSV: {e}")
        import traceback
        traceback.print_exc()
        return []

def atualizar_nome_na_api(api_client, emp_id, access_id, novo_first_name, novo_last_name, api_version='2026-07-01', modo_teste=False):
    """
    Atualiza o nome do colaborador na API Factorial
    Tenta diferentes formatos de endpoint
    """
    # Tentar diferentes formatos de endpoint
    # A API Factorial pode usar access_id ou id, e diferentes formatos de endpoint
    endpoints = []
    
    # Tentar com ID
    endpoints.extend([
        f'api/{api_version}/resources/employees/employees/{emp_id}',  # Formato com resources/employees/employees
        f'api/{api_version}/resources/employees/{emp_id}',  # Formato com resources/employees
        f'api/{api_version}/employees/employees/{emp_id}',  # Formato sem resources
        f'api/{api_version}/employees/{emp_id}',  # Formato direto
    ])
    
    # Tentar com access_id se disponível
    if access_id:
        endpoints.extend([
            f'api/{api_version}/resources/employees/employees/{access_id}',
            f'api/{api_version}/resources/employees/{access_id}',
            f'api/{api_version}/employees/employees/{access_id}',
            f'api/{api_version}/employees/{access_id}',
        ])
    
    # Dados para atualização
    data = {
        'first_name': novo_first_name,
        'last_name': novo_last_name
    }
    
    if modo_teste:
        print(f"  [MODO TESTE] Não atualizando na API")
        print(f"  Dados que seriam enviados: {data}")
        return True
    
    for endpoint in endpoints:
        try:
            print(f"  [INFO] Tentando endpoint: {endpoint}")
            # Suprimir logs do api_client durante a requisição para evitar problemas de encoding
            import logging
            old_level = logging.getLogger('core.api_client').level
            logging.getLogger('core.api_client').setLevel(logging.ERROR)
            
            try:
                response = api_client.patch(endpoint, data=data)
            finally:
                logging.getLogger('core.api_client').setLevel(old_level)
            
            if response:
                print(f"  [OK] Sucesso! Nome atualizado para: {novo_first_name} {novo_last_name}")
                return True
            else:
                print(f"  [ERRO] Resposta vazia, tentando próximo endpoint...")
                continue
                
        except Exception as e:
            error_msg = str(e)
            if '404' in error_msg or 'Not Found' in error_msg:
                print(f"  [ERRO] Endpoint não encontrado, tentando próximo...")
                continue
            elif '401' in error_msg or 'Unauthorized' in error_msg:
                print(f"  [ERRO] Erro de autenticação: {e}")
                return False
            else:
                print(f"  [ERRO] Erro: {e}, tentando próximo endpoint...")
                continue
    
    print(f"  [ERRO] Todos os endpoints falharam")
    return False

def main():
    """Função principal"""
    # Parse de argumentos
    parser = argparse.ArgumentParser(description='Atualiza nomes africanos na API Factorial')
    parser.add_argument('--teste', action='store_true', help='Modo teste (não atualiza na API)')
    parser.add_argument('--sim', action='store_true', help='Pula confirmação e executa diretamente')
    args = parser.parse_args()
    
    print("=" * 80)
    print("ATUALIZACAO DE NOMES AFRICANOS - API FACTORIAL")
    print("=" * 80)
    
    # Configurações
    arquivo_csv = 'data/raw/employees/employees_20260202_175128.csv'
    api_version = '2026-07-01'  # Versão da API Factorial
    
    # Verificar se o arquivo existe
    if not Path(arquivo_csv).exists():
        print(f"\n[ERRO] Arquivo não encontrado: {arquivo_csv}")
        return
    
    # Ler colaboradores do CSV
    print(f"\n[INFO] Lendo arquivo: {arquivo_csv}")
    colaboradores = ler_colaboradores_csv(arquivo_csv)
    
    if not colaboradores:
        print("\n[INFO] Nenhum colaborador encontrado para atualizar.")
        return
    
    print(f"\n[INFO] Total de colaboradores para atualizar: {len(colaboradores)}")
    
    # Mostrar preview dos nomes que serão gerados
    print("\n" + "=" * 80)
    print("PREVIEW - NOVOS NOMES AFRICANOS:")
    print("=" * 80)
    
    previews = []
    for colab in colaboradores[:10]:  # Mostrar apenas os 10 primeiros
        novo_first, novo_last = gerar_nome_africano(colab['gender'], colab['first_name'])
        previews.append({
            'id': colab['id'],
            'nome_atual': colab['full_name'],
            'genero': colab['gender'],
            'novo_nome': f"{novo_first} {novo_last}"
        })
        print(f"  ID {colab['id']:8s} | {colab['full_name']:30s} -> {novo_first} {novo_last} ({colab['gender']})")
    
    if len(colaboradores) > 10:
        print(f"  ... e mais {len(colaboradores) - 10} colaboradores")
    
    # Determinar modo de execução
    modo_teste = args.teste
    
    if args.sim:
        # Modo automático - pula confirmação
        if modo_teste:
            print("\n[INFO] Modo TESTE ativado (via --teste) - nenhuma alteracao sera feita na API")
        else:
            print("\n[INFO] Modo REAL ativado (via --sim) - as alteracoes serao feitas na API")
    else:
        # Modo interativo - pedir confirmação
        print("\n" + "=" * 80)
        print("OPCOES:")
        print("  1. Modo TESTE (nao atualiza na API, apenas mostra o que seria feito)")
        print("  2. Modo REAL (atualiza na API)")
        print("  3. Cancelar")
        
        try:
            resposta = input("\nEscolha uma opcao (1/2/3): ").strip()
            
            if resposta == '1':
                modo_teste = True
                print("\n[INFO] Modo TESTE ativado - nenhuma alteracao sera feita na API")
            elif resposta == '2':
                modo_teste = False
                print("\n[INFO] Modo REAL ativado - as alteracoes serao feitas na API")
                confirmacao = input("Tem certeza? (sim/nao): ").strip().lower()
                if confirmacao not in ['sim', 's', 'yes', 'y']:
                    print("\n[INFO] Operacao cancelada pelo usuario.")
                    return
            else:
                print("\n[INFO] Operacao cancelada pelo usuario.")
                return
        except (EOFError, KeyboardInterrupt):
            print("\n[INFO] Operacao cancelada.")
            return
    
    # Inicializar cliente da API
    print("\n[INFO] Conectando à API Factorial...")
    try:
        api_client = APIClient()
        
        # Testar conexão
        if not api_client.test_connection():
            print("[AVISO] Teste de conexão falhou, mas continuando...")
    except Exception as e:
        print(f"[ERRO] Erro ao conectar à API: {e}")
        return
    
    # Processar cada colaborador
    print("\n" + "=" * 80)
    print("ATUALIZANDO NOMES NA API:")
    print("=" * 80)
    
    sucessos = 0
    erros = 0
    atualizacoes = []
    
    for i, colab in enumerate(colaboradores, 1):
        print(f"\n[{i}/{len(colaboradores)}] Processando ID {colab['id']} - {colab['full_name']}")
        
        # Gerar novo nome africano
        novo_first, novo_last = gerar_nome_africano(colab['gender'], colab['first_name'])
        
        print(f"  Nome atual: {colab['full_name']} ({colab['gender']})")
        print(f"  Novo nome: {novo_first} {novo_last}")
        
        # Atualizar na API
        sucesso = atualizar_nome_na_api(
            api_client, 
            colab['id'],
            colab.get('access_id', ''),
            novo_first, 
            novo_last,
            api_version,
            modo_teste=modo_teste
        )
        
        if sucesso:
            sucessos += 1
            atualizacoes.append({
                'id': colab['id'],
                'nome_antigo': colab['full_name'],
                'nome_novo': f"{novo_first} {novo_last}",
                'genero': colab['gender']
            })
        else:
            erros += 1
        
        # Pequeno delay para não sobrecarregar a API
        time.sleep(0.5)
    
    # Resumo final
    print("\n" + "=" * 80)
    print("RESUMO DA ATUALIZAÇÃO:")
    print("=" * 80)
    print(f"[OK] Sucessos: {sucessos}")
    print(f"[ERRO] Erros: {erros}")
    print(f"[INFO] Total processado: {len(colaboradores)}")
    
    # Salvar log das atualizações
    if atualizacoes:
        log_file = 'atualizacoes_nomes_africanos.json'
        import json
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(atualizacoes, f, indent=2, ensure_ascii=False)
        print(f"\n[INFO] Log salvo em: {log_file}")
    
    print("\n" + "=" * 80)
    
    # Fechar conexão
    api_client.close()

if __name__ == '__main__':
    main()
