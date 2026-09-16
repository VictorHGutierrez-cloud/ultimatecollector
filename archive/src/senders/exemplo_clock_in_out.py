#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo prático de como usar o sistema de clock in/clock out
"""

import sys
import os
from datetime import datetime, timezone

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from senders.attendance_sender import AttendanceSender

def exemplo_clock_in_simples():
    """Exemplo 1: Clock in simples"""
    print("=" * 60)
    print("EXEMPLO 1: CLOCK IN SIMPLES")
    print("=" * 60)
    
    # Criar instância do sender
    sender = AttendanceSender()
    
    try:
        # Dados do funcionário (substitua pelo ID real)
        employee_id = 1
        
        print(f"🕐 Registrando CLOCK IN para funcionário {employee_id}")
        print(f"   Horário: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        # Registrar clock in
        response = sender.clock_in(
            employee_id=employee_id,
            observations="Entrada registrada via sistema Python"
        )
        
        print("✅ CLOCK IN registrado com sucesso!")
        print(f"   Resposta da API: {response}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

def exemplo_clock_out_simples():
    """Exemplo 2: Clock out simples"""
    print("\n" + "=" * 60)
    print("EXEMPLO 2: CLOCK OUT SIMPLES")
    print("=" * 60)
    
    sender = AttendanceSender()
    
    try:
        employee_id = 1
        
        print(f"🕐 Registrando CLOCK OUT para funcionário {employee_id}")
        print(f"   Horário: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        # Registrar clock out
        response = sender.clock_out(
            employee_id=employee_id,
            observations="Saída registrada via sistema Python"
        )
        
        print("✅ CLOCK OUT registrado com sucesso!")
        print(f"   Resposta da API: {response}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

def exemplo_turno_completo():
    """Exemplo 3: Turno completo (entrada + saída de uma vez)"""
    print("\n" + "=" * 60)
    print("EXEMPLO 3: TURNO COMPLETO")
    print("=" * 60)
    
    sender = AttendanceSender()
    
    try:
        employee_id = 1
        
        # Definir horários do turno
        clock_in_time = datetime(2024, 1, 15, 8, 0, 0, tzinfo=timezone.utc)
        clock_out_time = datetime(2024, 1, 15, 17, 0, 0, tzinfo=timezone.utc)
        
        print(f"🕐 Registrando TURNO COMPLETO para funcionário {employee_id}")
        print(f"   Entrada: {clock_in_time.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"   Saída: {clock_out_time.strftime('%d/%m/%Y %H:%M:%S')}")
        
        # Registrar turno completo
        response = sender.register_complete_shift(
            employee_id=employee_id,
            clock_in_time=clock_in_time,
            clock_out_time=clock_out_time,
            observations="Turno completo registrado via sistema Python"
        )
        
        print("✅ TURNO COMPLETO registrado com sucesso!")
        print(f"   Resposta da API: {response}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

def exemplo_com_localizacao():
    """Exemplo 4: Clock in/out com localização geográfica"""
    print("\n" + "=" * 60)
    print("EXEMPLO 4: COM LOCALIZAÇÃO GEOGRÁFICA")
    print("=" * 60)
    
    sender = AttendanceSender()
    
    try:
        employee_id = 1
        
        # Coordenadas de São Paulo (exemplo)
        latitude = -23.5505
        longitude = -46.6333
        
        print(f"🕐 Registrando CLOCK IN com localização para funcionário {employee_id}")
        print(f"   Horário: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"   Localização: {latitude}, {longitude} (São Paulo)")
        
        # Registrar clock in com localização
        response = sender.clock_in(
            employee_id=employee_id,
            latitude=latitude,
            longitude=longitude,
            observations="Entrada com localização GPS"
        )
        
        print("✅ CLOCK IN com localização registrado com sucesso!")
        print(f"   Resposta da API: {response}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

def exemplo_verificar_turnos():
    """Exemplo 5: Verificar turnos de um funcionário"""
    print("\n" + "=" * 60)
    print("EXEMPLO 5: VERIFICAR TURNOS DO FUNCIONÁRIO")
    print("=" * 60)
    
    sender = AttendanceSender()
    
    try:
        employee_id = 1
        
        print(f"📋 Buscando turnos do funcionário {employee_id}")
        
        # Buscar turnos
        response = sender.get_employee_shifts(employee_id)
        
        if 'data' in response and response['data']:
            print(f"✅ Encontrados {len(response['data'])} turno(s):")
            print("-" * 50)
            
            for i, shift in enumerate(response['data'], 1):
                print(f"Turno {i}:")
                print(f"  ID: {shift.get('id', 'N/A')}")
                print(f"  Data: {shift.get('date', 'N/A')}")
                print(f"  Clock In: {shift.get('clock_in', 'N/A')}")
                print(f"  Clock Out: {shift.get('clock_out', 'N/A')}")
                print(f"  Status: {shift.get('status', 'N/A')}")
                print("-" * 30)
        else:
            print("ℹ️  Nenhum turno encontrado para este funcionário.")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

def exemplo_validar_funcionario():
    """Exemplo 6: Validar se funcionário existe"""
    print("\n" + "=" * 60)
    print("EXEMPLO 6: VALIDAR FUNCIONÁRIO")
    print("=" * 60)
    
    sender = AttendanceSender()
    
    try:
        # Testar com diferentes IDs
        employee_ids = [1, 999, 2]
        
        for employee_id in employee_ids:
            print(f"🔍 Verificando funcionário {employee_id}...")
            
            if sender.validate_employee_id(employee_id):
                print(f"✅ Funcionário {employee_id} existe na API")
            else:
                print(f"❌ Funcionário {employee_id} NÃO existe na API")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

def main():
    """Função principal que executa todos os exemplos"""
    print("🕐 EXEMPLOS DE USO - CLOCK IN/OUT FACTORIAL API")
    print("=" * 60)
    
    # Verificar conexão primeiro
    sender = AttendanceSender()
    print("🔌 Testando conexão com a API...")
    
    if not sender.test_connection():
        print("❌ ERRO: Não foi possível conectar à API Factorial!")
        print("   Verifique suas configurações em config_factorial.env")
        print("   - API_KEY está correta?")
        print("   - BASE_URL está correta?")
        print("   - Internet está funcionando?")
        return
    
    print("✅ Conexão estabelecida com sucesso!")
    print()
    
    # Executar exemplos
    try:
        exemplo_clock_in_simples()
        exemplo_clock_out_simples()
        exemplo_turno_completo()
        exemplo_com_localizacao()
        exemplo_verificar_turnos()
        exemplo_validar_funcionario()
        
        print("\n" + "=" * 60)
        print("✅ TODOS OS EXEMPLOS EXECUTADOS!")
        print("=" * 60)
        print()
        print("📝 COMO USAR EM SEU CÓDIGO:")
        print("-" * 30)
        print("1. Importe a classe: from senders.attendance_sender import AttendanceSender")
        print("2. Crie uma instância: sender = AttendanceSender()")
        print("3. Use os métodos:")
        print("   - sender.clock_in(employee_id)")
        print("   - sender.clock_out(employee_id)")
        print("   - sender.register_complete_shift(employee_id, clock_in_time, clock_out_time)")
        print("   - sender.get_employee_shifts(employee_id)")
        print("   - sender.validate_employee_id(employee_id)")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Execução interrompida pelo usuário")
    except Exception as e:
        print(f"\n\n❌ Erro geral: {e}")

if __name__ == "__main__":
    main()
