#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar turnos de agosto para todos os funcionários ativos
"""

import sys
import os
import pandas as pd
from datetime import datetime, timezone, timedelta
import random
import time

# Adicionar o diretório do projeto ao path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from senders.attendance_sender import AttendanceSender

def gerar_horarios_turno():
    """Gera horários realistas de entrada e saída"""
    # Horários típicos de trabalho (8h às 17h, 9h às 18h, etc.)
    horarios_entrada = [
        "08:00", "08:15", "08:30", "08:45", "09:00", "09:15"
    ]
    horarios_saida = [
        "17:00", "17:15", "17:30", "17:45", "18:00", "18:15", "18:30"
    ]
    
    entrada = random.choice(horarios_entrada)
    saida = random.choice(horarios_saida)
    
    return entrada, saida

def gerar_turnos_agosto():
    """Gera turnos para todos os funcionários ativos em agosto"""
    
    print("🗓️  GERADOR DE TURNOS - AGOSTO 2024")
    print("=" * 50)
    
    # Ler lista de funcionários
    arquivo_funcionarios = "Dados_Coletados/Dados_Brutos/Dados da API/Funcionários/employees_20250912_132435.csv"
    
    if not os.path.exists(arquivo_funcionarios):
        print("❌ Arquivo de funcionários não encontrado!")
        return
    
    try:
        df = pd.read_csv(arquivo_funcionarios)
        funcionarios_ativos = df[df['active'] == True]
        
        print(f"👥 Encontrados {len(funcionarios_ativos)} funcionários ativos")
        print()
        
        # Criar instância do sender
        sender = AttendanceSender()
        
        # Testar conexão
        print("🔌 Testando conexão com a API...")
        if not sender.test_connection():
            print("❌ Erro: Não foi possível conectar à API!")
            return
        
        print("✅ Conexão estabelecida!")
        print()
        
        # Gerar turnos para cada dia de agosto (1 a 31)
        dias_agosto = list(range(1, 32))
        
        # Remover fins de semana (sábado=5, domingo=6)
        dias_uteis = []
        for dia in dias_agosto:
            data = datetime(2024, 8, dia)
            if data.weekday() < 5:  # Segunda=0, Sexta=4
                dias_uteis.append(dia)
        
        print(f"📅 Gerando turnos para {len(dias_uteis)} dias úteis de agosto")
        print(f"   Dias: {dias_uteis}")
        print()
        
        total_turnos = 0
        sucessos = 0
        erros = 0
        
        for idx, funcionario in funcionarios_ativos.iterrows():
            emp_id = funcionario['id']
            nome = funcionario['full_name']
            
            print(f"👤 Processando: {nome} (ID: {emp_id})")
            
            for dia in dias_uteis:
                try:
                    # Gerar horários aleatórios
                    entrada_hora, saida_hora = gerar_horarios_turno()
                    
                    # Criar datas
                    data_base = datetime(2024, 8, dia)
                    clock_in = datetime.combine(data_base.date(), 
                                              datetime.strptime(entrada_hora, "%H:%M").time())
                    clock_out = datetime.combine(data_base.date(), 
                                               datetime.strptime(saida_hora, "%H:%M").time())
                    
                    # Adicionar timezone UTC
                    clock_in = clock_in.replace(tzinfo=timezone.utc)
                    clock_out = clock_out.replace(tzinfo=timezone.utc)
                    
                    # Garantir que saída seja após entrada
                    if clock_out <= clock_in:
                        clock_out = clock_in + timedelta(hours=8, minutes=30)
                    
                    # Registrar turno
                    response = sender.register_complete_shift(
                        employee_id=emp_id,
                        clock_in_time=clock_in,
                        clock_out_time=clock_out,
                        observations=f"Turno gerado automaticamente - {data_base.strftime('%d/%m/%Y')}"
                    )
                    
                    sucessos += 1
                    total_turnos += 1
                    
                    print(f"   ✅ {data_base.strftime('%d/%m')}: {entrada_hora} - {saida_hora}")
                    
                    # Pequena pausa para não sobrecarregar a API
                    time.sleep(0.5)
                    
                except Exception as e:
                    erros += 1
                    print(f"   ❌ Erro no dia {dia}: {e}")
                    continue
            
            print(f"   📊 {nome}: {sucessos} turnos registrados")
            print()
        
        print("=" * 50)
        print("📊 RELATÓRIO FINAL:")
        print(f"   • Total de turnos processados: {total_turnos}")
        print(f"   • Sucessos: {sucessos}")
        print(f"   • Erros: {erros}")
        print(f"   • Funcionários processados: {len(funcionarios_ativos)}")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")

def gerar_turnos_para_funcionario_especifico(employee_id, nome):
    """Gera turnos para um funcionário específico"""
    
    print(f"👤 GERANDO TURNOS PARA: {nome} (ID: {employee_id})")
    print("=" * 50)
    
    sender = AttendanceSender()
    
    # Testar conexão
    if not sender.test_connection():
        print("❌ Erro de conexão!")
        return
    
    # Gerar turnos para agosto
    dias_uteis = []
    for dia in range(1, 32):
        data = datetime(2024, 8, dia)
        if data.weekday() < 5:  # Segunda=0, Sexta=4
            dias_uteis.append(dia)
    
    sucessos = 0
    erros = 0
    
    for dia in dias_uteis:
        try:
            # Gerar horários
            entrada_hora, saida_hora = gerar_horarios_turno()
            
            # Criar datas
            data_base = datetime(2024, 8, dia)
            clock_in = datetime.combine(data_base.date(), 
                                      datetime.strptime(entrada_hora, "%H:%M").time())
            clock_out = datetime.combine(data_base.date(), 
                                       datetime.strptime(saida_hora, "%H:%M").time())
            
            # Adicionar timezone
            clock_in = clock_in.replace(tzinfo=timezone.utc)
            clock_out = clock_out.replace(tzinfo=timezone.utc)
            
            if clock_out <= clock_in:
                clock_out = clock_in + timedelta(hours=8, minutes=30)
            
            # Registrar turno
            response = sender.register_complete_shift(
                employee_id=employee_id,
                clock_in_time=clock_in,
                clock_out_time=clock_out,
                observations=f"Turno gerado automaticamente - {data_base.strftime('%d/%m/%Y')}"
            )
            
            sucessos += 1
            print(f"✅ {data_base.strftime('%d/%m')}: {entrada_hora} - {saida_hora}")
            
            time.sleep(0.5)
            
        except Exception as e:
            erros += 1
            print(f"❌ Erro no dia {dia}: {e}")
    
    print(f"\n📊 {nome}: {sucessos} sucessos, {erros} erros")

def main():
    """Função principal"""
    print("🗓️  GERADOR DE TURNOS - AGOSTO 2024")
    print("=" * 50)
    print("Opções:")
    print("1. Gerar turnos para TODOS os funcionários ativos")
    print("2. Gerar turnos para um funcionário específico")
    print("3. Sair")
    
    opcao = input("\nEscolha uma opção (1-3): ").strip()
    
    if opcao == "1":
        confirmar = input("⚠️  ATENÇÃO: Isso vai gerar turnos para TODOS os funcionários ativos. Continuar? (s/N): ")
        if confirmar.lower() in ['s', 'sim', 'y', 'yes']:
            gerar_turnos_agosto()
        else:
            print("❌ Operação cancelada.")
    
    elif opcao == "2":
        try:
            emp_id = int(input("Digite o ID do funcionário: "))
            
            # Buscar nome do funcionário
            df = pd.read_csv("Dados_Coletados/Dados_Brutos/Dados da API/Funcionários/employees_20250912_132435.csv")
            funcionario = df[df['id'] == emp_id]
            
            if funcionario.empty:
                print("❌ Funcionário não encontrado!")
                return
            
            nome = funcionario.iloc[0]['full_name']
            gerar_turnos_para_funcionario_especifico(emp_id, nome)
            
        except ValueError:
            print("❌ ID deve ser um número!")
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    elif opcao == "3":
        print("👋 Até logo!")
    
    else:
        print("❌ Opção inválida!")

if __name__ == "__main__":
    main()
