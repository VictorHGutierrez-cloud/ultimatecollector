#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface simples para registro de clock in/clock out
"""

import sys
import os
from datetime import datetime, timezone
from typing import Optional

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from senders.attendance_sender import AttendanceSender

class ClockInterface:
    """Interface simples para registro de presença"""
    
    def __init__(self):
        """Inicializa a interface"""
        self.sender = AttendanceSender()
        
    def clock_in(self, employee_id: int, 
                 latitude: Optional[float] = None,
                 longitude: Optional[float] = None,
                 observations: Optional[str] = None) -> bool:
        """
        Registra clock in de um funcionário
        
        Args:
            employee_id: ID do funcionário
            latitude: Latitude (opcional)
            longitude: Longitude (opcional)
            observations: Observações (opcional)
            
        Returns:
            True se sucesso, False se erro
        """
        try:
            print(f"🕐 Registrando CLOCK IN para funcionário {employee_id}...")
            
            # Validar se funcionário existe
            if not self.sender.validate_employee_id(employee_id):
                print(f"❌ Erro: Funcionário {employee_id} não encontrado!")
                return False
            
            # Registrar clock in
            response = self.sender.clock_in(
                employee_id=employee_id,
                latitude=latitude,
                longitude=longitude,
                observations=observations
            )
            
            print(f"✅ CLOCK IN registrado com sucesso!")
            print(f"   Funcionário: {employee_id}")
            print(f"   Horário: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            
            if latitude and longitude:
                print(f"   Localização: {latitude}, {longitude}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao registrar CLOCK IN: {e}")
            return False
    
    def clock_out(self, employee_id: int,
                  latitude: Optional[float] = None,
                  longitude: Optional[float] = None,
                  observations: Optional[str] = None) -> bool:
        """
        Registra clock out de um funcionário
        
        Args:
            employee_id: ID do funcionário
            latitude: Latitude (opcional)
            longitude: Longitude (opcional)
            observations: Observações (opcional)
            
        Returns:
            True se sucesso, False se erro
        """
        try:
            print(f"🕐 Registrando CLOCK OUT para funcionário {employee_id}...")
            
            # Validar se funcionário existe
            if not self.sender.validate_employee_id(employee_id):
                print(f"❌ Erro: Funcionário {employee_id} não encontrado!")
                return False
            
            # Registrar clock out
            response = self.sender.clock_out(
                employee_id=employee_id,
                latitude=latitude,
                longitude=longitude,
                observations=observations
            )
            
            print(f"✅ CLOCK OUT registrado com sucesso!")
            print(f"   Funcionário: {employee_id}")
            print(f"   Horário: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            
            if latitude and longitude:
                print(f"   Localização: {latitude}, {longitude}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao registrar CLOCK OUT: {e}")
            return False
    
    def register_shift(self, employee_id: int,
                       clock_in_time: str,
                       clock_out_time: str,
                       latitude: Optional[float] = None,
                       longitude: Optional[float] = None,
                       observations: Optional[str] = None) -> bool:
        """
        Registra um turno completo
        
        Args:
            employee_id: ID do funcionário
            clock_in_time: Horário de entrada (formato: YYYY-MM-DD HH:MM:SS)
            clock_out_time: Horário de saída (formato: YYYY-MM-DD HH:MM:SS)
            latitude: Latitude (opcional)
            longitude: Longitude (opcional)
            observations: Observações (opcional)
            
        Returns:
            True se sucesso, False se erro
        """
        try:
            print(f"🕐 Registrando TURNO COMPLETO para funcionário {employee_id}...")
            
            # Converter strings para datetime
            clock_in_dt = datetime.strptime(clock_in_time, "%Y-%m-%d %H:%M:%S")
            clock_out_dt = datetime.strptime(clock_out_time, "%Y-%m-%d %H:%M:%S")
            
            # Adicionar timezone UTC
            clock_in_dt = clock_in_dt.replace(tzinfo=timezone.utc)
            clock_out_dt = clock_out_dt.replace(tzinfo=timezone.utc)
            
            # Validar se funcionário existe
            if not self.sender.validate_employee_id(employee_id):
                print(f"❌ Erro: Funcionário {employee_id} não encontrado!")
                return False
            
            # Registrar turno completo
            response = self.sender.register_complete_shift(
                employee_id=employee_id,
                clock_in_time=clock_in_dt,
                clock_out_time=clock_out_dt,
                latitude=latitude,
                longitude=longitude,
                observations=observations
            )
            
            print(f"✅ TURNO COMPLETO registrado com sucesso!")
            print(f"   Funcionário: {employee_id}")
            print(f"   Entrada: {clock_in_time}")
            print(f"   Saída: {clock_out_time}")
            
            if latitude and longitude:
                print(f"   Localização: {latitude}, {longitude}")
            
            return True
            
        except ValueError as e:
            print(f"❌ Erro de formato de data: {e}")
            print("   Use o formato: YYYY-MM-DD HH:MM:SS")
            return False
        except Exception as e:
            print(f"❌ Erro ao registrar turno: {e}")
            return False
    
    def show_employee_shifts(self, employee_id: int, date: Optional[str] = None):
        """
        Mostra os turnos de um funcionário
        
        Args:
            employee_id: ID do funcionário
            date: Data no formato YYYY-MM-DD (opcional)
        """
        try:
            print(f"📋 Buscando turnos do funcionário {employee_id}...")
            
            response = self.sender.get_employee_shifts(employee_id, date)
            
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
            print(f"❌ Erro ao buscar turnos: {e}")

def main():
    """Função principal para demonstração"""
    print("🕐 INTERFACE DE CLOCK IN/OUT - FACTORIAL API")
    print("=" * 50)
    
    # Testar conexão
    sender = AttendanceSender()
    if not sender.test_connection():
        print("❌ Erro: Não foi possível conectar à API Factorial!")
        print("   Verifique suas configurações em config_factorial.env")
        return
    
    print("✅ Conexão com API estabelecida!")
    print()
    
    # Exemplo de uso
    interface = ClockInterface()
    
    # Exemplo 1: Clock in simples
    print("EXEMPLO 1: Clock In Simples")
    print("-" * 30)
    interface.clock_in(employee_id=1, observations="Entrada via sistema")
    print()
    
    # Exemplo 2: Clock out simples
    print("EXEMPLO 2: Clock Out Simples")
    print("-" * 30)
    interface.clock_out(employee_id=1, observations="Saída via sistema")
    print()
    
    # Exemplo 3: Turno completo
    print("EXEMPLO 3: Turno Completo")
    print("-" * 30)
    interface.register_shift(
        employee_id=1,
        clock_in_time="2024-01-15 08:00:00",
        clock_out_time="2024-01-15 17:00:00",
        observations="Turno completo via sistema"
    )
    print()
    
    # Exemplo 4: Ver turnos
    print("EXEMPLO 4: Ver Turnos do Funcionário")
    print("-" * 30)
    interface.show_employee_shifts(employee_id=1)

if __name__ == "__main__":
    main()
