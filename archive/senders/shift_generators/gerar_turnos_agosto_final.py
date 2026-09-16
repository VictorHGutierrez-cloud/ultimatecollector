#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script FINAL para gerar turnos de agosto - com verificação de conflitos
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

def verificar_turnos_existentes(sender, employee_id, data):
    """Verifica se já existem turnos para o funcionário na data"""
    try:
        response = sender.get_employee_shifts(employee_id, data.strftime("%Y-%m-%d"))
        
        if 'data' in response and response['data']:
            # Verificar se há turnos na data específica
            turnos_na_data = [t for t in response['data'] if t.get('date') == data.strftime("%Y-%m-%d")]
            return len(turnos_na_data) > 0
        
        return False
    except Exception as e:
        print(f"   ⚠️  Erro ao verificar turnos existentes: {e}")
        return False

def gerar_turnos_agosto():
    """Gera turnos para todos os funcionários ativos em agosto"""
    
    print("🗓️  GERADOR DE TURNOS - AGOSTO 2024 (FINAL)")
    print("=" * 60)
    
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
        turnos_existentes = 0
        
        for idx, funcionario in funcionarios_ativos.iterrows():
            emp_id = funcionario['id']
            nome = funcionario['full_name']
            
            print(f"👤 Processando: {nome} (ID: {emp_id})")
            
            for dia in dias_uteis:
                try:
                    data_base = datetime(2024, 8, dia)
                    
                    # Verificar se já existe turno para este funcionário nesta data
                    if verificar_turnos_existentes(sender, emp_id, data_base):
                        print(f"   ⏭️  {data_base.strftime('%d/%m')}: Turno já existe, pulando...")
                        turnos_existentes += 1
                        continue
                    
                    # Gerar horários aleatórios
                    entrada_hora, saida_hora = gerar_horarios_turno()
                    
                    # Criar datas
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
                    time.sleep(0.3)
                    
                except Exception as e:
                    erros += 1
                    print(f"   ❌ Erro no dia {dia}: {e}")
                    continue
            
            print(f"   📊 {nome}: {sucessos} turnos registrados, {turnos_existentes} já existiam")
            print()
        
        print("=" * 60)
        print("📊 RELATÓRIO FINAL:")
        print(f"   • Total de turnos processados: {total_turnos}")
        print(f"   • Sucessos: {sucessos}")
        print(f"   • Erros: {erros}")
        print(f"   • Turnos já existentes (pulados): {turnos_existentes}")
        print(f"   • Funcionários processados: {len(funcionarios_ativos)}")
        print("=" * 60)
        
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
    turnos_existentes = 0
    
    for dia in dias_uteis:
        try:
            data_base = datetime(2024, 8, dia)
            
            # Verificar se já existe turno
            if verificar_turnos_existentes(sender, employee_id, data_base):
                print(f"⏭️  {data_base.strftime('%d/%m')}: Turno já existe, pulando...")
                turnos_existentes += 1
                continue
            
            # Gerar horários
            entrada_hora, saida_hora = gerar_horarios_turno()
            
            # Criar datas
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
            
            time.sleep(0.3)
            
        except Exception as e:
            erros += 1
            print(f"❌ Erro no dia {dia}: {e}")
    
    print(f"\n📊 {nome}: {sucessos} sucessos, {erros} erros, {turnos_existentes} já existiam")

def testar_turno_unico():
    """Testa um turno único para verificar se está funcionando"""
    print("🧪 TESTE: Turno único")
    print("-" * 30)
    
    sender = AttendanceSender()
    
    try:
        # Testar com uma data que não tem conflito (16/08/2024)
        clock_in = datetime(2024, 8, 16, 8, 0, 0, tzinfo=timezone.utc)
        clock_out = datetime(2024, 8, 16, 17, 0, 0, tzinfo=timezone.utc)
        
        response = sender.register_complete_shift(
            employee_id=270284,
            clock_in_time=clock_in,
            clock_out_time=clock_out,
            observations="Teste de turno único"
        )
        
        print("✅ Turno único funcionou!")
        print(f"Resposta: {response}")
        
    except Exception as e:
        print(f"❌ Erro no turno único: {e}")

def main():
    """Função principal"""
    print("🗓️  GERADOR DE TURNOS - AGOSTO 2024 (FINAL)")
    print("=" * 60)
    print("Opções:")
    print("1. Testar turno único")
    print("2. Gerar turnos para TODOS os funcionários ativos")
    print("3. Gerar turnos para um funcionário específico")
    print("4. Sair")
    
    opcao = input("\nEscolha uma opção (1-4): ").strip()
    
    if opcao == "1":
        testar_turno_unico()
    
    elif opcao == "2":
        confirmar = input("⚠️  ATENÇÃO: Isso vai gerar turnos para TODOS os funcionários ativos. Continuar? (s/N): ")
        if confirmar.lower() in ['s', 'sim', 'y', 'yes']:
            gerar_turnos_agosto()
        else:
            print("❌ Operação cancelada.")
    
    elif opcao == "3":
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
    
    elif opcao == "4":
        print("👋 Até logo!")
    
    else:
        print("❌ Opção inválida!")

if __name__ == "__main__":
    main()
