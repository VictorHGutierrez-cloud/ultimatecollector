#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 ULTIMATE COLLECTOR - MENU INTERATIVO
Sistema definitivo com 28 funções avançadas
"""

import os
import sys
from pathlib import Path

# Obter o diretório onde este script está localizado
script_dir = Path(__file__).parent.resolve()

project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

secrets_dir = script_dir / "secrets"
seutoken_path = secrets_dir / "seutoken.txt"
if not seutoken_path.exists():
    seutoken_path = script_dir / "seutoken.txt"
if seutoken_path.exists():
    api_key = seutoken_path.read_text(encoding="utf-8").strip()
    if api_key:
        os.environ["API_KEY"] = api_key
        os.environ.setdefault("AUTH_TYPE", "x-api-key")

# Garantir que o config_local.env (na mesma pasta) seja carregado primeiro
# Fallback para config_unificado.env na raiz do projeto
try:
    from dotenv import load_dotenv
    
    # Priorizar config_local.env na mesma pasta do script
    local_config_path = secrets_dir / "config_local.env"
    if not local_config_path.exists():
        local_config_path = script_dir / "config_local.env"
    if local_config_path.exists():
        load_dotenv(local_config_path, override=True)
    else:
        for unified_path in (
            project_root / "config" / "unificado.env",
            project_root / "config_unificado.env",
        ):
            if unified_path.exists():
                load_dotenv(unified_path, override=True)
                break
except Exception:
    pass

from ultimate_collector.collectors.hr_data_masterultimate import HRDataMasterUltimate

class UltimateCollectorMenu:
    """Menu interativo do Ultimate Collector"""
    
    def __init__(self):
        # Não criar o coletor aqui - criar quando necessário para garantir config atualizada
        self.collector = None
        self.running = True
        self._menu_actions = {}
        self._max_option = 0
    
    def _get_collector(self):
        """Obtém o coletor, recriando se necessário para garantir config atualizada"""
        # Sempre recriar o coletor para garantir que está usando a configuração mais recente
        self.collector = HRDataMasterUltimate()
        return self.collector

    def _build_menu_actions(self):
        """Monta o índice de ações do menu dinamicamente"""
        actions = {}
        idx = 1
        actions[idx] = ("test_connection", None)
        idx += 1

        # Garantir que o coletor está inicializado
        collector = self._get_collector()
        categories = collector.list_categories()
        for category in categories:
            actions[idx] = ("collect_category", category)
            idx += 1

        actions[idx] = ("collect_all_data", None)
        idx += 1

        actions[idx] = ("analyze_data", None); idx += 1
        actions[idx] = ("export_data", None); idx += 1
        actions[idx] = ("validate_data", None); idx += 1
        actions[idx] = ("backup_data", None); idx += 1
        actions[idx] = ("cleanup_data", None); idx += 1
        actions[idx] = ("list_categories", None); idx += 1
        actions[idx] = ("list_endpoints", None); idx += 1
        actions[idx] = ("check_status", None); idx += 1
        actions[idx] = ("configure_filters", None); idx += 1
        actions[idx] = ("monitor_collection", None); idx += 1
        actions[idx] = ("show_stats", None); idx += 1
        actions[idx] = ("generate_report", None); idx += 1
        actions[idx] = ("collect_specific_category", None); idx += 1
        actions[idx] = ("collect_with_date_filter", None); idx += 1
        actions[idx] = ("auto_collect", None); idx += 1
        actions[idx] = ("exit_program", None); idx += 1

        self._menu_actions = actions
        self._max_option = idx - 1
        return categories
    
    def display_main_menu(self):
        """Exibe o menu principal"""
        categories = self._build_menu_actions()
        print("\n" + "="*80)
        print("🚀 ULTIMATE COLLECTOR - QI 300+ EDITION")
        print("   Sistema Definitivo com Funções Avançadas")
        print("="*80)
        print("📊 COLETA DE DADOS:")
        print("   1.  🔍 Testar Conexão")
        for i, cat in enumerate(categories, 2):
            print(f"   {i:2d}. 📥 Coletar {cat}")
        collect_all_option = len(categories) + 2
        print(f"   {collect_all_option:2d}. 🔄 Coletar TODOS os Dados")
        print("")
        print("📈 ANÁLISE E PROCESSAMENTO:")
        base = collect_all_option
        print(f"   {base+1:2d}. 📊 Analisar Dados")
        print(f"   {base+2:2d}. 📤 Exportar Dados")
        print(f"   {base+3:2d}. 🔍 Validar Dados")
        print(f"   {base+4:2d}. 💾 Backup de Dados")
        print(f"   {base+5:2d}. 🧹 Limpar Dados Antigos")
        print("")
        print("⚙️  CONFIGURAÇÃO E MONITORAMENTO:")
        print(f"   {base+6:2d}. 📋 Listar Categorias")
        print(f"   {base+7:2d}. 🔗 Listar Endpoints")
        print(f"   {base+8:2d}. 📊 Verificar Status")
        print(f"   {base+9:2d}. ⚙️  Configurar Filtros")
        print(f"   {base+10:2d}. 📈 Monitorar Coleta")
        print(f"   {base+11:2d}. 📊 Estatísticas de Coleta")
        print(f"   {base+12:2d}. 📄 Gerar Relatório Completo")
        print("")
        print("🔧 UTILIDADES:")
        print(f"   {base+13:2d}. 🎯 Coletar Categoria Específica")
        print(f"   {base+14:2d}. 📅 Coletar com Filtro de Data")
        print(f"   {base+15:2d}. 🔄 Coleta Automática")
        print(f"   {base+16:2d}. ❌ Sair")
        print("="*80)
    
    def get_user_choice(self):
        """Obtém escolha do usuário"""
        try:
            max_option = self._max_option or 1
            choice = input(f"\n🎯 Escolha uma opção (1-{max_option}): ").strip()
            return int(choice) if choice.isdigit() else 0
        except (ValueError, KeyboardInterrupt):
            return 0
    
    def handle_choice(self, choice):
        """Processa a escolha do usuário"""
        action = self._menu_actions.get(choice)
        if not action:
            print("❌ Opção inválida! Tente novamente.")
            return

        action_name, payload = action
        if action_name == "test_connection":
            self.test_connection()
        elif action_name == "collect_category":
            self.collect_category_by_name(payload)
        elif action_name == "collect_all_data":
            self.collect_all_data()
        elif action_name == "analyze_data":
            self.analyze_data()
        elif action_name == "export_data":
            self.export_data()
        elif action_name == "validate_data":
            self.validate_data()
        elif action_name == "backup_data":
            self.backup_data()
        elif action_name == "cleanup_data":
            self.cleanup_data()
        elif action_name == "list_categories":
            self.list_categories()
        elif action_name == "list_endpoints":
            self.list_endpoints()
        elif action_name == "check_status":
            self.check_status()
        elif action_name == "configure_filters":
            self.configure_filters()
        elif action_name == "monitor_collection":
            self.monitor_collection()
        elif action_name == "show_stats":
            self.show_stats()
        elif action_name == "generate_report":
            self.generate_report()
        elif action_name == "collect_specific_category":
            self.collect_specific_category()
        elif action_name == "collect_with_date_filter":
            self.collect_with_date_filter()
        elif action_name == "auto_collect":
            self.auto_collect()
        elif action_name == "exit_program":
            self.exit_program()
        else:
            print("❌ Opção inválida! Tente novamente.")

    def collect_category_by_name(self, category: str):
        """Coleta categoria selecionada no menu dinâmico"""
        print(f"\n📥 COLETANDO CATEGORIA: {category.upper()}...")
        print("-" * 50)
        # Recriar coletor para garantir config atualizada
        collector = self._get_collector()
        success = collector.collect_category(category)
        if success:
            print(f"✅ {category} coletado com sucesso!")
        else:
            print(f"❌ Erro na coleta de {category}!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def test_connection(self):
        """Função 1: Testar Conexão"""
        print("\n🔍 TESTANDO CONEXÃO...")
        print("-" * 50)
        # Recriar coletor para garantir config atualizada
        collector = self._get_collector()
        success = collector.test_connection()
        if success:
            print("✅ Conexão estabelecida com sucesso!")
        else:
            print("❌ Falha na conexão!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_employees(self):
        """Função 2: Coletar Funcionários"""
        print("\n👥 COLETANDO FUNCIONÁRIOS...")
        print("-" * 50)
        collector = self._get_collector()
        success = collector.collect_employees()
        if success:
            print("✅ Funcionários coletados com sucesso!")
        else:
            print("❌ Erro na coleta de funcionários!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_expenses(self):
        """Função 3: Coletar Despesas"""
        print("\n💰 COLETANDO DESPESAS...")
        print("-" * 50)
        collector = self._get_collector()
        success = collector.collect_expenses()
        if success:
            print("✅ Despesas coletadas com sucesso!")
        else:
            print("❌ Erro na coleta de despesas!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_finance(self):
        """Função 4: Coletar Dados Financeiros"""
        print("\n🏦 COLETANDO DADOS FINANCEIROS...")
        print("-" * 50)
        collector = self._get_collector()
        success = collector.collect_finance()
        if success:
            print("✅ Dados financeiros coletados com sucesso!")
        else:
            print("❌ Erro na coleta de dados financeiros!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_attendance(self):
        """Função 5: Coletar Presença"""
        print("\n⏰ COLETANDO PRESENÇA...")
        print("-" * 50)
        collector = self._get_collector()
        success = collector.collect_attendance()
        if success:
            print("✅ Dados de presença coletados com sucesso!")
        else:
            print("❌ Erro na coleta de presença!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_time_off(self):
        """Função 6: Coletar Férias"""
        print("\n🏖️  COLETANDO FÉRIAS E AUSÊNCIAS...")
        print("-" * 50)
        collector = self._get_collector()
        success = collector.collect_time_off()
        if success:
            print("✅ Dados de férias coletados com sucesso!")
        else:
            print("❌ Erro na coleta de férias!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_recruitment(self):
        """Função 7: Coletar Recrutamento"""
        print("\n📋 COLETANDO DADOS DE RECRUTAMENTO...")
        print("-" * 50)
        collector = self._get_collector()
        success = collector.collect_recruitment()
        if success:
            print("✅ Dados de recrutamento coletados com sucesso!")
        else:
            print("❌ Erro na coleta de recrutamento!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_performance(self):
        """Função 8: Coletar Performance"""
        print("\n🎯 COLETANDO DADOS DE PERFORMANCE...")
        print("-" * 50)
        collector = self._get_collector()
        success = collector.collect_performance()
        if success:
            print("✅ Dados de performance coletados com sucesso!")
        else:
            print("❌ Erro na coleta de performance!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_training(self):
        """Função 9: Coletar Treinamento"""
        print("\n🎓 COLETANDO DADOS DE TREINAMENTO...")
        print("-" * 50)
        collector = self._get_collector()
        success = collector.collect_training()
        if success:
            print("✅ Dados de treinamento coletados com sucesso!")
        else:
            print("❌ Erro na coleta de treinamento!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_documents(self):
        """Função 10: Coletar Documentos"""
        print("\n📄 COLETANDO DOCUMENTOS...")
        print("-" * 50)
        collector = self._get_collector()
        success = collector.collect_documents()
        if success:
            print("✅ Documentos coletados com sucesso!")
        else:
            print("❌ Erro na coleta de documentos!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_company(self):
        """Função 11: Coletar Dados da Empresa"""
        print("\n🏢 COLETANDO DADOS DA EMPRESA...")
        print("-" * 50)
        collector = self._get_collector()
        success = collector.collect_company()
        if success:
            print("✅ Dados da empresa coletados com sucesso!")
        else:
            print("❌ Erro na coleta de dados da empresa!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_all_data(self):
        """Função 12: Coletar TODOS os Dados"""
        print("\n🔄 COLETANDO TODOS OS DADOS...")
        print("-" * 50)
        print("⚠️  ATENÇÃO: Esta operação pode demorar!")
        confirm = input("Deseja continuar? (s/N): ").lower()
        if confirm == 's':
            # Recriar coletor para garantir config atualizada
            collector = self._get_collector()
            results = collector.collect_all_data()
            print(f"✅ Coleta completa finalizada!")
            print(f"📊 Resultados: {sum(results.values())} categorias processadas")
        else:
            print("❌ Operação cancelada!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def analyze_data(self):
        """Função 13: Analisar Dados"""
        print("\n📊 ANÁLISE DE DADOS")
        print("-" * 50)
        collector = self._get_collector()
        categories = collector.list_categories()
        print("Categorias disponíveis:")
        for i, cat in enumerate(categories, 1):
            print(f"   {i}. {cat}")
        
        try:
            choice = int(input("\nEscolha uma categoria (número): ")) - 1
            if 0 <= choice < len(categories):
                category = categories[choice]
                analysis = collector.analyze_data(category)
                print(f"\n📊 Análise de {category}:")
                print(f"   📄 Arquivos: {len(analysis.get('files', []))}")
                print(f"   📊 Registros: {analysis.get('total_records', 0)}")
            else:
                print("❌ Categoria inválida!")
        except ValueError:
            print("❌ Entrada inválida!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def export_data(self):
        """Função 14: Exportar Dados"""
        print("\n📤 EXPORTAR DADOS")
        print("-" * 50)
        collector = self._get_collector()
        categories = collector.list_categories()
        print("Categorias disponíveis:")
        for i, cat in enumerate(categories, 1):
            print(f"   {i}. {cat}")
        
        try:
            choice = int(input("\nEscolha uma categoria (número): ")) - 1
            if 0 <= choice < len(categories):
                category = categories[choice]
                format_choice = input("Formato (excel/csv): ").lower()
                if format_choice in ['excel', 'csv']:
                    success = collector.export_data(category, format_choice)
                    if success:
                        print(f"✅ Dados exportados com sucesso!")
                    else:
                        print("❌ Erro na exportação!")
                else:
                    print("❌ Formato inválido!")
            else:
                print("❌ Categoria inválida!")
        except ValueError:
            print("❌ Entrada inválida!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def validate_data(self):
        """Função 15: Validar Dados"""
        print("\n🔍 VALIDAÇÃO DE DADOS")
        print("-" * 50)
        collector = self._get_collector()
        categories = collector.list_categories()
        print("Categorias disponíveis:")
        for i, cat in enumerate(categories, 1):
            print(f"   {i}. {cat}")
        
        try:
            choice = int(input("\nEscolha uma categoria (número): ")) - 1
            if 0 <= choice < len(categories):
                category = categories[choice]
                validation = collector.validate_data(category)
                print(f"\n🔍 Validação de {category}:")
                print(f"   📊 Qualidade: {validation.get('quality_score', 0)}%")
                print(f"   📄 Arquivos: {validation.get('files_validated', 0)}")
                print(f"   📊 Registros: {validation.get('total_records', 0)}")
            else:
                print("❌ Categoria inválida!")
        except ValueError:
            print("❌ Entrada inválida!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def backup_data(self):
        """Função 16: Backup de Dados"""
        print("\n💾 BACKUP DE DADOS")
        print("-" * 50)
        collector = self._get_collector()
        categories = collector.list_categories()
        print("Categorias disponíveis:")
        for i, cat in enumerate(categories, 1):
            print(f"   {i}. {cat}")
        
        try:
            choice = int(input("\nEscolha uma categoria (número): ")) - 1
            if 0 <= choice < len(categories):
                category = categories[choice]
                success = collector.backup_data(category)
                if success:
                    print(f"✅ Backup de {category} criado com sucesso!")
                else:
                    print("❌ Erro no backup!")
            else:
                print("❌ Categoria inválida!")
        except ValueError:
            print("❌ Entrada inválida!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def cleanup_data(self):
        """Função 17: Limpar Dados Antigos"""
        print("\n🧹 LIMPEZA DE DADOS ANTIGOS")
        print("-" * 50)
        collector = self._get_collector()
        categories = collector.list_categories()
        print("Categorias disponíveis:")
        for i, cat in enumerate(categories, 1):
            print(f"   {i}. {cat}")
        
        try:
            choice = int(input("\nEscolha uma categoria (número): ")) - 1
            if 0 <= choice < len(categories):
                category = categories[choice]
                days = int(input("Dias para manter (padrão 30): ") or "30")
                success = collector.cleanup_old_data(category, days)
                if success:
                    print(f"✅ Limpeza de {category} concluída!")
                else:
                    print("❌ Erro na limpeza!")
            else:
                print("❌ Categoria inválida!")
        except ValueError:
            print("❌ Entrada inválida!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def list_categories(self):
        """Função 18: Listar Categorias"""
        print("\n📋 CATEGORIAS DISPONÍVEIS")
        print("-" * 50)
        collector = self._get_collector()
        categories = collector.list_categories()
        for i, category in enumerate(categories, 1):
            endpoints = collector.list_endpoints(category)
            print(f"   {i:2d}. {category:<15} ({len(endpoints)} endpoints)")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def list_endpoints(self):
        """Função 19: Listar Endpoints"""
        print("\n🔗 ENDPOINTS DISPONÍVEIS")
        print("-" * 50)
        collector = self._get_collector()
        categories = collector.list_categories()
        print("Categorias disponíveis:")
        for i, cat in enumerate(categories, 1):
            print(f"   {i}. {cat}")
        
        try:
            choice = int(input("\nEscolha uma categoria (número): ")) - 1
            if 0 <= choice < len(categories):
                category = categories[choice]
                endpoints = collector.list_endpoints(category)
                print(f"\n🔗 Endpoints de {category}:")
                for name, path in endpoints.items():
                    print(f"   • {name}: {path}")
            else:
                print("❌ Categoria inválida!")
        except ValueError:
            print("❌ Entrada inválida!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def check_status(self):
        """Função 20: Verificar Status"""
        print("\n📊 STATUS DO SISTEMA")
        print("-" * 50)
        collector = self._get_collector()
        status = collector.check_status()
        print(f"🔌 Cliente inicializado: {'✅' if status['client_initialized'] else '❌'}")
        print(f"⚙️  Configuração carregada: {'✅' if status['config_loaded'] else '❌'}")
        print(f"📁 Categorias disponíveis: {status['categories_available']}")
        print(f"🔗 Total de endpoints: {status['total_endpoints']}")
        print(f"📊 Estatísticas: {status['collection_stats']}")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def configure_filters(self):
        """Função 21: Configurar Filtros"""
        print("\n⚙️  CONFIGURAÇÃO DE FILTROS")
        print("-" * 50)
        collector = self._get_collector()
        categories = collector.list_categories()
        print("Categorias disponíveis:")
        for i, cat in enumerate(categories, 1):
            print(f"   {i}. {cat}")
        
        try:
            choice = int(input("\nEscolha uma categoria (número): ")) - 1
            if 0 <= choice < len(categories):
                category = categories[choice]
                print(f"\nConfigurando filtros para {category}...")
                filters = {}
                # Implementar lógica de filtros personalizados
                success = collector.configure_filters(category, filters)
                if success:
                    print(f"✅ Filtros configurados para {category}!")
                else:
                    print("❌ Erro na configuração!")
            else:
                print("❌ Categoria inválida!")
        except ValueError:
            print("❌ Entrada inválida!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def monitor_collection(self):
        """Função 22: Monitorar Coleta"""
        print("\n📈 MONITORAMENTO DE COLETA")
        print("-" * 50)
        collector = self._get_collector()
        categories = collector.list_categories()
        print("Categorias disponíveis:")
        for i, cat in enumerate(categories, 1):
            print(f"   {i}. {cat}")
        
        try:
            choice = int(input("\nEscolha uma categoria (número): ")) - 1
            if 0 <= choice < len(categories):
                category = categories[choice]
                monitor = collector.monitor_collection(category)
                print(f"\n📈 Monitoramento de {category}:")
                print(f"   Status: {monitor.get('status', 'unknown')}")
                print(f"   Arquivos: {monitor.get('files_count', 0)}")
                print(f"   Registros: {monitor.get('total_records', 0)}")
            else:
                print("❌ Categoria inválida!")
        except ValueError:
            print("❌ Entrada inválida!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def show_stats(self):
        """Função 23: Estatísticas de Coleta"""
        print("\n📊 ESTATÍSTICAS DE COLETA")
        print("-" * 50)
        collector = self._get_collector()
        stats = collector.get_collection_stats()
        print(f"🔗 Endpoints processados: {stats['total_endpoints']}")
        print(f"📁 Categorias completadas: {stats['categories_completed']}")
        print(f"📄 Total de registros: {stats['total_records']}")
        if stats['duration']:
            print(f"⏱️  Duração: {stats['duration']}")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def generate_report(self):
        """Função 24: Gerar Relatório Completo"""
        print("\n📄 GERANDO RELATÓRIO COMPLETO...")
        print("-" * 50)
        collector = self._get_collector()
        report = collector.generate_report()
        if report:
            print("✅ Relatório gerado com sucesso!")
            print(f"📊 Categorias analisadas: {len(report.get('categories', {}))}")
            print(f"📄 Arquivo salvo: data/processed/relatorio_completo.json")
        else:
            print("❌ Erro na geração do relatório!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_specific_category(self):
        """Função 25: Coletar Categoria Específica"""
        print("\n🎯 COLETA DE CATEGORIA ESPECÍFICA")
        print("-" * 50)
        collector = self._get_collector()
        categories = collector.list_categories()
        print("Categorias disponíveis:")
        for i, cat in enumerate(categories, 1):
            print(f"   {i}. {cat}")
        
        try:
            choice = int(input("\nEscolha uma categoria (número): ")) - 1
            if 0 <= choice < len(categories):
                category = categories[choice]
                success = collector.collect_category(category)
                if success:
                    print(f"✅ {category} coletado com sucesso!")
                else:
                    print(f"❌ Erro na coleta de {category}!")
            else:
                print("❌ Categoria inválida!")
        except ValueError:
            print("❌ Entrada inválida!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_with_date_filter(self):
        """Função 26: Coletar com Filtro de Data"""
        print("\n📅 COLETA COM FILTRO DE DATA")
        print("-" * 50)
        collector = self._get_collector()
        categories = collector.list_categories()
        print("Categorias disponíveis:")
        for i, cat in enumerate(categories, 1):
            print(f"   {i}. {cat}")
        
        try:
            choice = int(input("\nEscolha uma categoria (número): ")) - 1
            if 0 <= choice < len(categories):
                category = categories[choice]
                days = int(input("Últimos quantos dias? (padrão 30): ") or "30")
                success = collector.collect_category(category, days)
                if success:
                    print(f"✅ {category} coletado com sucesso (últimos {days} dias)!")
                else:
                    print(f"❌ Erro na coleta de {category}!")
            else:
                print("❌ Categoria inválida!")
        except ValueError:
            print("❌ Entrada inválida!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def auto_collect(self):
        """Função 27: Coleta Automática"""
        print("\n🔄 COLETA AUTOMÁTICA")
        print("-" * 50)
        print("⚠️  ATENÇÃO: Esta operação executará coleta contínua!")
        print("💡 Pressione Ctrl+C para parar")
        confirm = input("Deseja continuar? (s/N): ").lower()
        if confirm == 's':
            try:
                import time
                while True:
                    print(f"\n⏰ {time.strftime('%H:%M:%S')} - Iniciando coleta automática...")
                    collector = self._get_collector()
                    collector.collect_all_data()
                    print("✅ Coleta automática concluída! Próxima em 60 minutos...")
                    time.sleep(3600)  # 60 minutos
            except KeyboardInterrupt:
                print("\n🛑 Coleta automática interrompida pelo usuário!")
        else:
            print("❌ Operação cancelada!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def exit_program(self):
        """Função 28: Sair"""
        print("\n👋 OBRIGADO POR USAR O ULTIMATE COLLECTOR!")
        print("🚀 Sistema desenvolvido com QI 300+")
        self.running = False
    
    def run(self):
        """Executa o menu principal"""
        while self.running:
            try:
                self.display_main_menu()
                choice = self.get_user_choice()
                self.handle_choice(choice)
            except KeyboardInterrupt:
                print("\n\n👋 Saindo...")
                break
            except Exception as e:
                print(f"\n❌ Erro inesperado: {e}")
                input("\n⏸️  Pressione Enter para continuar...")

def main():
    """Função principal"""
    print("🚀 INICIANDO ULTIMATE COLLECTOR...")
    print("   Sistema Definitivo com 28 Funções Avançadas")
    
    menu = UltimateCollectorMenu()
    menu.run()

if __name__ == "__main__":
    main()
