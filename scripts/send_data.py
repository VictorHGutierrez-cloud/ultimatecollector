#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📤 SEND ONCE - Envio único
Executa um envio único baseado nas configurações do .env
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz do projeto ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from ultimate_collector.core.config import Config
from ultimate_collector.senders.attendance_sender import AttendanceSender

def main():
    print("📤 ENVIO ÚNICO - Ultimate Sender")
    print("=" * 60)
    
    config = Config()
    
    print(f"📋 Tipos configurados: {', '.join(config.AUTO_SEND_TYPES)}")
    print(f"👥 Funcionários presença: {config.AUTO_ATTENDANCE_EMPLOYEES}")
    print(f"🌐 API: {config.BASE_URL}")
    print(f"🔑 Token: {config.API_KEY[:20]}...")
    print("=" * 60)
    
    # Executar envio de presença
    if 'attendance' in config.AUTO_SEND_TYPES:
        print("🔄 Enviando dados de presença...")
        try:
            sender = AttendanceSender()
            
            for employee_id in config.AUTO_ATTENDANCE_EMPLOYEES:
                print(f"👤 Enviando presença para funcionário {employee_id}")
                
                # Clock in
                result_in = sender.clock_in(
                    employee_id=employee_id,
                    clock_in_time=config.DEFAULT_CLOCK_IN_TIME,
                    include_location=config.INCLUDE_LOCATION,
                    latitude=config.DEFAULT_LATITUDE,
                    longitude=config.DEFAULT_LONGITUDE
                )
                
                if result_in:
                    print(f"✅ Clock in enviado para funcionário {employee_id}")
                else:
                    print(f"❌ Erro no clock in para funcionário {employee_id}")
                
                # Clock out
                result_out = sender.clock_out(
                    employee_id=employee_id,
                    clock_out_time=config.DEFAULT_CLOCK_OUT_TIME,
                    include_location=config.INCLUDE_LOCATION,
                    latitude=config.DEFAULT_LATITUDE,
                    longitude=config.DEFAULT_LONGITUDE
                )
                
                if result_out:
                    print(f"✅ Clock out enviado para funcionário {employee_id}")
                else:
                    print(f"❌ Erro no clock out para funcionário {employee_id}")
                    
        except Exception as e:
            print(f"❌ Erro no envio de presença: {e}")
    
    print("🎉 Envio único concluído!")

if __name__ == "__main__":
    main()