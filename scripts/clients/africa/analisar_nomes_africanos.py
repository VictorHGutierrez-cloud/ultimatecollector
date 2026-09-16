#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analisa quais colaboradores não têm nomes africanos
"""

import json
import csv
from pathlib import Path

# Nomes africanos comuns (exemplos)
nomes_africanos_comuns = [
    'ayo', 'kwame', 'chike', 'nia', 'amina', 'kone', 'mensah', 'okafor', 
    'obi', 'traore', 'kone', 'diop', 'sow', 'ndiaye', 'toure', 'diallo',
    'camara', 'keita', 'sangare', 'konate', 'ba', 'fall', 'ndoye',
    'ndiaye', 'sarr', 'thiam', 'gueye', 'faye', 'ndaw', 'seck'
]

def is_nome_africano(nome):
    """Verifica se o nome parece ser africano"""
    if not nome:
        return False
    
    nome_lower = nome.lower().strip()
    
    # Verificar se está na lista de nomes africanos comuns
    for nome_africano in nomes_africanos_comuns:
        if nome_africano in nome_lower:
            return True
    
    # Verificar padrões comuns de nomes africanos
    # Nomes comuns de origem africana ocidental
    if any(prefix in nome_lower for prefix in ['ayo', 'kwame', 'kofi', 'akua', 'ama']):
        return True
    
    return False

def analisar_colaboradores():
    """Analisa os colaboradores coletados"""
    print("=" * 80)
    print("ANALISE DE NOMES AFRICANOS")
    print("=" * 80)
    
    # Procurar arquivo mais recente
    employees_dir = Path('data/raw/employees')
    if not employees_dir.exists():
        print("\n[ERRO] Diretorio data/raw/employees nao encontrado!")
        print("Execute o coletor primeiro para coletar os dados.")
        return
    
    json_files = list(employees_dir.glob('*.json'))
    if not json_files:
        print("\n[ERRO] Nenhum arquivo JSON encontrado!")
        print("Execute o coletor primeiro para coletar os dados.")
        return
    
    # Pegar o arquivo mais recente
    latest_file = max(json_files, key=lambda p: p.stat().st_mtime)
    print(f"\nAnalisando arquivo: {latest_file.name}")
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            employees = json.load(f)
        
        print(f"Total de colaboradores: {len(employees)}")
        
        nomes_africanos = []
        nomes_nao_africanos = []
        
        for emp in employees:
            first_name = emp.get('first_name', '').strip()
            last_name = emp.get('last_name', '').strip()
            full_name = emp.get('full_name', '').strip()
            company_id = emp.get('company_id')
            
            # Verificar se tem nome africano
            tem_nome_africano = (
                is_nome_africano(first_name) or 
                is_nome_africano(last_name) or
                is_nome_africano(full_name)
            )
            
            info = {
                'id': emp.get('id'),
                'full_name': full_name or f"{first_name} {last_name}",
                'first_name': first_name,
                'last_name': last_name,
                'company_id': company_id,
                'email': emp.get('email', ''),
                'active': emp.get('active', False)
            }
            
            if tem_nome_africano:
                nomes_africanos.append(info)
            else:
                nomes_nao_africanos.append(info)
        
        print(f"\n" + "=" * 80)
        print(f"RESULTADOS:")
        print(f"=" * 80)
        print(f"\nColaboradores COM nomes africanos: {len(nomes_africanos)}")
        print(f"Colaboradores SEM nomes africanos: {len(nomes_nao_africanos)}")
        
        print(f"\n" + "=" * 80)
        print(f"COLABORADORES SEM NOMES AFRICANOS ({len(nomes_nao_africanos)}):")
        print(f"=" * 80)
        
        for i, emp in enumerate(nomes_nao_africanos, 1):
            status = "Ativo" if emp['active'] else "Inativo"
            print(f"{i:2d}. {emp['full_name']:<30} | ID: {emp['id']} | {status} | Company ID: {emp['company_id']}")
        
        if nomes_africanos:
            print(f"\n" + "=" * 80)
            print(f"COLABORADORES COM NOMES AFRICANOS ({len(nomes_africanos)}):")
            print(f"=" * 80)
            for i, emp in enumerate(nomes_africanos, 1):
                status = "Ativo" if emp['active'] else "Inativo"
                print(f"{i:2d}. {emp['full_name']:<30} | ID: {emp['id']} | {status} | Company ID: {emp['company_id']}")
        
        # Verificar Company ID
        company_ids = set(emp.get('company_id') for emp in employees)
        print(f"\n" + "=" * 80)
        print(f"INFORMACAO:")
        print(f"=" * 80)
        print(f"Company IDs encontrados: {company_ids}")
        if 27275 in company_ids:
            print(f"[AVISO] Estes dados sao do ambiente ANTIGO (Company ID 27275)")
            print(f"        Para ver os colaboradores do NOVO ambiente (Company ID 55229),")
            print(f"        execute o coletor novamente com o token correto configurado.")
        
    except Exception as e:
        print(f"\n[ERRO] Erro ao analisar: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 80)

if __name__ == '__main__':
    analisar_colaboradores()
