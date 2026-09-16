#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 COLLECT ONCE - Coleta única
Executa uma coleta única baseada nas configurações do .env
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz do projeto ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from ultimate_collector.core.config import Config
from ultimate_collector.collectors.hr_data_masterultimate import HRDataMasterUltimate

def main():
    print("🎯 COLETA ÚNICA - Ultimate Collector")
    print("=" * 60)
    
    config = Config()
    collector = HRDataMasterUltimate()
    
    print(f"📋 Categorias configuradas: {', '.join(config.AUTO_COLLECT_CATEGORIES)}")
    print(f"🌐 API: {config.BASE_URL}")
    print(f"🔑 Token: {config.API_KEY[:20]}...")
    print("=" * 60)
    
    for category in config.AUTO_COLLECT_CATEGORIES:
        try:
            print(f"🔄 Coletando: {category}")
            collector.collect_category(category.strip())
            print(f"✅ {category} coletado com sucesso")
        except Exception as e:
            print(f"❌ Erro ao coletar {category}: {e}")
    
    print("🎉 Coleta única concluída!")

if __name__ == "__main__":
    main()
