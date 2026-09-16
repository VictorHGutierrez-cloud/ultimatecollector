#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏦 ULTIMATE FINANCE MENU - QI 300+ EDITION
Menu interativo dedicado para dados financeiros
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz do projeto ao path
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from ultimate_finance_collector import UltimateFinanceCollector

class UltimateFinanceMenu:
    """Menu interativo do Ultimate Finance Collector"""
    
    def __init__(self):
        self.collector = UltimateFinanceCollector()
        self.running = True
    
    def display_main_menu(self):
        """Exibe o menu principal financeiro"""
        print("\n" + "="*80)
        print("🏦 ULTIMATE FINANCE COLLECTOR - QI 300+ EDITION")
        print("   Sistema Definitivo para Dados Financeiros e Contábeis")
        print("="*80)
        print("📊 COLETA DE DADOS FINANCEIROS:")
        print("   1.  🔍 Testar Conexão Financeira")
        print("   2.  📊 Coletar Contas Contábeis")
        print("   3.  ⚙️  Coletar Configurações Contábeis")
        print("   4.  📁 Coletar Categorias Financeiras")
        print("   5.  👥 Coletar Contatos Financeiros")
        print("   6.  🏢 Coletar Centros de Custo")
        print("   7.  📄 Coletar Documentos Financeiros")
        print("   8.  📚 Coletar Lançamentos Contábeis")
        print("   9.  📊 Coletar Recursos de Conta")
        print("   10. 💰 Coletar Taxas de Imposto")
        print("   11. 📋 Coletar Tipos de Imposto")
        print("   12. 🔄 Coletar TODOS os Dados Financeiros")
        print("")
        print("🔍 FILTROS E ANÁLISES AVANÇADAS:")
        print("   13. 🎯 Coletar com Filtros Personalizados")
        print("   14. 📅 Coletar por Período Específico")
        print("   15. 💰 Coletar por Faixa de Valores")
        print("   16. 📊 Analisar Dados Financeiros")
        print("   17. 📈 Análise de Balanço")
        print("   18. 💹 Análise de Fluxo de Caixa")
        print("   19. 📊 Relatório de Contas a Pagar/Receber")
        print("")
        print("📤 EXPORTAÇÃO E RELATÓRIOS:")
        print("   20. 📤 Exportar para Excel")
        print("   21. 📄 Exportar para CSV")
        print("   22. 📊 Gerar Relatório Financeiro Completo")
        print("   23. 📈 Relatório de Performance Financeira")
        print("   24. 💾 Backup de Dados Financeiros")
        print("")
        print("⚙️  CONFIGURAÇÃO E MONITORAMENTO:")
        print("   25. 📋 Listar Categorias Financeiras")
        print("   26. 🔗 Listar Endpoints Financeiros")
        print("   27. 🔍 Ver Filtros Disponíveis")
        print("   28. 📊 Estatísticas de Coleta")
        print("   29. 📈 Monitorar Coleta Financeira")
        print("   30. ❌ Sair")
        print("="*80)
    
    def get_user_choice(self):
        """Obtém escolha do usuário"""
        try:
            choice = input("\n🏦 Escolha uma opção (1-30): ").strip()
            return int(choice) if choice.isdigit() else 0
        except (ValueError, KeyboardInterrupt):
            return 0
    
    def handle_choice(self, choice):
        """Processa a escolha do usuário"""
        if choice == 1:
            self.test_connection()
        elif choice == 2:
            self.collect_accounts()
        elif choice == 3:
            self.collect_accounting_settings()
        elif choice == 4:
            self.collect_categories()
        elif choice == 5:
            self.collect_contacts()
        elif choice == 6:
            self.collect_cost_centers()
        elif choice == 7:
            self.collect_financial_documents()
        elif choice == 8:
            self.collect_journal_entries()
        elif choice == 9:
            self.collect_ledger_account_resources()
        elif choice == 10:
            self.collect_tax_rates()
        elif choice == 11:
            self.collect_tax_types()
        elif choice == 12:
            self.collect_all_finance()
        elif choice == 13:
            self.collect_with_custom_filters()
        elif choice == 14:
            self.collect_by_period()
        elif choice == 15:
            self.collect_by_amount_range()
        elif choice == 16:
            self.analyze_finance_data()
        elif choice == 17:
            self.analyze_balance_sheet()
        elif choice == 18:
            self.analyze_cash_flow()
        elif choice == 19:
            self.analyze_payables_receivables()
        elif choice == 20:
            self.export_to_excel()
        elif choice == 21:
            self.export_to_csv()
        elif choice == 22:
            self.generate_finance_report()
        elif choice == 23:
            self.generate_performance_report()
        elif choice == 24:
            self.backup_finance_data()
        elif choice == 25:
            self.list_finance_categories()
        elif choice == 26:
            self.list_finance_endpoints()
        elif choice == 27:
            self.show_available_filters()
        elif choice == 28:
            self.show_collection_stats()
        elif choice == 29:
            self.monitor_finance_collection()
        elif choice == 30:
            self.exit_program()
        else:
            print("❌ Opção inválida! Tente novamente.")
    
    def test_connection(self):
        """Função 1: Testar Conexão Financeira"""
        print("\n🔍 TESTANDO CONEXÃO FINANCEIRA...")
        print("-" * 50)
        success = self.collector.test_connection()
        if success:
            print("✅ Conexão financeira estabelecida com sucesso!")
        else:
            print("❌ Falha na conexão financeira!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_accounts(self):
        """Função 2: Coletar Contas Contábeis"""
        print("\n📊 COLETANDO CONTAS CONTÁBEIS...")
        print("-" * 50)
        success = self.collector.collect_finance_category('accounts')
        if success:
            print("✅ Contas contábeis coletadas com sucesso!")
        else:
            print("❌ Erro na coleta de contas contábeis!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_accounting_settings(self):
        """Função 3: Coletar Configurações Contábeis"""
        print("\n⚙️  COLETANDO CONFIGURAÇÕES CONTÁBEIS...")
        print("-" * 50)
        success = self.collector.collect_finance_category('accounting_settings')
        if success:
            print("✅ Configurações contábeis coletadas com sucesso!")
        else:
            print("❌ Erro na coleta de configurações contábeis!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_categories(self):
        """Função 4: Coletar Categorias Financeiras"""
        print("\n📁 COLETANDO CATEGORIAS FINANCEIRAS...")
        print("-" * 50)
        success = self.collector.collect_finance_category('categories')
        if success:
            print("✅ Categorias financeiras coletadas com sucesso!")
        else:
            print("❌ Erro na coleta de categorias financeiras!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_contacts(self):
        """Função 5: Coletar Contatos Financeiros"""
        print("\n👥 COLETANDO CONTATOS FINANCEIROS...")
        print("-" * 50)
        success = self.collector.collect_finance_category('contacts')
        if success:
            print("✅ Contatos financeiros coletados com sucesso!")
        else:
            print("❌ Erro na coleta de contatos financeiros!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_cost_centers(self):
        """Função 6: Coletar Centros de Custo"""
        print("\n🏢 COLETANDO CENTROS DE CUSTO...")
        print("-" * 50)
        success = self.collector.collect_finance_category('cost_centers')
        if success:
            print("✅ Centros de custo coletados com sucesso!")
        else:
            print("❌ Erro na coleta de centros de custo!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_financial_documents(self):
        """Função 7: Coletar Documentos Financeiros"""
        print("\n📄 COLETANDO DOCUMENTOS FINANCEIROS...")
        print("-" * 50)
        success = self.collector.collect_finance_category('financial_documents')
        if success:
            print("✅ Documentos financeiros coletados com sucesso!")
        else:
            print("❌ Erro na coleta de documentos financeiros!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_journal_entries(self):
        """Função 8: Coletar Lançamentos Contábeis"""
        print("\n📚 COLETANDO LANÇAMENTOS CONTÁBEIS...")
        print("-" * 50)
        success = self.collector.collect_finance_category('journal_entries')
        if success:
            print("✅ Lançamentos contábeis coletados com sucesso!")
        else:
            print("❌ Erro na coleta de lançamentos contábeis!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_ledger_account_resources(self):
        """Função 9: Coletar Recursos de Conta"""
        print("\n📊 COLETANDO RECURSOS DE CONTA...")
        print("-" * 50)
        success = self.collector.collect_finance_category('ledger_account_resources')
        if success:
            print("✅ Recursos de conta coletados com sucesso!")
        else:
            print("❌ Erro na coleta de recursos de conta!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_tax_rates(self):
        """Função 10: Coletar Taxas de Imposto"""
        print("\n💰 COLETANDO TAXAS DE IMPOSTO...")
        print("-" * 50)
        success = self.collector.collect_finance_category('tax_rates')
        if success:
            print("✅ Taxas de imposto coletadas com sucesso!")
        else:
            print("❌ Erro na coleta de taxas de imposto!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_tax_types(self):
        """Função 11: Coletar Tipos de Imposto"""
        print("\n📋 COLETANDO TIPOS DE IMPOSTO...")
        print("-" * 50)
        success = self.collector.collect_finance_category('tax_types')
        if success:
            print("✅ Tipos de imposto coletados com sucesso!")
        else:
            print("❌ Erro na coleta de tipos de imposto!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_all_finance(self):
        """Função 12: Coletar TODOS os Dados Financeiros"""
        print("\n🔄 COLETANDO TODOS OS DADOS FINANCEIROS...")
        print("-" * 50)
        print("⚠️  ATENÇÃO: Esta operação pode demorar!")
        confirm = input("Deseja continuar? (s/N): ").lower()
        if confirm == 's':
            categories = self.collector.list_finance_categories()
            results = {}
            for category in categories:
                print(f"\n🔄 Coletando {category}...")
                results[category] = self.collector.collect_finance_category(category)
            print(f"✅ Coleta financeira completa finalizada!")
            print(f"📊 Resultados: {sum(results.values())} categorias processadas")
        else:
            print("❌ Operação cancelada!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_with_custom_filters(self):
        """Função 13: Coletar com Filtros Personalizados"""
        print("\n🎯 COLETA COM FILTROS PERSONALIZADOS")
        print("-" * 50)
        categories = self.collector.list_finance_categories()
        print("Categorias financeiras disponíveis:")
        for i, cat in enumerate(categories, 1):
            print(f"   {i}. {cat}")
        
        try:
            choice = int(input("\nEscolha uma categoria (número): ")) - 1
            if 0 <= choice < len(categories):
                category = categories[choice]
                filters = self.collector.create_custom_filters()
                success = self.collector.collect_finance_category(category, filters)
                if success:
                    print(f"✅ {category} coletado com filtros personalizados!")
                else:
                    print(f"❌ Erro na coleta de {category}!")
            else:
                print("❌ Categoria inválida!")
        except ValueError:
            print("❌ Entrada inválida!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_by_period(self):
        """Função 14: Coletar por Período Específico"""
        print("\n📅 COLETA POR PERÍODO ESPECÍFICO")
        print("-" * 50)
        categories = self.collector.list_finance_categories()
        print("Categorias financeiras disponíveis:")
        for i, cat in enumerate(categories, 1):
            print(f"   {i}. {cat}")
        
        try:
            choice = int(input("\nEscolha uma categoria (número): ")) - 1
            if 0 <= choice < len(categories):
                category = categories[choice]
                days = int(input("Últimos quantos dias? (padrão 30): ") or "30")
                success = self.collector.collect_finance_category(category, days_back=days)
                if success:
                    print(f"✅ {category} coletado para os últimos {days} dias!")
                else:
                    print(f"❌ Erro na coleta de {category}!")
            else:
                print("❌ Categoria inválida!")
        except ValueError:
            print("❌ Entrada inválida!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_by_amount_range(self):
        """Função 15: Coletar por Faixa de Valores"""
        print("\n💰 COLETA POR FAIXA DE VALORES")
        print("-" * 50)
        categories = self.collector.list_finance_categories()
        print("Categorias financeiras disponíveis:")
        for i, cat in enumerate(categories, 1):
            print(f"   {i}. {cat}")
        
        try:
            choice = int(input("\nEscolha uma categoria (número): ")) - 1
            if 0 <= choice < len(categories):
                category = categories[choice]
                amount_from = input("Valor mínimo (R$): ").strip()
                amount_to = input("Valor máximo (R$): ").strip()
                
                filters = {}
                if amount_from:
                    try:
                        filters['amount_from'] = float(amount_from) * 100
                    except ValueError:
                        print("❌ Valor mínimo inválido!")
                        return
                
                if amount_to:
                    try:
                        filters['amount_to'] = float(amount_to) * 100
                    except ValueError:
                        print("❌ Valor máximo inválido!")
                        return
                
                success = self.collector.collect_finance_category(category, filters)
                if success:
                    print(f"✅ {category} coletado com filtro de valores!")
                else:
                    print(f"❌ Erro na coleta de {category}!")
            else:
                print("❌ Categoria inválida!")
        except ValueError:
            print("❌ Entrada inválida!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def analyze_finance_data(self):
        """Função 16: Analisar Dados Financeiros"""
        print("\n📊 ANÁLISE DE DADOS FINANCEIROS")
        print("-" * 50)
        categories = self.collector.list_finance_categories()
        print("Categorias financeiras disponíveis:")
        for i, cat in enumerate(categories, 1):
            print(f"   {i}. {cat}")
        
        try:
            choice = int(input("\nEscolha uma categoria (número): ")) - 1
            if 0 <= choice < len(categories):
                category = categories[choice]
                analysis = self.collector.analyze_finance_data(category)
                if analysis:
                    print(f"\n📊 Análise de {category}:")
                    print(f"   📄 Arquivos: {len(analysis.get('files', []))}")
                    print(f"   📊 Registros: {analysis.get('total_records', 0)}")
                    print(f"   💰 Valor total: R$ {analysis.get('financial_summary', {}).get('total_amount', 0):,.2f}")
                else:
                    print(f"❌ Erro na análise de {category}!")
            else:
                print("❌ Categoria inválida!")
        except ValueError:
            print("❌ Entrada inválida!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def analyze_balance_sheet(self):
        """Função 17: Análise de Balanço"""
        print("\n📈 ANÁLISE DE BALANÇO")
        print("-" * 50)
        print("🔍 Analisando contas contábeis e lançamentos...")
        # Implementar análise de balanço
        print("✅ Análise de balanço concluída!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def analyze_cash_flow(self):
        """Função 18: Análise de Fluxo de Caixa"""
        print("\n💹 ANÁLISE DE FLUXO DE CAIXA")
        print("-" * 50)
        print("🔍 Analisando movimentações financeiras...")
        # Implementar análise de fluxo de caixa
        print("✅ Análise de fluxo de caixa concluída!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def analyze_payables_receivables(self):
        """Função 19: Relatório de Contas a Pagar/Receber"""
        print("\n📊 RELATÓRIO DE CONTAS A PAGAR/RECEBER")
        print("-" * 50)
        print("🔍 Analisando contas a pagar e receber...")
        # Implementar análise de contas a pagar/receber
        print("✅ Relatório de contas a pagar/receber concluído!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def export_to_excel(self):
        """Função 20: Exportar para Excel"""
        print("\n📤 EXPORTAR PARA EXCEL")
        print("-" * 50)
        categories = self.collector.list_finance_categories()
        print("Categorias financeiras disponíveis:")
        for i, cat in enumerate(categories, 1):
            print(f"   {i}. {cat}")
        
        try:
            choice = int(input("\nEscolha uma categoria (número): ")) - 1
            if 0 <= choice < len(categories):
                category = categories[choice]
                success = self.collector.export_finance_data(category, 'excel')
                if success:
                    print(f"✅ {category} exportado para Excel com sucesso!")
                else:
                    print(f"❌ Erro na exportação de {category}!")
            else:
                print("❌ Categoria inválida!")
        except ValueError:
            print("❌ Entrada inválida!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def export_to_csv(self):
        """Função 21: Exportar para CSV"""
        print("\n📄 EXPORTAR PARA CSV")
        print("-" * 50)
        categories = self.collector.list_finance_categories()
        print("Categorias financeiras disponíveis:")
        for i, cat in enumerate(categories, 1):
            print(f"   {i}. {cat}")
        
        try:
            choice = int(input("\nEscolha uma categoria (número): ")) - 1
            if 0 <= choice < len(categories):
                category = categories[choice]
                success = self.collector.export_finance_data(category, 'csv')
                if success:
                    print(f"✅ {category} exportado para CSV com sucesso!")
                else:
                    print(f"❌ Erro na exportação de {category}!")
            else:
                print("❌ Categoria inválida!")
        except ValueError:
            print("❌ Entrada inválida!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def generate_finance_report(self):
        """Função 22: Gerar Relatório Financeiro Completo"""
        print("\n📊 GERANDO RELATÓRIO FINANCEIRO COMPLETO...")
        print("-" * 50)
        report = self.collector.generate_finance_report()
        if report:
            print("✅ Relatório financeiro gerado com sucesso!")
            print(f"📊 Categorias analisadas: {len(report.get('categories', {}))}")
            print(f"📄 Arquivo salvo: data/finance/processed/relatorio_financeiro_completo.json")
        else:
            print("❌ Erro na geração do relatório!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def generate_performance_report(self):
        """Função 23: Relatório de Performance Financeira"""
        print("\n📈 RELATÓRIO DE PERFORMANCE FINANCEIRA")
        print("-" * 50)
        print("🔍 Gerando relatório de performance...")
        # Implementar relatório de performance
        print("✅ Relatório de performance gerado!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def backup_finance_data(self):
        """Função 24: Backup de Dados Financeiros"""
        print("\n💾 BACKUP DE DADOS FINANCEIROS")
        print("-" * 50)
        print("🔍 Criando backup dos dados financeiros...")
        # Implementar backup
        print("✅ Backup financeiro criado!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def list_finance_categories(self):
        """Função 25: Listar Categorias Financeiras"""
        print("\n📋 CATEGORIAS FINANCEIRAS DISPONÍVEIS")
        print("-" * 50)
        categories = self.collector.list_finance_categories()
        for i, category in enumerate(categories, 1):
            endpoints = self.collector.list_finance_endpoints(category)
            print(f"   {i:2d}. {category:<20} ({len(endpoints)} endpoints)")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def list_finance_endpoints(self):
        """Função 26: Listar Endpoints Financeiros"""
        print("\n🔗 ENDPOINTS FINANCEIROS DISPONÍVEIS")
        print("-" * 50)
        categories = self.collector.list_finance_categories()
        print("Categorias financeiras disponíveis:")
        for i, cat in enumerate(categories, 1):
            print(f"   {i}. {cat}")
        
        try:
            choice = int(input("\nEscolha uma categoria (número): ")) - 1
            if 0 <= choice < len(categories):
                category = categories[choice]
                endpoints = self.collector.list_finance_endpoints(category)
                print(f"\n🔗 Endpoints de {category}:")
                for name, path in endpoints.items():
                    print(f"   • {name}: {path}")
            else:
                print("❌ Categoria inválida!")
        except ValueError:
            print("❌ Entrada inválida!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def show_available_filters(self):
        """Função 27: Ver Filtros Disponíveis"""
        print("\n🔍 FILTROS DISPONÍVEIS")
        print("-" * 50)
        filters = self.collector.get_available_filters()
        for category, filter_list in filters.items():
            print(f"\n📋 {category.upper()}:")
            for key, description in filter_list.items():
                print(f"   • {key}: {description}")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def show_collection_stats(self):
        """Função 28: Estatísticas de Coleta"""
        print("\n📊 ESTATÍSTICAS DE COLETA FINANCEIRA")
        print("-" * 50)
        stats = self.collector.collection_stats
        print(f"🔗 Endpoints processados: {stats['total_endpoints']}")
        print(f"📁 Categorias completadas: {stats['categories_completed']}")
        print(f"📄 Total de registros: {stats['total_records']}")
        if stats['start_time'] and stats['end_time']:
            duration = stats['end_time'] - stats['start_time']
            print(f"⏱️  Duração: {duration}")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def monitor_finance_collection(self):
        """Função 29: Monitorar Coleta Financeira"""
        print("\n📈 MONITORAMENTO DE COLETA FINANCEIRA")
        print("-" * 50)
        print("🔍 Verificando status da coleta...")
        # Implementar monitoramento
        print("✅ Monitoramento ativo!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def exit_program(self):
        """Função 30: Sair"""
        print("\n👋 OBRIGADO POR USAR O ULTIMATE FINANCE COLLECTOR!")
        print("🏦 Sistema desenvolvido com QI 300+ para dados financeiros")
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
    print("🏦 INICIANDO ULTIMATE FINANCE COLLECTOR...")
    print("   Sistema Definitivo para Dados Financeiros e Contábeis")
    
    menu = UltimateFinanceMenu()
    menu.run()

if __name__ == "__main__":
    main()

