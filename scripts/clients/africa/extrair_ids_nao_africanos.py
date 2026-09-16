#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrai os IDs dos colaboradores que NÃO têm nomes africanos de um arquivo CSV
"""

import csv
from pathlib import Path

# Nomes africanos comuns
nomes_africanos_comuns = [
    'ayo', 'kwame', 'chike', 'nia', 'amina', 'kone', 'mensah', 'okafor', 
    'obi', 'traore', 'diop', 'sow', 'ndiaye', 'toure', 'diallo',
    'camara', 'keita', 'sangare', 'konate', 'ba', 'fall', 'ndoye',
    'sarr', 'thiam', 'gueye', 'faye', 'ndaw', 'seck', 'nkosi',
    'abebe', 'taye', 'zola'
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
    if any(prefix in nome_lower for prefix in ['ayo', 'kwame', 'kofi', 'akua', 'ama']):
        return True
    
    return False

def extrair_ids_nao_africanos(arquivo_csv):
    """Extrai os IDs dos colaboradores que NÃO têm nomes africanos"""
    
    ids_nao_africanos = []
    
    try:
        with open(arquivo_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                first_name = row.get('first_name', '').strip()
                last_name = row.get('last_name', '').strip()
                full_name = row.get('full_name', '').strip()
                emp_id = row.get('id', '').strip()
                
                # Verificar se tem nome africano
                tem_nome_africano = (
                    is_nome_africano(first_name) or 
                    is_nome_africano(last_name) or
                    is_nome_africano(full_name)
                )
                
                # Se NÃO tem nome africano, adiciona o ID
                if not tem_nome_africano and emp_id:
                    ids_nao_africanos.append(emp_id)
        
        return ids_nao_africanos
    
    except Exception as e:
        print(f"[ERRO] Erro ao processar arquivo: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == '__main__':
    # Caminho do arquivo CSV
    arquivo_csv = 'data/raw/employees/employees_20260202_175128.csv'
    
    print("=" * 80)
    print("EXTRAINDO IDs DE COLABORADORES SEM NOMES AFRICANOS")
    print("=" * 80)
    print(f"\nArquivo: {arquivo_csv}")
    
    ids = extrair_ids_nao_africanos(arquivo_csv)
    
    print(f"\nTotal de IDs encontrados: {len(ids)}")
    print("\n" + "=" * 80)
    print("IDs DOS COLABORADORES SEM NOMES AFRICANOS:")
    print("=" * 80)
    
    # Mostrar os IDs
    for i, emp_id in enumerate(ids, 1):
        print(emp_id)
    
    print("\n" + "=" * 80)
    print(f"Total: {len(ids)} IDs")
    print("=" * 80)
    
    # Também salvar em um arquivo de texto
    arquivo_saida = 'ids_nao_africanos.txt'
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        for emp_id in ids:
            f.write(f"{emp_id}\n")
    
    print(f"\nIDs salvos em: {arquivo_saida}")
