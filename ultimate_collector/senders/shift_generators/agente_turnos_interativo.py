#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agente Interativo para Inserção de Turnos
Pergunta qual colaborador e para qual mês/ano inserir dados
"""

import sys
import os
import pandas as pd
from datetime import datetime, timezone, timedelta
import random
import time
import calendar

# Adicionar o diretório do projeto ao path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from ..attendance_sender import AttendanceSender

def listar_colaboradores():
    """Lista todos os colaboradores ativos"""
    try:
        df = pd.read_csv("Dados_Coletados/Dados_Brutos/Dados da API/Funcionários/employees_20250912_132435.csv")
        funcionarios_ativos = df[df['active'] == True]
        
        print("👥 COLABORADORES ATIVOS:")
        print("=" * 50)
        
        for idx, funcionario in funcionarios_ativos.iterrows():
            print(f"🟢 ID: {funcionario['id']:6} | {funcionario['full_name']}")
        
        print("=" * 50)
        return funcionarios_ativos
        
    except Exception as e:
        print(f"❌ Erro ao carregar colaboradores: {e}")
        return None

def gerar_horarios_turno():
    """Gera horários realistas de entrada e saída"""
    horarios_entrada = [
        "08:00", "08:15", "08:30", "08:45", "09:00", "09:15"
    ]
    horarios_saida = [
        "17:00", "17:15", "17:30", "17:45", "18:00", "18:15", "18:30"
    ]
    
    entrada = random.choice(horarios_entrada)
    saida = random.choice(horarios_saida)
    
    return entrada, saida

def obter_horarios_do_usuario():
    """Permite ao usuário inserir horários personalizados"""
    print("\n🕐 INSERIR HORÁRIOS PERSONALIZADOS")
    print("=" * 40)
    
    while True:
        try:
            entrada = input("⏰ Insira horário de entrada (HH:MM): ").strip()
            
            # Validar formato
            if not entrada or len(entrada) != 5 or entrada[2] != ':':
                print("❌ Formato inválido! Use HH:MM (ex: 08:30)")
                continue
            
            # Validar hora
            hora, minuto = entrada.split(':')
            hora = int(hora)
            minuto = int(minuto)
            
            if hora < 0 or hora > 23 or minuto < 0 or minuto > 59:
                print("❌ Horário inválido! Hora deve ser 00-23 e minuto 00-59")
                continue
            
            break
            
        except ValueError:
            print("❌ Formato inválido! Use HH:MM (ex: 08:30)")
    
    while True:
        try:
            saida = input("⏰ Insira horário de saída (HH:MM): ").strip()
            
            # Validar formato
            if not saida or len(saida) != 5 or saida[2] != ':':
                print("❌ Formato inválido! Use HH:MM (ex: 17:30)")
                continue
            
            # Validar hora
            hora, minuto = saida.split(':')
            hora = int(hora)
            minuto = int(minuto)
            
            if hora < 0 or hora > 23 or minuto < 0 or minuto > 59:
                print("❌ Horário inválido! Hora deve ser 00-23 e minuto 00-59")
                continue
            
            # Validar que saída é após entrada
            entrada_dt = datetime.strptime(entrada, "%H:%M")
            saida_dt = datetime.strptime(saida, "%H:%M")
            
            if saida_dt <= entrada_dt:
                print("❌ Horário de saída deve ser posterior ao de entrada!")
                continue
            
            break
            
        except ValueError:
            print("❌ Formato inválido! Use HH:MM (ex: 17:30)")
    
    print(f"✅ Horários definidos: {entrada} - {saida}")
    return entrada, saida

def verificar_turnos_existentes(sender, employee_id, data):
    """Verifica se já existem turnos para o funcionário na data"""
    try:
        # Buscar turnos especificamente para a data
        response = sender.get_employee_shifts(employee_id, data.strftime("%Y-%m-%d"))
        
        if 'data' in response and response['data']:
            turnos_na_data = [t for t in response['data'] if t.get('date') == data.strftime("%Y-%m-%d")]
            return len(turnos_na_data) > 0
        
        return False
    except Exception as e:
        print(f"   ⚠️  Erro ao verificar turnos existentes: {e}")
        return False

def obter_dias_uteis(ano, mes):
    """Obtém os dias úteis de um mês específico"""
    dias_uteis = []
    
    # Obter o último dia do mês
    ultimo_dia = calendar.monthrange(ano, mes)[1]
    
    for dia in range(1, ultimo_dia + 1):
        data = datetime(ano, mes, dia)
        if data.weekday() < 5:  # Segunda=0, Sexta=4
            dias_uteis.append(dia)
    
    return dias_uteis

def gerar_turnos_para_colaborador(employee_id, nome, ano, mes, usar_horarios_personalizados=False):
    """Gera turnos para um colaborador específico em um mês/ano"""
    
    print(f"\n👤 GERANDO TURNOS PARA: {nome} (ID: {employee_id})")
    print(f"📅 Mês/Ano: {mes:02d}/{ano}")
    print("=" * 60)
    
    sender = AttendanceSender()
    
    # Testar conexão
    if not sender.test_connection():
        print("❌ Erro de conexão!")
        return
    
    # Obter dias úteis do mês
    dias_uteis = obter_dias_uteis(ano, mes)
    
    print(f"📅 Dias úteis encontrados: {len(dias_uteis)}")
    print(f"   Dias: {dias_uteis}")
    print()
    
    # Obter horários personalizados se solicitado
    entrada_hora_personalizada = None
    saida_hora_personalizada = None
    
    if usar_horarios_personalizados:
        entrada_hora_personalizada, saida_hora_personalizada = obter_horarios_do_usuario()
    
    sucessos = 0
    erros = 0
    turnos_existentes = 0
    
    for dia in dias_uteis:
        try:
            data_base = datetime(ano, mes, dia)
            
            # Forçar inserção mesmo se já existir turno
            # (comentado para forçar inserção)
            # if verificar_turnos_existentes(sender, employee_id, data_base):
            #     print(f"⏭️  {data_base.strftime('%d/%m')}: Turno já existe, pulando...")
            #     turnos_existentes += 1
            #     continue
            
            # Usar horários personalizados ou gerar aleatórios
            if usar_horarios_personalizados:
                entrada_hora = entrada_hora_personalizada
                saida_hora = saida_hora_personalizada
            else:
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

def gerar_turnos_para_todos(ano, mes):
    """Gera turnos para todos os colaboradores ativos em um mês/ano"""
    
    print(f"\n👥 GERANDO TURNOS PARA TODOS OS COLABORADORES")
    print(f"📅 Mês/Ano: {mes:02d}/{ano}")
    print("=" * 60)
    
    # Carregar colaboradores
    funcionarios_ativos = listar_colaboradores()
    if funcionarios_ativos is None:
        return
    
    # Criar instância do sender
    sender = AttendanceSender()
    
    # Testar conexão
    if not sender.test_connection():
        print("❌ Erro de conexão!")
        return
    
    # Obter dias úteis do mês
    dias_uteis = obter_dias_uteis(ano, mes)
    
    print(f"📅 Dias úteis encontrados: {len(dias_uteis)}")
    print(f"👥 Colaboradores ativos: {len(funcionarios_ativos)}")
    print()
    
    total_turnos = 0
    total_sucessos = 0
    total_erros = 0
    total_existentes = 0
    
    for idx, funcionario in funcionarios_ativos.iterrows():
        emp_id = funcionario['id']
        nome = funcionario['full_name']
        
        print(f"👤 Processando: {nome} (ID: {emp_id})")
        
        sucessos = 0
        erros = 0
        existentes = 0
        
        for dia in dias_uteis:
            try:
                data_base = datetime(ano, mes, dia)
                
                # Forçar inserção mesmo se já existir turno
                # (comentado para forçar inserção)
                # if verificar_turnos_existentes(sender, emp_id, data_base):
                #     existentes += 1
                #     continue
                
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
                    employee_id=emp_id,
                    clock_in_time=clock_in,
                    clock_out_time=clock_out,
                    observations=f"Turno gerado automaticamente - {data_base.strftime('%d/%m/%Y')}"
                )
                
                sucessos += 1
                print(f"   ✅ {data_base.strftime('%d/%m')}: {entrada_hora} - {saida_hora}")
                
                time.sleep(0.3)
                
            except Exception as e:
                erros += 1
                print(f"   ❌ Erro no dia {dia}: {e}")
        
        print(f"   📊 {nome}: {sucessos} sucessos, {erros} erros, {existentes} já existiam")
        print()
        
        total_sucessos += sucessos
        total_erros += erros
        total_existentes += existentes
        total_turnos += sucessos + erros + existentes
    
    print("=" * 60)
    print("📊 RELATÓRIO FINAL:")
    print(f"   • Total de turnos processados: {total_turnos}")
    print(f"   • Sucessos: {total_sucessos}")
    print(f"   • Erros: {total_erros}")
    print(f"   • Turnos já existentes (pulados): {total_existentes}")
    print(f"   • Colaboradores processados: {len(funcionarios_ativos)}")
    print("=" * 60)

def gerar_turnos_para_todos_personalizados(ano, mes):
    """Gera turnos para todos os colaboradores ativos com horários personalizados"""
    
    print(f"\n👥 GERANDO TURNOS PARA TODOS OS COLABORADORES (HORÁRIOS PERSONALIZADOS)")
    print(f"📅 Mês/Ano: {mes:02d}/{ano}")
    print("=" * 60)
    
    # Obter horários personalizados
    entrada_hora, saida_hora = obter_horarios_do_usuario()
    
    # Carregar colaboradores
    funcionarios_ativos = listar_colaboradores()
    if funcionarios_ativos is None:
        return
    
    # Criar instância do sender
    sender = AttendanceSender()
    
    # Testar conexão
    if not sender.test_connection():
        print("❌ Erro de conexão!")
        return
    
    # Obter dias úteis do mês
    dias_uteis = obter_dias_uteis(ano, mes)
    
    print(f"📅 Dias úteis encontrados: {len(dias_uteis)}")
    print(f"👥 Colaboradores ativos: {len(funcionarios_ativos)}")
    print(f"🕐 Horários definidos: {entrada_hora} - {saida_hora}")
    print()
    
    total_turnos = 0
    total_sucessos = 0
    total_erros = 0
    total_existentes = 0
    
    for idx, funcionario in funcionarios_ativos.iterrows():
        emp_id = funcionario['id']
        nome = funcionario['full_name']
        
        print(f"👤 Processando: {nome} (ID: {emp_id})")
        
        sucessos = 0
        erros = 0
        existentes = 0
        
        for dia in dias_uteis:
            try:
                data_base = datetime(ano, mes, dia)
                
                # Forçar inserção mesmo se já existir turno
                # (comentado para forçar inserção)
                # if verificar_turnos_existentes(sender, emp_id, data_base):
                #     existentes += 1
                #     continue
                
                # Criar datas com horários personalizados
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
                    employee_id=emp_id,
                    clock_in_time=clock_in,
                    clock_out_time=clock_out,
                    observations=f"Turno gerado automaticamente - {data_base.strftime('%d/%m/%Y')}"
                )
                
                sucessos += 1
                print(f"   ✅ {data_base.strftime('%d/%m')}: {entrada_hora} - {saida_hora}")
                
                time.sleep(0.3)
                
            except Exception as e:
                erros += 1
                print(f"   ❌ Erro no dia {dia}: {e}")
        
        print(f"   📊 {nome}: {sucessos} sucessos, {erros} erros, {existentes} já existiam")
        print()
        
        total_sucessos += sucessos
        total_erros += erros
        total_existentes += existentes
        total_turnos += sucessos + erros + existentes
    
    print("=" * 60)
    print("📊 RELATÓRIO FINAL:")
    print(f"   • Total de turnos processados: {total_turnos}")
    print(f"   • Sucessos: {total_sucessos}")
    print(f"   • Erros: {total_erros}")
    print(f"   • Turnos já existentes (pulados): {total_existentes}")
    print(f"   • Colaboradores processados: {len(funcionarios_ativos)}")
    print(f"   • Horários utilizados: {entrada_hora} - {saida_hora}")
    print("=" * 60)

def main():
    """Função principal - Agente Interativo"""
    
    print("🤖 AGENTE INTERATIVO PARA INSERÇÃO DE TURNOS")
    print("=" * 60)
    
    while True:
        print("\n📋 MENU PRINCIPAL:")
        print("1. Listar colaboradores ativos")
        print("2. Gerar turnos para UM colaborador (horários aleatórios)")
        print("3. Gerar turnos para UM colaborador (horários personalizados)")
        print("4. Gerar turnos para TODOS os colaboradores (horários aleatórios)")
        print("5. Gerar turnos para TODOS os colaboradores (horários personalizados)")
        print("6. Sair")
        
        opcao = input("\nEscolha uma opção (1-6): ").strip()
        
        if opcao == "1":
            listar_colaboradores()
        
        elif opcao == "2":
            # Gerar turnos para UM colaborador (horários aleatórios)
            funcionarios = listar_colaboradores()
            if funcionarios is None:
                continue
            
            try:
                employee_id = int(input("\n🔍 Qual ID do colaborador? "))
                funcionario = funcionarios[funcionarios['id'] == employee_id]
                if funcionario.empty:
                    print("❌ Colaborador não encontrado!")
                    continue
                
                nome = funcionario.iloc[0]['full_name']
                print(f"✅ Colaborador encontrado: {nome}")
                
                ano = int(input("📅 Qual ano? (ex: 2024): "))
                mes = int(input("📅 Qual mês? (1-12): "))
                
                if mes < 1 or mes > 12:
                    print("❌ Mês inválido! Use 1-12")
                    continue
                
                confirmar = input(f"\n⚠️  Gerar turnos ALEATÓRIOS para {nome} em {mes:02d}/{ano}? (s/N): ")
                if confirmar.lower() in ['s', 'sim', 'y', 'yes']:
                    gerar_turnos_para_colaborador(employee_id, nome, ano, mes, usar_horarios_personalizados=False)
                else:
                    print("❌ Operação cancelada.")
                
            except ValueError:
                print("❌ ID deve ser um número!")
            except Exception as e:
                print(f"❌ Erro: {e}")
        
        elif opcao == "3":
            # Gerar turnos para UM colaborador (horários personalizados)
            funcionarios = listar_colaboradores()
            if funcionarios is None:
                continue
            
            try:
                employee_id = int(input("\n🔍 Qual ID do colaborador? "))
                funcionario = funcionarios[funcionarios['id'] == employee_id]
                if funcionario.empty:
                    print("❌ Colaborador não encontrado!")
                    continue
                
                nome = funcionario.iloc[0]['full_name']
                print(f"✅ Colaborador encontrado: {nome}")
                
                ano = int(input("📅 Qual ano? (ex: 2024): "))
                mes = int(input("📅 Qual mês? (1-12): "))
                
                if mes < 1 or mes > 12:
                    print("❌ Mês inválido! Use 1-12")
                    continue
                
                confirmar = input(f"\n⚠️  Gerar turnos com HORÁRIOS PERSONALIZADOS para {nome} em {mes:02d}/{ano}? (s/N): ")
                if confirmar.lower() in ['s', 'sim', 'y', 'yes']:
                    gerar_turnos_para_colaborador(employee_id, nome, ano, mes, usar_horarios_personalizados=True)
                else:
                    print("❌ Operação cancelada.")
                
            except ValueError:
                print("❌ ID deve ser um número!")
            except Exception as e:
                print(f"❌ Erro: {e}")
        
        elif opcao == "4":
            # Gerar turnos para TODOS os colaboradores (horários aleatórios)
            try:
                ano = int(input("📅 Qual ano? (ex: 2024): "))
                mes = int(input("📅 Qual mês? (1-12): "))
                
                if mes < 1 or mes > 12:
                    print("❌ Mês inválido! Use 1-12")
                    continue
                
                confirmar = input(f"\n⚠️  Gerar turnos ALEATÓRIOS para TODOS os colaboradores em {mes:02d}/{ano}? (s/N): ")
                if confirmar.lower() in ['s', 'sim', 'y', 'yes']:
                    gerar_turnos_para_todos(ano, mes)
                else:
                    print("❌ Operação cancelada.")
                
            except ValueError:
                print("❌ Ano e mês devem ser números!")
            except Exception as e:
                print(f"❌ Erro: {e}")
        
        elif opcao == "5":
            # Gerar turnos para TODOS os colaboradores (horários personalizados)
            try:
                ano = int(input("📅 Qual ano? (ex: 2024): "))
                mes = int(input("📅 Qual mês? (1-12): "))
                
                if mes < 1 or mes > 12:
                    print("❌ Mês inválido! Use 1-12")
                    continue
                
                print("\n⚠️  ATENÇÃO: Esta opção irá usar os MESMOS horários para TODOS os colaboradores!")
                confirmar = input(f"Gerar turnos com HORÁRIOS PERSONALIZADOS para TODOS em {mes:02d}/{ano}? (s/N): ")
                if confirmar.lower() in ['s', 'sim', 'y', 'yes']:
                    gerar_turnos_para_todos_personalizados(ano, mes)
                else:
                    print("❌ Operação cancelada.")
                
            except ValueError:
                print("❌ Ano e mês devem ser números!")
            except Exception as e:
                print(f"❌ Erro: {e}")
        
        elif opcao == "6":
            print("👋 Até logo!")
            break
        
        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    main()
