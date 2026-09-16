#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏦 ULTIMATE FINANCE SYSTEM - QI 300+ EDITION
Sistema completo de coleta e envio de dados financeiros
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz do projeto ao path
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from ultimate_finance_collector import UltimateFinanceCollector
from ultimate_finance_senders import UltimateFinanceSenders

class UltimateFinanceSystem:
    """Sistema completo de finance com coleta e envio"""
    
    def __init__(self):
        self.collector = UltimateFinanceCollector()
        self.senders = UltimateFinanceSenders()
        self.running = True
    
    def display_main_menu(self):
        """Exibe o menu principal do sistema financeiro"""
        print("\n" + "="*80)
        print("🏦 ULTIMATE FINANCE SYSTEM - QI 300+ EDITION")
        print("   Sistema Completo de Coleta e Envio de Dados Financeiros")
        print("="*80)
        print("📊 COLETA DE DADOS FINANCEIROS:")
        print("   1.  🔍 Testar Conexão")
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
        print("📤 ENVIO DE DADOS FINANCEIROS:")
        print("   13. 📊 Enviar Conta Contábil")
        print("   14. ⚙️  Enviar Configuração Contábil")
        print("   15. 📁 Enviar Categoria Financeira")
        print("   16. 👥 Enviar Contato Financeiro")
        print("   17. 🏢 Enviar Centro de Custo")
        print("   18. 📄 Enviar Documento Financeiro")
        print("   19. 📚 Enviar Lançamento Contábil")
        print("   20. 📊 Enviar Recurso de Conta")
        print("   21. 💰 Enviar Taxa de Imposto")
        print("   22. 📋 Enviar Tipo de Imposto")
        print("   23. 🔄 Enviar Lote de Dados")
        print("")
        print("🔍 FILTROS E ANÁLISES:")
        print("   24. 🎯 Coletar com Filtros Personalizados")
        print("   25. 📅 Coletar por Período")
        print("   26. 💰 Coletar por Faixa de Valores")
        print("   27. 📊 Analisar Dados Financeiros")
        print("   28. 📈 Gerar Relatório Financeiro")
        print("")
        print("⚙️  CONFIGURAÇÃO E MONITORAMENTO:")
        print("   29. 📋 Listar Categorias Disponíveis")
        print("   30. 🔗 Listar Endpoints Disponíveis")
        print("   31. 📊 Estatísticas de Coleta")
        print("   32. 📤 Estatísticas de Envio")
        print("   33. 🧪 Testar Envio com Dados de Exemplo")
        print("   34. ❌ Sair")
        print("="*80)
    
    def get_user_choice(self):
        """Obtém escolha do usuário"""
        try:
            choice = input("\n🏦 Escolha uma opção (1-34): ").strip()
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
            self.send_account()
        elif choice == 14:
            self.send_accounting_setting()
        elif choice == 15:
            self.send_category()
        elif choice == 16:
            self.send_contact()
        elif choice == 17:
            self.send_cost_center()
        elif choice == 18:
            self.send_financial_document()
        elif choice == 19:
            self.send_journal_entry()
        elif choice == 20:
            self.send_ledger_account_resource()
        elif choice == 21:
            self.send_tax_rate()
        elif choice == 22:
            self.send_tax_type()
        elif choice == 23:
            self.send_batch_data()
        elif choice == 24:
            self.collect_with_custom_filters()
        elif choice == 25:
            self.collect_by_period()
        elif choice == 26:
            self.collect_by_amount_range()
        elif choice == 27:
            self.analyze_finance_data()
        elif choice == 28:
            self.generate_finance_report()
        elif choice == 29:
            self.list_categories()
        elif choice == 30:
            self.list_endpoints()
        elif choice == 31:
            self.show_collection_stats()
        elif choice == 32:
            self.show_sending_stats()
        elif choice == 33:
            self.test_sending()
        elif choice == 34:
            self.exit_program()
        else:
            print("❌ Opção inválida! Tente novamente.")
    
    def test_connection(self):
        """Testa conexão"""
        print("\n🔍 TESTANDO CONEXÃO...")
        print("-" * 50)
        collector_ok = self.collector.test_connection()
        sender_ok = self.senders.test_connection()
        
        if collector_ok and sender_ok:
            print("✅ Conexão completa estabelecida!")
        else:
            print("❌ Problemas na conexão!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_accounts(self):
        """Coleta contas contábeis"""
        print("\n📊 COLETANDO CONTAS CONTÁBEIS...")
        print("-" * 50)
        success = self.collector.collect_finance_category('accounts')
        if success:
            print("✅ Contas contábeis coletadas com sucesso!")
        else:
            print("❌ Erro na coleta de contas contábeis!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_accounting_settings(self):
        """Coleta configurações contábeis"""
        print("\n⚙️  COLETANDO CONFIGURAÇÕES CONTÁBEIS...")
        print("-" * 50)
        success = self.collector.collect_finance_category('accounting_settings')
        if success:
            print("✅ Configurações contábeis coletadas com sucesso!")
        else:
            print("❌ Erro na coleta de configurações contábeis!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_categories(self):
        """Coleta categorias financeiras"""
        print("\n📁 COLETANDO CATEGORIAS FINANCEIRAS...")
        print("-" * 50)
        success = self.collector.collect_finance_category('categories')
        if success:
            print("✅ Categorias financeiras coletadas com sucesso!")
        else:
            print("❌ Erro na coleta de categorias financeiras!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_contacts(self):
        """Coleta contatos financeiros"""
        print("\n👥 COLETANDO CONTATOS FINANCEIROS...")
        print("-" * 50)
        success = self.collector.collect_finance_category('contacts')
        if success:
            print("✅ Contatos financeiros coletados com sucesso!")
        else:
            print("❌ Erro na coleta de contatos financeiros!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_cost_centers(self):
        """Coleta centros de custo"""
        print("\n🏢 COLETANDO CENTROS DE CUSTO...")
        print("-" * 50)
        success = self.collector.collect_finance_category('cost_centers')
        if success:
            print("✅ Centros de custo coletados com sucesso!")
        else:
            print("❌ Erro na coleta de centros de custo!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_financial_documents(self):
        """Coleta documentos financeiros"""
        print("\n📄 COLETANDO DOCUMENTOS FINANCEIROS...")
        print("-" * 50)
        success = self.collector.collect_finance_category('financial_documents')
        if success:
            print("✅ Documentos financeiros coletados com sucesso!")
        else:
            print("❌ Erro na coleta de documentos financeiros!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_journal_entries(self):
        """Coleta lançamentos contábeis"""
        print("\n📚 COLETANDO LANÇAMENTOS CONTÁBEIS...")
        print("-" * 50)
        success = self.collector.collect_finance_category('journal_entries')
        if success:
            print("✅ Lançamentos contábeis coletados com sucesso!")
        else:
            print("❌ Erro na coleta de lançamentos contábeis!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_ledger_account_resources(self):
        """Coleta recursos de conta"""
        print("\n📊 COLETANDO RECURSOS DE CONTA...")
        print("-" * 50)
        success = self.collector.collect_finance_category('ledger_account_resources')
        if success:
            print("✅ Recursos de conta coletados com sucesso!")
        else:
            print("❌ Erro na coleta de recursos de conta!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_tax_rates(self):
        """Coleta taxas de imposto"""
        print("\n💰 COLETANDO TAXAS DE IMPOSTO...")
        print("-" * 50)
        success = self.collector.collect_finance_category('tax_rates')
        if success:
            print("✅ Taxas de imposto coletadas com sucesso!")
        else:
            print("❌ Erro na coleta de taxas de imposto!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_tax_types(self):
        """Coleta tipos de imposto"""
        print("\n📋 COLETANDO TIPOS DE IMPOSTO...")
        print("-" * 50)
        success = self.collector.collect_finance_category('tax_types')
        if success:
            print("✅ Tipos de imposto coletados com sucesso!")
        else:
            print("❌ Erro na coleta de tipos de imposto!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_all_finance(self):
        """Coleta todos os dados financeiros"""
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
    
    def send_account(self):
        """Envia conta contábil"""
        print("\n📊 ENVIANDO CONTA CONTÁBIL...")
        print("-" * 50)
        data = self.senders.create_sample_finance_data('accounts')
        success = self.senders.send_finance_data('accounts', data)
        if success:
            print("✅ Conta contábil enviada com sucesso!")
        else:
            print("❌ Erro no envio da conta contábil!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def send_accounting_setting(self):
        """Envia configuração contábil"""
        print("\n⚙️  ENVIANDO CONFIGURAÇÃO CONTÁBIL...")
        print("-" * 50)
        data = self.senders.create_sample_finance_data('accounting_settings')
        success = self.senders.send_finance_data('accounting_settings', data)
        if success:
            print("✅ Configuração contábil enviada com sucesso!")
        else:
            print("❌ Erro no envio da configuração contábil!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def send_category(self):
        """Envia categoria financeira"""
        print("\n📁 ENVIANDO CATEGORIA FINANCEIRA...")
        print("-" * 50)
        data = self.senders.create_sample_finance_data('categories')
        success = self.senders.send_finance_data('categories', data)
        if success:
            print("✅ Categoria financeira enviada com sucesso!")
        else:
            print("❌ Erro no envio da categoria financeira!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def send_contact(self):
        """Envia contato financeiro"""
        print("\n👥 ENVIANDO CONTATO FINANCEIRO...")
        print("-" * 50)
        data = self.senders.create_sample_finance_data('contacts')
        success = self.senders.send_finance_data('contacts', data)
        if success:
            print("✅ Contato financeiro enviado com sucesso!")
        else:
            print("❌ Erro no envio do contato financeiro!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def send_cost_center(self):
        """Envia centro de custo"""
        print("\n🏢 ENVIANDO CENTRO DE CUSTO...")
        print("-" * 50)
        data = self.senders.create_sample_finance_data('cost_centers')
        success = self.senders.send_finance_data('cost_centers', data)
        if success:
            print("✅ Centro de custo enviado com sucesso!")
        else:
            print("❌ Erro no envio do centro de custo!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def send_financial_document(self):
        """Envia documento financeiro"""
        print("\n📄 ENVIANDO DOCUMENTO FINANCEIRO...")
        print("-" * 50)
        data = self.senders.create_sample_finance_data('financial_documents')
        success = self.senders.send_finance_data('financial_documents', data)
        if success:
            print("✅ Documento financeiro enviado com sucesso!")
        else:
            print("❌ Erro no envio do documento financeiro!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def send_journal_entry(self):
        """Envia lançamento contábil"""
        print("\n📚 ENVIANDO LANÇAMENTO CONTÁBIL...")
        print("-" * 50)
        data = self.senders.create_sample_finance_data('journal_entries')
        success = self.senders.send_finance_data('journal_entries', data)
        if success:
            print("✅ Lançamento contábil enviado com sucesso!")
        else:
            print("❌ Erro no envio do lançamento contábil!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def send_ledger_account_resource(self):
        """Envia recurso de conta"""
        print("\n📊 ENVIANDO RECURSO DE CONTA...")
        print("-" * 50)
        data = self.senders.create_sample_finance_data('ledger_account_resources')
        success = self.senders.send_finance_data('ledger_account_resources', data)
        if success:
            print("✅ Recurso de conta enviado com sucesso!")
        else:
            print("❌ Erro no envio do recurso de conta!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def send_tax_rate(self):
        """Envia taxa de imposto"""
        print("\n💰 ENVIANDO TAXA DE IMPOSTO...")
        print("-" * 50)
        data = self.senders.create_sample_finance_data('tax_rates')
        success = self.senders.send_finance_data('tax_rates', data)
        if success:
            print("✅ Taxa de imposto enviada com sucesso!")
        else:
            print("❌ Erro no envio da taxa de imposto!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def send_tax_type(self):
        """Envia tipo de imposto"""
        print("\n📋 ENVIANDO TIPO DE IMPOSTO...")
        print("-" * 50)
        data = self.senders.create_sample_finance_data('tax_types')
        success = self.senders.send_finance_data('tax_types', data)
        if success:
            print("✅ Tipo de imposto enviado com sucesso!")
        else:
            print("❌ Erro no envio do tipo de imposto!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def send_batch_data(self):
        """Envia lote de dados"""
        print("\n🔄 ENVIANDO LOTE DE DADOS...")
        print("-" * 50)
        categories = self.senders.list_available_senders()
        print("Categorias disponíveis:")
        for i, cat in enumerate(categories, 1):
            print(f"   {i}. {cat}")
        
        try:
            choice = int(input("\nEscolha uma categoria (número): ")) - 1
            if 0 <= choice < len(categories):
                category = categories[choice]
                count = int(input("Quantos itens enviar? (padrão 3): ") or "3")
                
                data_list = []
                for i in range(count):
                    data = self.senders.create_sample_finance_data(category)
                    data['name'] = f"{data.get('name', 'Item')} {i+1}"
                    data_list.append(data)
                
                results = self.senders.send_batch_finance_data(category, data_list)
                print(f"✅ Lote enviado: {results['successful']}/{results['total']} sucessos")
            else:
                print("❌ Categoria inválida!")
        except ValueError:
            print("❌ Entrada inválida!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def collect_with_custom_filters(self):
        """Coleta com filtros personalizados"""
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
        """Coleta por período"""
        print("\n📅 COLETA POR PERÍODO")
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
        """Coleta por faixa de valores"""
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
        """Analisa dados financeiros"""
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
    
    def generate_finance_report(self):
        """Gera relatório financeiro"""
        print("\n📊 GERANDO RELATÓRIO FINANCEIRO...")
        print("-" * 50)
        report = self.collector.generate_finance_report()
        if report:
            print("✅ Relatório financeiro gerado com sucesso!")
            print(f"📊 Categorias analisadas: {len(report.get('categories', {}))}")
            print(f"📄 Arquivo salvo: data/finance/processed/relatorio_financeiro_completo.json")
        else:
            print("❌ Erro na geração do relatório!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def list_categories(self):
        """Lista categorias disponíveis"""
        print("\n📋 CATEGORIAS FINANCEIRAS DISPONÍVEIS")
        print("-" * 50)
        categories = self.collector.list_finance_categories()
        for i, category in enumerate(categories, 1):
            endpoints = self.collector.list_finance_endpoints(category)
            print(f"   {i:2d}. {category:<20} ({len(endpoints)} endpoints)")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def list_endpoints(self):
        """Lista endpoints disponíveis"""
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
    
    def show_collection_stats(self):
        """Mostra estatísticas de coleta"""
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
    
    def show_sending_stats(self):
        """Mostra estatísticas de envio"""
        print("\n📤 ESTATÍSTICAS DE ENVIO FINANCEIRO")
        print("-" * 50)
        stats = self.senders.get_sending_stats()
        print(f"📤 Total de envios: {stats['total_sends']}")
        print(f"✅ Envios bem-sucedidos: {stats['successful_sends']}")
        print(f"❌ Envios falhados: {stats['failed_sends']}")
        print(f"📊 Taxa de sucesso: {stats['success_rate']:.1f}%")
        if stats['duration']:
            print(f"⏱️  Duração: {stats['duration']}")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def test_sending(self):
        """Testa envio com dados de exemplo"""
        print("\n🧪 TESTANDO ENVIO COM DADOS DE EXEMPLO")
        print("-" * 50)
        categories = self.senders.list_available_senders()
        print("Categorias disponíveis para teste:")
        for i, cat in enumerate(categories, 1):
            print(f"   {i}. {cat}")
        
        try:
            choice = int(input("\nEscolha uma categoria (número): ")) - 1
            if 0 <= choice < len(categories):
                category = categories[choice]
                data = self.senders.create_sample_finance_data(category)
                print(f"\n📤 Testando envio de {category}...")
                print(f"📋 Dados: {data}")
                success = self.senders.send_finance_data(category, data)
                if success:
                    print(f"✅ Teste de envio de {category} bem-sucedido!")
                else:
                    print(f"❌ Teste de envio de {category} falhou!")
            else:
                print("❌ Categoria inválida!")
        except ValueError:
            print("❌ Entrada inválida!")
        input("\n⏸️  Pressione Enter para continuar...")
    
    def exit_program(self):
        """Sai do programa"""
        print("\n👋 OBRIGADO POR USAR O ULTIMATE FINANCE SYSTEM!")
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
    print("🏦 INICIANDO ULTIMATE FINANCE SYSTEM...")
    print("   Sistema Completo de Coleta e Envio de Dados Financeiros")
    
    system = UltimateFinanceSystem()
    system.run()

if __name__ == "__main__":
    main()

