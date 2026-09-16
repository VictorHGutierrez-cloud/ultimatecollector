#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 AUTO COLLECT - Coleta automática
Executa coleta automática baseada nas configurações do .env
"""

import sys
import time
from pathlib import Path

# Adicionar o diretório raiz do projeto ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from ultimate_collector.core.config import Config
from ultimate_collector.collectors.hr_data_masterultimate import HRDataMasterUltimate

def main():
    print("🔄 COLETA AUTOMÁTICA - Ultimate Collector")
    print("=" * 60)
    
    config = Config()
    collector = HRDataMasterUltimate()
    
    print(f"📋 Categorias configuradas: {', '.join(config.AUTO_COLLECT_CATEGORIES)}")
    print(f"⏰ Intervalo: {config.AUTO_COLLECT_INTERVAL} minutos")
    print(f"🌐 API: {config.BASE_URL}")
    print(f"🔑 Token: {config.API_KEY[:20]}...")
    print("=" * 60)
    
    print("🔄 Iniciando coleta automática...")
    print("💡 Pressione Ctrl+C para parar")
    
    try:
        while True:
            print(f"\n⏰ {time.strftime('%H:%M:%S')} - Iniciando coleta...")
            
            for category in config.AUTO_COLLECT_CATEGORIES:
                try:
                    print(f"🔄 Coletando: {category}")
                    collector.collect_category(category.strip())
                    print(f"✅ {category} coletado com sucesso")
                except Exception as e:
                    print(f"❌ Erro ao coletar {category}: {e}")
            
            print(f"✅ Coleta concluída! Próxima em {config.AUTO_COLLECT_INTERVAL} minutos...")
            time.sleep(config.AUTO_COLLECT_INTERVAL * 60)
            
    except KeyboardInterrupt:
        print("\n🛑 Coleta automática interrompida pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro na coleta automática: {e}")

if __name__ == "__main__":
    main()