#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para listar todos os colaboradores com seus IDs e nomes
"""

import pandas as pd
import os

def listar_colaboradores():
    """Lista todos os colaboradores com ID, nome e status"""
    
    # Caminho para o arquivo de funcionários
    arquivo_funcionarios = "Dados_Coletados/Dados_Brutos/Dados da API/Funcionários/employees_20250912_132435.csv"
    
    if not os.path.exists(arquivo_funcionarios):
        print("❌ Arquivo de funcionários não encontrado!")
        return
    
    try:
        # Ler o arquivo CSV
        df = pd.read_csv(arquivo_funcionarios)
        
        print("👥 RELAÇÃO DE COLABORADORES - FACTORIAL API")
        print("=" * 80)
        print(f"📊 Total de colaboradores: {len(df)}")
        print("=" * 80)
        print()
        
        # Filtrar apenas colaboradores ativos
        ativos = df[df['active'] == True]
        inativos = df[df['active'] == False]
        
        print("✅ COLABORADORES ATIVOS:")
        print("-" * 50)
        for _, row in ativos.iterrows():
            status_icon = "🟢" if row['active'] else "🔴"
            print(f"{status_icon} ID: {row['id']:6d} | {row['full_name']:25s} | {row['email']}")
        
        print()
        print("❌ COLABORADORES INATIVOS:")
        print("-" * 50)
        for _, row in inativos.iterrows():
            status_icon = "🟢" if row['active'] else "🔴"
            print(f"{status_icon} ID: {row['id']:6d} | {row['full_name']:25s} | {row['email']}")
        
        print()
        print("📋 RESUMO:")
        print(f"   • Total de colaboradores: {len(df)}")
        print(f"   • Ativos: {len(ativos)}")
        print(f"   • Inativos: {len(inativos)}")
        print()
        
        # Mostrar alguns exemplos de IDs para teste
        print("🧪 IDS SUGERIDOS PARA TESTE:")
        print("-" * 30)
        ids_ativos = ativos['id'].head(5).tolist()
        for emp_id in ids_ativos:
            nome = ativos[ativos['id'] == emp_id]['full_name'].iloc[0]
            print(f"   • ID {emp_id}: {nome}")
        
        print()
        print("💡 DICA: Use estes IDs nos exemplos de clock in/clock out!")
        
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {e}")

def buscar_colaborador_por_id(employee_id):
    """Busca um colaborador específico pelo ID"""
    
    arquivo_funcionarios = "Dados_Coletados/Dados_Brutos/Dados da API/Funcionários/employees_20250912_132435.csv"
    
    if not os.path.exists(arquivo_funcionarios):
        print("❌ Arquivo de funcionários não encontrado!")
        return
    
    try:
        df = pd.read_csv(arquivo_funcionarios)
        
        # Buscar o colaborador
        colaborador = df[df['id'] == employee_id]
        
        if colaborador.empty:
            print(f"❌ Colaborador com ID {employee_id} não encontrado!")
            return
        
        col = colaborador.iloc[0]
        
        print(f"👤 COLABORADOR ENCONTRADO:")
        print("=" * 40)
        print(f"ID: {col['id']}")
        print(f"Nome: {col['full_name']}")
        print(f"Email: {col['email']}")
        print(f"Status: {'🟢 Ativo' if col['active'] else '🔴 Inativo'}")
        print(f"Gênero: {col['gender']}")
        print(f"Idade: {col['age_number']} anos")
        print(f"Telefone: {col['phone_number']}")
        print(f"Data de criação: {col['created_at']}")
        
        if col['is_terminating']:
            print(f"⚠️  Funcionário em processo de desligamento")
            print(f"   Data de desligamento: {col['terminated_on']}")
        
    except Exception as e:
        print(f"❌ Erro ao buscar colaborador: {e}")

def main():
    """Função principal"""
    print("🔍 SISTEMA DE BUSCA DE COLABORADORES")
    print("=" * 50)
    
    while True:
        print("\nOpções:")
        print("1. Listar todos os colaboradores")
        print("2. Buscar colaborador por ID")
        print("3. Sair")
        
        opcao = input("\nEscolha uma opção (1-3): ").strip()
        
        if opcao == "1":
            listar_colaboradores()
        elif opcao == "2":
            try:
                emp_id = int(input("Digite o ID do colaborador: "))
                buscar_colaborador_por_id(emp_id)
            except ValueError:
                print("❌ ID deve ser um número inteiro!")
        elif opcao == "3":
            print("👋 Até logo!")
            break
        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    main()
