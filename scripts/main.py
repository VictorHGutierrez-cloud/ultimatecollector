#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 MENU PRINCIPAL - Ultimate Collector
Menu interativo para gerenciar coleta e envio de dados
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz do projeto ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from ultimate_collector.core.config import Config

def show_menu():
    """Exibe o menu principal"""
    print("\n" + "="*60)
    print("🎯 ULTIMATE COLLECTOR - MENU PRINCIPAL")
    print("="*60)
    print("1. 📥 Coletar dados (uma vez)")
    print("2. 📤 Enviar dados (uma vez)")
    print("3. 🔄 Coleta automática")
    print("4. 📤 Envio automático")
    print("5. 📊 Ver dados coletados")
    print("6. ⚙️  Configurações")
    print("7. ❌ Sair")
    print("="*60)

def collect_data():
    """Executa coleta única"""
    print("\n📥 COLETANDO DADOS...")
    try:
        from scripts.collect_data import main as collect_main
        collect_main()
    except Exception as e:
        print(f"❌ Erro na coleta: {e}")

def send_data():
    """Executa envio único"""
    print("\n📤 ENVIANDO DADOS...")
    try:
        from scripts.send_data import main as send_main
        send_main()
    except Exception as e:
        print(f"❌ Erro no envio: {e}")

def auto_collect():
    """Inicia coleta automática"""
    print("\n🔄 INICIANDO COLETA AUTOMÁTICA...")
    try:
        from scripts.auto_collect import main as auto_collect_main
        auto_collect_main()
    except Exception as e:
        print(f"❌ Erro na coleta automática: {e}")

def auto_send():
    """Inicia envio automático"""
    print("\n📤 INICIANDO ENVIO AUTOMÁTICO...")
    try:
        from scripts.auto_send import main as auto_send_main
        auto_send_main()
    except Exception as e:
        print(f"❌ Erro no envio automático: {e}")

def show_data():
    """Mostra dados coletados"""
    print("\n📊 DADOS COLETADOS:")
    print("="*40)

    raw_base = Path(Config.RAW_DATA_DIR or "data/raw")
    print(f"Pasta: {raw_base}")
    
    data_dirs = [
        ("👥 Funcionários", raw_base / "employees"),
        ("💰 Financeiro", raw_base / "finance"),
        ("💸 Despesas", raw_base / "expenses"),
        ("⏰ Presença", raw_base / "attendance")
    ]
    
    for name, path in data_dirs:
        if path.exists():
            files = list(path.glob("*.csv"))
            print(f"{name}: {len(files)} arquivos")
            if files:
                latest = max(files, key=lambda x: x.stat().st_mtime)
                print(f"   📄 Mais recente: {latest.name}")
        else:
            print(f"{name}: Nenhum arquivo")

def show_config():
    """Mostra configurações atuais"""
    print("\n⚙️  CONFIGURAÇÕES ATUAIS:")
    print("="*40)
    
    try:
        config = Config()
        print(f"🌐 API: {config.BASE_URL}")
        print(f"🔑 Token: {config.API_KEY[:20]}...")
        print(f"📥 Coleta automática: {config.AUTO_COLLECT_ON_START}")
        print(f"📤 Envio automático: {config.AUTO_SEND_ON_START}")
        print(f"📋 Categorias: {', '.join(config.AUTO_COLLECT_CATEGORIES)}")
        print(f"👥 Funcionários presença: {config.AUTO_ATTENDANCE_EMPLOYEES}")
    except Exception as e:
        print(f"❌ Erro ao carregar configurações: {e}")

def main():
    """Função principal do menu"""
    while True:
        show_menu()
        
        try:
            choice = input("\n🎯 Escolha uma opção (1-7): ").strip()
            
            if choice == "1":
                collect_data()
            elif choice == "2":
                send_data()
            elif choice == "3":
                auto_collect()
            elif choice == "4":
                auto_send()
            elif choice == "5":
                show_data()
            elif choice == "6":
                show_config()
            elif choice == "7":
                print("\n👋 Até logo!")
                break
            else:
                print("❌ Opção inválida! Tente novamente.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Até logo!")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        input("\n⏸️  Pressione Enter para continuar...")

if __name__ == "__main__":
    main()