#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para debugar a verificação de turnos existentes
"""

import sys
import os
from datetime import datetime

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ultimate_collector.senders.attendance_sender import AttendanceSender

def debug_verificacao_turnos():
    """Debuga a verificação de turnos existentes"""
    
    print("🔍 DEBUGANDO VERIFICAÇÃO DE TURNOS EXISTENTES")
    print("=" * 60)
    
    sender = AttendanceSender()
    
    # Testar com Alice Anderson (ID: 270105)
    employee_id = 270105
    data_teste = datetime(2024, 8, 27)  # 27/08/2024
    
    print(f"👤 Funcionário: Alice Anderson (ID: {employee_id})")
    print(f"📅 Data de teste: {data_teste.strftime('%d/%m/%Y')}")
    print()
    
    try:
        # Buscar todos os turnos do funcionário
        print("1️⃣ Buscando todos os turnos do funcionário...")
        response = sender.get_employee_shifts(employee_id)
        
        if 'data' in response and response['data']:
            turnos = response['data']
            print(f"   ✅ Encontrados {len(turnos)} turnos")
            
            # Filtrar turnos da data específica
            data_str = data_teste.strftime('%Y-%m-%d')
            print(f"2️⃣ Filtrando turnos para a data: {data_str}")
            
            turnos_na_data = [t for t in turnos if t.get('date') == data_str]
            print(f"   📊 Turnos encontrados na data: {len(turnos_na_data)}")
            
            if turnos_na_data:
                print("   📅 Turnos na data:")
                for i, turno in enumerate(turnos_na_data, 1):
                    print(f"      {i}. ID: {turno.get('id')}")
                    print(f"         Data: {turno.get('date')}")
                    print(f"         Entrada: {turno.get('clock_in')}")
                    print(f"         Saída: {turno.get('clock_out')}")
                    print(f"         Fonte: {turno.get('in_source')}")
                    print()
            else:
                print("   ❌ Nenhum turno encontrado na data")
            
            # Testar a função de verificação
            print("3️⃣ Testando função de verificação...")
            existe = verificar_turnos_existentes_debug(sender, employee_id, data_teste)
            print(f"   Resultado: {existe}")
            
            if existe:
                print("   ⚠️  A função está retornando que EXISTE turno")
            else:
                print("   ✅ A função está retornando que NÃO EXISTE turno")
        
        else:
            print("   ❌ Nenhum turno encontrado")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

def verificar_turnos_existentes_debug(sender, employee_id, data):
    """Versão debug da função de verificação"""
    try:
        print(f"   🔍 Verificando turnos para ID {employee_id} na data {data.strftime('%Y-%m-%d')}")
        
        response = sender.get_employee_shifts(employee_id)
        print(f"   📊 Resposta da API: {len(response.get('data', []))} turnos")
        
        if 'data' in response and response['data']:
            data_str = data.strftime('%Y-%m-%d')
            print(f"   📅 Buscando data: {data_str}")
            
            turnos_na_data = [t for t in response['data'] if t.get('date') == data_str]
            print(f"   📊 Turnos encontrados na data: {len(turnos_na_data)}")
            
            if turnos_na_data:
                print(f"   ✅ Encontrados {len(turnos_na_data)} turnos na data")
                for turno in turnos_na_data:
                    print(f"      - ID: {turno.get('id')}, Entrada: {turno.get('clock_in')}, Saída: {turno.get('clock_out')}")
                return True
            else:
                print(f"   ❌ Nenhum turno encontrado na data {data_str}")
                return False
        
        print(f"   ❌ Nenhum dado na resposta da API")
        return False
        
    except Exception as e:
        print(f"   ❌ Erro na verificação: {e}")
        return False

def testar_diferentes_datas():
    """Testa diferentes datas para ver o comportamento"""
    
    print("\n🧪 TESTANDO DIFERENTES DATAS")
    print("=" * 60)
    
    sender = AttendanceSender()
    employee_id = 270105
    
    # Testar várias datas
    datas_teste = [
        datetime(2024, 8, 27),  # 27/08/2024 (deveria ter turno)
        datetime(2024, 8, 28),  # 28/08/2024 (deveria ter turno)
        datetime(2024, 8, 29),  # 29/08/2024 (deveria ter turno)
        datetime(2024, 9, 1),   # 01/09/2024 (não deveria ter turno)
        datetime(2024, 9, 2),   # 02/09/2024 (não deveria ter turno)
    ]
    
    for data in datas_teste:
        print(f"\n📅 Testando data: {data.strftime('%d/%m/%Y')}")
        existe = verificar_turnos_existentes_debug(sender, employee_id, data)
        print(f"   Resultado: {'EXISTE' if existe else 'NÃO EXISTE'}")

if __name__ == "__main__":
    debug_verificacao_turnos()
    testar_diferentes_datas()
