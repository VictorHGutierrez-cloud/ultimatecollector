#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏦 ULTIMATE FINANCE COLLECTOR - QI 300+ EDITION
Sistema definitivo para coleta e envio de dados financeiros
Menu dedicado com filtros avançados e senders completos
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import logging
from typing import Dict, List, Optional, Any, Tuple

# Configurar encoding UTF-8 para Windows
os.environ['PYTHONIOENCODING'] = 'utf-8'
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# Carregar configurações
from dotenv import load_dotenv
load_dotenv('config/.env')

# Garantir import do pacote
try:
    from ultimate_collector.core.api_client import APIClient
    from ultimate_collector.core.config import Config
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from ultimate_collector.core.api_client import APIClient
    from ultimate_collector.core.config import Config

class UltimateFinanceCollector:
    """
    🏦 ULTIMATE FINANCE COLLECTOR - QI 300+ EDITION
    
    Sistema definitivo para coleta e envio de dados financeiros
    com menu dedicado e filtros avançados
    """
    
    def __init__(self):
        """Inicializa o coletor financeiro ultimate"""
        self.client = None
        self.config = Config()
        self.collection_stats = {
            'total_endpoints': 0,
            'categories_completed': 0,
            'total_records': 0,
            'start_time': None,
            'end_time': None
        }
        
        # Mapeamento completo de endpoints financeiros
        self.finance_endpoints = {
            # 📊 CONTAS CONTÁBEIS
            'accounts': {
                'accounts': 'finance/accounts',
                'account_balances': 'finance/account_balances',
                'account_transactions': 'finance/account_transactions',
                'account_reconciliations': 'finance/account_reconciliations'
            },
            
            # ⚙️ CONFIGURAÇÕES CONTÁBEIS
            'accounting_settings': {
                'accounting_settings': 'finance/accounting_settings',
                'fiscal_years': 'finance/fiscal_years',
                'accounting_periods': 'finance/accounting_periods',
                'chart_of_accounts': 'finance/chart_of_accounts'
            },
            
            # 📁 CATEGORIAS FINANCEIRAS
            'categories': {
                'categories': 'finance/categories',
                'category_balances': 'finance/category_balances',
                'category_analytics': 'finance/category_analytics'
            },
            
            # 👥 CONTATOS FINANCEIROS
            'contacts': {
                'contacts': 'finance/contacts',
                'contact_transactions': 'finance/contact_transactions',
                'contact_balances': 'finance/contact_balances'
            },
            
            # 🏢 CENTROS DE CUSTO
            'cost_centers': {
                'cost_centers': 'finance/cost_centers',
                'cost_center_allocations': 'finance/cost_center_allocations',
                'cost_center_analytics': 'finance/cost_center_analytics'
            },
            
            # 📄 DOCUMENTOS FINANCEIROS
            'financial_documents': {
                'financial_documents': 'finance/financial_documents',
                'invoices': 'finance/invoices',
                'receipts': 'finance/receipts',
                'bills': 'finance/bills',
                'payments': 'finance/payments'
            },
            
            # 📚 LANÇAMENTOS CONTÁBEIS
            'journal_entries': {
                'journal_entries': 'finance/journal_entries',
                'journal_lines': 'finance/journal_lines',
                'journal_approvals': 'finance/journal_approvals'
            },
            
            # 📊 RECURSOS DE CONTA
            'ledger_account_resources': {
                'ledger_account_resources': 'finance/ledger_account_resources',
                'account_mappings': 'finance/account_mappings'
            },
            
            # 💰 TAXAS DE IMPOSTO
            'tax_rates': {
                'tax_rates': 'finance/tax_rates',
                'tax_calculations': 'finance/tax_calculations',
                'tax_reports': 'finance/tax_reports'
            },
            
            # 📋 TIPOS DE IMPOSTO
            'tax_types': {
                'tax_types': 'finance/tax_types',
                'tax_categories': 'finance/tax_categories'
            }
        }
        
        # Filtros avançados disponíveis
        self.available_filters = {
            'date_range': {
                'created_at_from': 'Data de criação (início)',
                'created_at_to': 'Data de criação (fim)',
                'updated_at_from': 'Data de atualização (início)',
                'updated_at_to': 'Data de atualização (fim)'
            },
            'amount_range': {
                'amount_from': 'Valor mínimo',
                'amount_to': 'Valor máximo',
                'currency': 'Moeda'
            },
            'status': {
                'status': 'Status do documento',
                'published': 'Publicado (true/false)',
                'archived': 'Arquivado (true/false)'
            },
            'entity': {
                'legal_entity_id': 'ID da entidade legal',
                'company_id': 'ID da empresa',
                'contact_id': 'ID do contato'
            },
            'accounting': {
                'account_id': 'ID da conta',
                'cost_center_id': 'ID do centro de custo',
                'category_id': 'ID da categoria'
            }
        }
        
        # Configurar logging
        self._setup_logging()
    
    def _setup_logging(self):
        """Configura o sistema de logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/finance_api.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def test_connection(self) -> bool:
        """Testa a conexão com a API Factorial"""
        print("🔍 TESTANDO CONEXÃO FINANCEIRA")
        print("=" * 60)
        
        try:
            self.client = APIClient()
            
            print(f"📋 Configurações:")
            print(f"   API: {self.client.config.API_NAME}")
            print(f"   URL: {self.client.config.BASE_URL}")
            print(f"   Módulo: Finance")
            
            # Testar conexão com endpoint financeiro
            response = self.client.get("api/2026-07-01/resources/finance/accounts", params={"limit": 1})
            
            if response and 'data' in response:
                print("✅ Conexão financeira estabelecida com sucesso!")
                return True
            else:
                print("❌ Falha na conexão financeira")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao testar conexão: {e}")
            return False
    
    def collect_finance_category(self, category_name: str, filters: Dict = None, days_back: int = None) -> bool:
        """Coleta dados de uma categoria financeira com filtros"""
        if category_name not in self.finance_endpoints:
            print(f"❌ Categoria financeira não encontrada: {category_name}")
            return False
        
        # Inicializar cliente se necessário
        if self.client is None:
            self.client = APIClient()
        
        print(f"\n🏦 COLETANDO CATEGORIA FINANCEIRA: {category_name.upper()}")
        if filters:
            print(f"🔍 Filtros aplicados: {len(filters)} parâmetros")
        if days_back:
            print(f"📅 Filtro de data: últimos {days_back} dias")
        print("=" * 60)
        
        endpoints = self.finance_endpoints[category_name]
        successful = 0
        
        for endpoint_name, endpoint_path in endpoints.items():
            self.collection_stats['total_endpoints'] += 1
            
            if self.collect_finance_endpoint(category_name, endpoint_name,
                                           endpoint_path, filters, days_back):
                successful += 1

        print(f"\n📊 Categoria {category_name}: "
              f"{successful}/{len(endpoints)} endpoints coletados")
        
        if successful > 0:
            self.collection_stats['categories_completed'] += 1
        
        return successful > 0
    
    def collect_finance_endpoint(self, category: str, endpoint_name: str, endpoint_path: str,
                                filters: Dict = None, days_back: int = None, limit: int = 100) -> bool:
        """Coleta dados de um endpoint financeiro específico"""
        print(f"🔍 Coletando: {category}/{endpoint_name}")

        try:
            full_path = f"api/2026-07-01/resources/{endpoint_path}"

            all_records = []
            page = 1

            while True:
                params = {
                    'limit': limit,
                    'page': page
                }

                # Aplicar filtros personalizados
                if filters:
                    params.update(filters)

                # Aplicar filtro de data se especificado
                if days_back is not None:
                    start_date = (datetime.now() - timedelta(days=days_back)
                                  ).strftime('%Y-%m-%d')
                    params['created_at_from'] = start_date
                    print(f"   📅 Filtro: últimos {days_back} dias (desde {start_date})")

                response = self.client.get(full_path, params=params)

                if not response or 'data' not in response:
                    break

                data = response['data'] or []
                all_records.extend(data)

                # Se não há mais dados ou menos registros que o limite, parar
                if len(data) < limit:
                    break

                page += 1

            if not all_records:
                print("⚠️ Endpoint vazio")
                return False

            # Salvar dados
            self._save_finance_data(category, endpoint_name, all_records)
            
            print(f"✅ {len(all_records)} registros coletados")
            self.collection_stats['total_records'] += len(all_records)
            
            return True

        except Exception as e:
            print(f"❌ Erro: {endpoint_name} - {e}")
            return False
    
    def _save_finance_data(self, category: str, endpoint_name: str, data: List[Dict]) -> None:
        """Salva dados financeiros coletados"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Criar diretórios
            base_dir = Path('data/finance/raw')
            category_dir = base_dir / category
            category_dir.mkdir(parents=True, exist_ok=True)
            
            # Salvar JSON
            json_file = category_dir / f"{endpoint_name}_{timestamp}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Salvar CSV
            if data:
                df = pd.DataFrame(data)
                csv_file = category_dir / f"{endpoint_name}_{timestamp}.csv"
                df.to_csv(csv_file, index=False, encoding='utf-8')
                
                # Mostrar preview das colunas
                columns_preview = ', '.join(df.columns[:5])
                if len(df.columns) > 5:
                    columns_preview += f"... (+{len(df.columns)-5} mais)"
                
                print(f"💾 Salvos: {json_file.name} | {csv_file.name}")
                print(f"   Colunas: {columns_preview}")
            
        except Exception as e:
            print(f"❌ Erro ao salvar {endpoint_name}: {e}")
    
    def analyze_finance_data(self, category: str) -> Dict[str, Any]:
        """Analisa dados financeiros coletados"""
        print(f"📊 ANALISANDO DADOS FINANCEIROS: {category.upper()}")
        print("=" * 60)
        
        try:
            category_dir = Path(f'data/finance/raw/{category}')
            if not category_dir.exists():
                print(f"❌ Categoria {category} não encontrada")
                return {}
            
            analysis = {
                'category': category,
                'files': [],
                'total_records': 0,
                'endpoints': {},
                'financial_summary': {
                    'total_amount': 0,
                    'total_debits': 0,
                    'total_credits': 0,
                    'currencies': set(),
                    'date_range': {'min': None, 'max': None}
                }
            }
            
            for file_path in category_dir.glob('*.csv'):
                df = pd.read_csv(file_path)
                endpoint_name = file_path.stem.split('_')[0]
                
                analysis['files'].append(file_path.name)
                analysis['total_records'] += len(df)
                analysis['endpoints'][endpoint_name] = {
                    'records': len(df),
                    'columns': list(df.columns),
                    'file': file_path.name
                }
                
                # Análise financeira específica
                if 'amount_cents' in df.columns:
                    total_amount = df['amount_cents'].sum() / 100  # Converter de centavos
                    analysis['financial_summary']['total_amount'] += total_amount
                
                if 'debit_amount_cents' in df.columns:
                    total_debits = df['debit_amount_cents'].sum() / 100
                    analysis['financial_summary']['total_debits'] += total_debits
                
                if 'credit_amount_cents' in df.columns:
                    total_credits = df['credit_amount_cents'].sum() / 100
                    analysis['financial_summary']['total_credits'] += total_credits
                
                if 'currency' in df.columns:
                    analysis['financial_summary']['currencies'].update(df['currency'].unique())
                
                if 'created_at' in df.columns:
                    df['created_at'] = pd.to_datetime(df['created_at'])
                    min_date = df['created_at'].min()
                    max_date = df['created_at'].max()
                    
                    if analysis['financial_summary']['date_range']['min'] is None or min_date < analysis['financial_summary']['date_range']['min']:
                        analysis['financial_summary']['date_range']['min'] = min_date
                    
                    if analysis['financial_summary']['date_range']['max'] is None or max_date > analysis['financial_summary']['date_range']['max']:
                        analysis['financial_summary']['date_range']['max'] = max_date
                
                print(f"📄 {endpoint_name}: {len(df)} registros")
            
            # Converter set para list para JSON
            analysis['financial_summary']['currencies'] = list(analysis['financial_summary']['currencies'])
            
            print(f"\n📊 Total: {analysis['total_records']} registros em {len(analysis['files'])} arquivos")
            print(f"💰 Valor total: R$ {analysis['financial_summary']['total_amount']:,.2f}")
            print(f"📈 Débitos: R$ {analysis['financial_summary']['total_debits']:,.2f}")
            print(f"📉 Créditos: R$ {analysis['financial_summary']['total_credits']:,.2f}")
            print(f"💱 Moedas: {', '.join(analysis['financial_summary']['currencies'])}")
            
            return analysis
            
        except Exception as e:
            print(f"❌ Erro na análise: {e}")
            return {}
    
    def export_finance_data(self, category: str, format: str = 'excel') -> bool:
        """Exporta dados financeiros para Excel ou CSV"""
        print(f"📤 EXPORTANDO DADOS FINANCEIROS: {category.upper()}")
        print("=" * 60)
        
        try:
            category_dir = Path(f'data/finance/raw/{category}')
            if not category_dir.exists():
                print(f"❌ Categoria {category} não encontrada")
                return False
            
            # Criar diretório de exportação
            export_dir = Path('data/finance/processed')
            export_dir.mkdir(parents=True, exist_ok=True)
            
            if format.lower() == 'excel':
                # Exportar para Excel com múltiplas abas
                excel_file = export_dir / f"{category}_financeiro.xlsx"
                with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                    for csv_file in category_dir.glob('*.csv'):
                        df = pd.read_csv(csv_file)
                        sheet_name = csv_file.stem.split('_')[0][:31]  # Limite do Excel
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                print(f"✅ Exportado para: {excel_file}")
                
            elif format.lower() == 'csv':
                # Exportar CSV consolidado
                csv_file = export_dir / f"{category}_financeiro_consolidado.csv"
                all_data = []
                
                for csv_file_path in category_dir.glob('*.csv'):
                    df = pd.read_csv(csv_file_path)
                    df['source_endpoint'] = csv_file_path.stem.split('_')[0]
                    all_data.append(df)
                
                if all_data:
                    consolidated_df = pd.concat(all_data, ignore_index=True)
                    consolidated_df.to_csv(csv_file, index=False, encoding='utf-8')
                    print(f"✅ Exportado para: {csv_file}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro na exportação: {e}")
            return False
    
    def generate_finance_report(self) -> Dict[str, Any]:
        """Gera relatório financeiro completo"""
        print("📊 GERANDO RELATÓRIO FINANCEIRO COMPLETO")
        print("=" * 60)
        
        try:
            report = {
                'timestamp': datetime.now().isoformat(),
                'categories': {},
                'summary': {
                    'total_categories': len(self.finance_endpoints),
                    'total_endpoints': sum(len(endpoints) for endpoints in self.finance_endpoints.values()),
                    'data_directories': []
                }
            }
            
            # Analisar cada categoria financeira
            for category in self.finance_endpoints.keys():
                category_dir = Path(f'data/finance/raw/{category}')
                if category_dir.exists():
                    files = list(category_dir.glob('*.csv'))
                    total_records = 0
                    total_amount = 0
                    
                    for file_path in files:
                        try:
                            df = pd.read_csv(file_path)
                            total_records += len(df)
                            
                            # Calcular valores financeiros
                            if 'amount_cents' in df.columns:
                                total_amount += df['amount_cents'].sum() / 100
                        except:
                            pass
                    
                    report['categories'][category] = {
                        'endpoints': len(self.finance_endpoints[category]),
                        'files': len(files),
                        'total_records': total_records,
                        'total_amount': total_amount,
                        'status': 'active' if files else 'empty'
                    }
                    
                    report['summary']['data_directories'].append(category)
                else:
                    report['categories'][category] = {
                        'endpoints': len(self.finance_endpoints[category]),
                        'files': 0,
                        'total_records': 0,
                        'total_amount': 0,
                        'status': 'not_collected'
                    }
            
            # Salvar relatório
            report_file = Path('data/finance/processed/relatorio_financeiro_completo.json')
            report_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Relatório salvo: {report_file}")
            print(f"📊 {report['summary']['total_categories']} categorias analisadas")
            print(f"📄 {report['summary']['total_endpoints']} endpoints mapeados")
            
            return report
            
        except Exception as e:
            print(f"❌ Erro no relatório: {e}")
            return {}
    
    def list_finance_categories(self) -> List[str]:
        """Lista todas as categorias financeiras disponíveis"""
        return list(self.finance_endpoints.keys())
    
    def list_finance_endpoints(self, category: str) -> Dict[str, str]:
        """Lista todos os endpoints de uma categoria financeira"""
        return self.finance_endpoints.get(category, {})
    
    def get_available_filters(self) -> Dict[str, Dict[str, str]]:
        """Retorna filtros disponíveis para dados financeiros"""
        return self.available_filters
    
    def create_custom_filters(self) -> Dict[str, Any]:
        """Cria filtros personalizados através de interface"""
        print("\n🔍 CRIANDO FILTROS PERSONALIZADOS")
        print("=" * 60)
        
        filters = {}
        
        # Filtros de data
        print("\n📅 FILTROS DE DATA:")
        print("1. Últimos N dias")
        print("2. Período específico")
        print("3. Pular filtros de data")
        
        date_choice = input("Escolha uma opção (1-3): ").strip()
        
        if date_choice == '1':
            days = input("Últimos quantos dias? (padrão 30): ").strip()
            if days.isdigit():
                start_date = (datetime.now() - timedelta(days=int(days))).strftime('%Y-%m-%d')
                filters['created_at_from'] = start_date
                print(f"✅ Filtro: últimos {days} dias (desde {start_date})")
        
        elif date_choice == '2':
            start_date = input("Data início (YYYY-MM-DD): ").strip()
            end_date = input("Data fim (YYYY-MM-DD): ").strip()
            if start_date:
                filters['created_at_from'] = start_date
            if end_date:
                filters['created_at_to'] = end_date
            print(f"✅ Filtro: período {start_date} a {end_date}")
        
        # Filtros de valor
        print("\n💰 FILTROS DE VALOR:")
        amount_from = input("Valor mínimo (deixe vazio para pular): ").strip()
        amount_to = input("Valor máximo (deixe vazio para pular): ").strip()
        
        if amount_from:
            try:
                filters['amount_from'] = float(amount_from) * 100  # Converter para centavos
                print(f"✅ Valor mínimo: R$ {amount_from}")
            except ValueError:
                print("❌ Valor inválido")
        
        if amount_to:
            try:
                filters['amount_to'] = float(amount_to) * 100  # Converter para centavos
                print(f"✅ Valor máximo: R$ {amount_to}")
            except ValueError:
                print("❌ Valor inválido")
        
        # Filtros de status
        print("\n📋 FILTROS DE STATUS:")
        published = input("Apenas publicados? (s/N): ").strip().lower()
        if published == 's':
            filters['published'] = 'true'
            print("✅ Apenas documentos publicados")
        
        archived = input("Incluir arquivados? (s/N): ").strip().lower()
        if archived == 'n':
            filters['archived'] = 'false'
            print("✅ Excluindo documentos arquivados")
        
        print(f"\n📊 Total de filtros criados: {len(filters)}")
        return filters

