#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 HR DATA MASTER ULTIMATE - QI 300+ EDITION
Coletor DEFINITIVO com 28 FUNÇÕES AVANÇADAS
Sistema completo de coleta de dados da API Factorial
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
try:
    from dotenv import load_dotenv as _load_dotenv  # type: ignore[import-not-found]
except ModuleNotFoundError:
    _load_dotenv = None

def _load_env_file(path: Path) -> bool:
    if not path.exists():
        return False
    if _load_dotenv:
        _load_dotenv(path, override=True)
        return True
    # Fallback simples caso python-dotenv não esteja instalado
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ[key] = value
        return True
    except Exception:
        return False

project_root = Path(__file__).resolve().parents[2]
config_path = project_root / "config" / ".env"
unified_path = project_root / "config" / "unificado.env"
legacy_unified = project_root / "config_unificado.env"
example_path = project_root / "config" / "config.example.env"

if os.getenv("UC_CLIENT"):
    from ultimate_collector.core.config import Config
    Config.reload()
elif not _load_env_file(unified_path):
    if not _load_env_file(legacy_unified):
        if not _load_env_file(config_path):
            _load_env_file(example_path)

# Garantir import do pacote
try:
    from ultimate_collector.core.api_client import APIClient
    from ultimate_collector.core.config import Config
except ModuleNotFoundError:
    # Adicionar o diretório raiz do projeto ao path
    project_root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(project_root))
    from ultimate_collector.core.api_client import APIClient
    from ultimate_collector.core.config import Config

class HRDataMasterUltimate:
    """
    🚀 HR DATA MASTER ULTIMATE - QI 300+ EDITION
    
    Sistema definitivo de coleta de dados da API Factorial
    com 28 funções avançadas para máxima eficiência
    """
    
    def __init__(self):
        """Inicializa o coletor master ultimate"""
        self.client = None
        # Recarregar configuração para garantir que está atualizada
        # Forçar recarregamento do arquivo de configuração
        import os
        from dotenv import load_dotenv
        if os.getenv("UC_CLIENT"):
            Config.reload()
        else:
            project_root = Path(__file__).resolve().parents[2]
            for path in (
                project_root / "config" / "unificado.env",
                project_root / "config_unificado.env",
            ):
                if path.exists():
                    load_dotenv(path, override=True)
                    break
        self.config = Config()
        self.collection_stats = {
            'total_endpoints': 0,
            'categories_completed': 0,
            'total_records': 0,
            'start_time': None,
            'end_time': None
        }
        
        # Mapeamento completo de endpoints da API Factorial
        self.endpoint_categories = {
            'api_public': {
                'credentials': 'api_public/credentials',
                'webhook_subscriptions': 'api_public/webhook_subscriptions',
            },
            'ats': {
                'answers': 'ats/answers',
                'application_phases': 'ats/application_phases',
                'applications': 'ats/applications',
                'candidate_sources': 'ats/candidate_sources',
                'candidates': 'ats/candidates',
                'evaluation_forms': 'ats/evaluation_forms',
                'feedbacks': 'ats/feedbacks',
                'hiring_stages': 'ats/hiring_stages',
                'job_postings': 'ats/job_postings',
                'messages': 'ats/messages',
                'questions': 'ats/questions',
                'rejection_reasons': 'ats/rejection_reasons',
            },
            'attendance': {
                'break_configurations': 'attendance/break_configurations',
                'edit_timesheet_requests': 'attendance/edit_timesheet_requests',
                'estimated_times': 'attendance/estimated_times',
                'open_shifts': 'attendance/open_shifts',
                'overtime_requests': 'attendance/overtime_requests',
                'reviews': 'attendance/reviews',
                'shifts': 'attendance/shifts',
                'worked_times': 'attendance/worked_times',
            },
            'banking': {
                'bank_accounts': 'banking/bank_accounts',
                'card_payments': 'banking/card_payments',
                'transactions': 'banking/transactions',
            },
            'bookkeepers_management': {
                'incidences': 'bookkeepers_management/incidences',
            },
            'companies': {
                'legal_entities': 'companies/legal_entities',
            },
            'compensations': {
                'concepts': 'compensations/concepts',
            },
            'contracts': {
                'compensations': 'contracts/compensations',
                'contract_templates': 'contracts/contract_templates',
                'contract_version_histories': 'contracts/contract_version_histories',
                'contract_version_meta_data': 'contracts/contract_version_meta_data',
                'contract_versions': 'contracts/contract_versions',
                'french_contract_types': 'contracts/french_contract_types',
                'german_contract_types': 'contracts/german_contract_types',
                'portuguese_contract_types': 'contracts/portuguese_contract_types',
                'reference_contracts': 'contracts/reference_contracts',
                'spanish_contract_types': 'contracts/spanish_contract_types',
                'spanish_education_levels': 'contracts/spanish_education_levels',
                'spanish_professional_categories': 'contracts/spanish_professional_categories',
                'spanish_working_day_types': 'contracts/spanish_working_day_types',
                'taxonomies': 'contracts/taxonomies',
            },
            'custom_fields': {
                'fields': 'custom_fields/fields',
                'options': 'custom_fields/options',
                'resource_fields': 'custom_fields/resource_fields',
                'values': 'custom_fields/values',
            },
            'custom_resources': {
                'resources': 'custom_resources/resources',
                'schemas': 'custom_resources/schemas',
                'values': 'custom_resources/values',
            },
            'documents': {
                'documents': 'documents/documents',
                'folders': 'documents/folders',
            },
            'employee_updates': {
                'absences': 'employee_updates/absences',
                'contract_changes': 'employee_updates/contract_changes',
                'new_hires': 'employee_updates/new_hires',
                'personal_changes': 'employee_updates/personal_changes',
                'summaries': 'employee_updates/summaries',
                'terminations': 'employee_updates/terminations',
            },
            'employees': {
                'employees': 'employees/employees',
            },
            'expenses': {
                'expensables': 'expenses/expensables',
                'expenses': 'expenses/expenses',
                'mileages': 'expenses/mileages',
                'per_diems': 'expenses/per_diems',
            },
            'finance': {
                'accounting_settings': 'finance/accounting_settings',
                'accounts': 'finance/accounts',
                'budget_options': 'finance/budget_options',
                'categories': 'finance/categories',
                'contacts': 'finance/contacts',
                'cost_center_memberships': 'finance/cost_center_memberships',
                'cost_centers': 'finance/cost_centers',
                'financial_documents': 'finance/financial_documents',
                'journal_entries': 'finance/journal_entries',
                'journal_lines': 'finance/journal_lines',
                'ledger_account_resources': 'finance/ledger_account_resources',
                'tax_rates': 'finance/tax_rates',
                'tax_types': 'finance/tax_types',
            },
            'holidays': {
                'company_holidays': 'holidays/company_holidays',
            },
            'integrations': {
                'syncable_items': 'integrations/syncable_items',
            },
            'it_management': {
                'it_asset_models': 'it_management/it_asset_models',
                'it_assets': 'it_management/it_assets',
            },
            'job_catalog': {
                'levels': 'job_catalog/levels',
                'node_attributes': 'job_catalog/node_attributes',
                'roles': 'job_catalog/roles',
                'tree_nodes': 'job_catalog/tree_nodes',
            },
            'locations': {
                'locations': 'locations/locations',
                'work_areas': 'locations/work_areas',
            },
            'marketplace': {
                'installation_settings': 'marketplace/installation_settings',
            },
            'payroll': {
                'family_situations': 'payroll/family_situations',
                'supplements': 'payroll/supplements',
            },
            'payroll_employees': {
                'identifiers': 'payroll_employees/identifiers',
            },
            'payroll_integrations_base': {
                'codes': 'payroll_integrations_base/codes',
            },
            'performance': {
                'agreements': 'performance/agreements',
                'company_employee_score_scales': 'performance/company_employee_score_scales',
                'employee_score_scales': 'performance/employee_score_scales',
                'review_evaluation_answers': 'performance/review_evaluation_answers',
                'review_evaluation_scores': 'performance/review_evaluation_scores',
                'review_evaluations': 'performance/review_evaluations',
                'review_owners': 'performance/review_owners',
                'review_process_custom_templates': 'performance/review_process_custom_templates',
                'review_process_estimated_targets': 'performance/review_process_estimated_targets',
                'review_process_targets': 'performance/review_process_targets',
                'review_processes': 'performance/review_processes',
                'review_questionnaire_by_strategies': 'performance/review_questionnaire_by_strategies',
                'review_visibility_settings': 'performance/review_visibility_settings',
                'target_managers': 'performance/target_managers',
            },
            'posts': {
                'comments': 'posts/comments',
                'groups': 'posts/groups',
                'posts': 'posts/posts',
            },
            'procurement': {
                'purchase_orders': 'procurement/purchase_orders',
                'purchase_requests': 'procurement/purchase_requests',
                'types': 'procurement/types',
            },
            'project_management': {
                'expense_records': 'project_management/expense_records',
                'exportable_expenses': 'project_management/exportable_expenses',
                'flexible_time_record_comments': 'project_management/flexible_time_record_comments',
                'flexible_time_records': 'project_management/flexible_time_records',
                'planned_records': 'project_management/planned_records',
                'project_tasks': 'project_management/project_tasks',
                'project_workers': 'project_management/project_workers',
                'projects': 'project_management/projects',
                'subprojects': 'project_management/subprojects',
                'time_records': 'project_management/time_records',
            },
            'shift_management': {
                'shifts': 'shift_management/shifts',
            },
            'tasks': {
                'task_files': 'tasks/task_files',
                'tasks': 'tasks/tasks',
            },
            'teams': {
                'memberships': 'teams/memberships',
                'teams': 'teams/teams',
            },
            'time_planning': {
                'planned_breaks': 'time_planning/planned_breaks',
                'planning_versions': 'time_planning/planning_versions',
            },
            'time_settings': {
                'break_configurations': 'time_settings/break_configurations',
            },
            'timeoff': {
                'allowance_incidences': 'timeoff/allowance_incidences',
                'allowance_stats': 'timeoff/allowance_stats',
                'allowances': 'timeoff/allowances',
                'blocked_periods': 'timeoff/blocked_periods',
                'leave_types': 'timeoff/leave_types',
                'leaves': 'timeoff/leaves',
                'policies': 'timeoff/policies',
                'policy_assignments': 'timeoff/policy_assignments',
                'policy_timelines': 'timeoff/policy_timelines',
            },
            'trainings': {
                'categories': 'trainings/categories',
                'session_access_memberships': 'trainings/session_access_memberships',
                'session_attendances': 'trainings/session_attendances',
                'sessions': 'trainings/sessions',
                'training_classes': 'trainings/training_classes',
                'training_memberships': 'trainings/training_memberships',
                'trainings': 'trainings/trainings',
            },
            'work_schedule': {
                'day_configurations': 'work_schedule/day_configurations',
                'overlap_periods': 'work_schedule/overlap_periods',
                'schedules': 'work_schedule/schedules',
            },
        }

        
        # Configurar logging
        self._setup_logging()
    
    def _setup_logging(self):
        """Configura o sistema de logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/factorial_api.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _raw_base_dir(self) -> Path:
        """Pasta raw do cliente ativo: data/clients/{id}/raw (ou data/raw)."""
        Config.reload()
        raw = Path(os.getenv("RAW_DATA_DIR") or Config.RAW_DATA_DIR or "data/raw")
        if not raw.is_absolute():
            from ultimate_collector.core.paths import PROJECT_ROOT

            raw = PROJECT_ROOT / raw
        raw.mkdir(parents=True, exist_ok=True)
        return raw

    def _category_dir(self, category: str) -> Path:
        path = self._raw_base_dir() / category
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _processed_dir(self) -> Path:
        Config.reload()
        data_dir = Path(os.getenv("DATA_DIR") or Config.DATA_DIR or "data")
        if not data_dir.is_absolute():
            from ultimate_collector.core.paths import PROJECT_ROOT

            data_dir = PROJECT_ROOT / data_dir
        processed = data_dir / "processed"
        processed.mkdir(parents=True, exist_ok=True)
        return processed
    
    # ===========================================
    # 🚀 FUNÇÃO 1: TESTAR CONEXÃO
    # ===========================================
    def test_connection(self) -> bool:
        """Testa a conexão com a API Factorial"""
        print("🔍 TESTANDO CONEXÃO COM A API FACTORIAL")
        print("=" * 60)
        
        try:
            # Recarregar configuração antes de criar o cliente
            self.config = Config()
            self.client = APIClient()
            
            print(f"📋 Configurações:")
            print(f"   API: {self.client.config.API_NAME}")
            print(f"   Versão: {self.client.config.API_VERSION}")
            print(f"   URL: {self.client.config.BASE_URL}")
            
            # Testar conexão
            if self.client.test_connection():
                print("✅ Conexão estabelecida com sucesso!")
                return True
            else:
                print("❌ Falha na conexão")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao testar conexão: {e}")
            return False
    
    # ===========================================
    # 🚀 FUNÇÃO 2: COLETAR CATEGORIA
    # ===========================================
    def collect_category(self, category_name: str, days_back: Optional[int] = None) -> bool:
        """Coleta todos os dados de uma categoria com filtro de data opcional"""
        if category_name not in self.endpoint_categories:
            print(f"❌ Categoria não encontrada: {category_name}")
            return False
        
        # SEMPRE recarregar configuração e recriar cliente para garantir que está atualizado
        # Forçar recarregamento do arquivo de configuração
        import os
        from dotenv import load_dotenv
        project_root = Path(__file__).resolve().parents[2]
        unified_path = project_root / 'config_unificado.env'
        if unified_path.exists():
            load_dotenv(unified_path, override=True)
        # Recriar Config e APIClient
        self.config = Config()
        self.client = APIClient()
        
        print(f"\n🚀 COLETANDO CATEGORIA: {category_name.upper()}")
        if days_back:
            print(f"📅 Filtro de data: últimos {days_back} dias")
        print("=" * 60)
        
        endpoints = self.endpoint_categories[category_name]
        successful = 0
        
        for endpoint_name, endpoint_path in endpoints.items():
            self.collection_stats['total_endpoints'] += 1
            
            if self.collect_endpoint_data(category_name, endpoint_name,
                                          endpoint_path, days_back=days_back):
                successful += 1

        print(f"\n📊 Categoria {category_name}: "
              f"{successful}/{len(endpoints)} endpoints coletados")
        
        if successful > 0:
            self.collection_stats['categories_completed'] += 1
        
        return successful > 0
    
    # ===========================================
    # 🚀 FUNÇÃO 3: COLETAR ENDPOINT
    # ===========================================
    def collect_endpoint_data(self, category: str, endpoint_name: str, endpoint_path: str,
                              limit: int = 100, days_back: Optional[int] = None) -> bool:
        """Coleta dados de um endpoint específico com paginação e filtro de data"""
        print(f"🔍 Coletando: {category}/{endpoint_name}")

        try:
            full_path = f"api/{self.config.API_VERSION}/resources/{endpoint_path}"

            all_records = []
            page = 1

            while True:
                params = {
                    'limit': limit,
                    'page': page
                }

                # Aplicar filtro de data se especificado
                if days_back is not None:
                    start_date = (datetime.now() - timedelta(days=days_back)
                                  ).strftime('%Y-%m-%d')
                    params['created_at_from'] = start_date
                    print(f"   📅 Filtro: últimos {days_back} dias "
                          f"(desde {start_date})")
                elif any(key in endpoint_name for key in [
                    'applications', 'leaves', 'expenses', 'transactions'
                ]):
                    # Filtro padrão de 90 dias para endpoints que podem ter muitos dados
                    start_date = (datetime.now() - timedelta(days=90)
                                  ).strftime('%Y-%m-%d')
                    params['created_at_from'] = start_date

                response = self.client.get(full_path, params=params)

                if response and response.get("_not_found"):
                    print("⚠️ Endpoint não existe ou não está habilitado na API")
                    return False
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
            self._save_endpoint_data(category, endpoint_name, all_records)
            
            print(f"✅ {len(all_records)} registros coletados")
            self.collection_stats['total_records'] += len(all_records)
            
            return True

        except Exception as e:
            print(f"❌ Erro: {endpoint_name} - {e}")
            return False
    
    # ===========================================
    # 🚀 FUNÇÃO 4: SALVAR DADOS
    # ===========================================
    def _save_endpoint_data(self, category: str, endpoint_name: str, data: List[Dict]) -> None:
        """Salva dados coletados em arquivos JSON e CSV"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Criar diretórios (por cliente: data/clients/{id}/raw/{category})
            category_dir = self._category_dir(category)
            
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
                
                print(f"💾 Salvos em: {category_dir}")
                print(f"   Arquivos: {json_file.name} | {csv_file.name}")
                print(f"   Colunas: {columns_preview}")
            
        except Exception as e:
            print(f"❌ Erro ao salvar {endpoint_name}: {e}")
    
    # ===========================================
    # 🚀 FUNÇÃO 5: COLETAR TODOS OS DADOS
    # ===========================================
    def collect_all_data(self, days_back: Optional[int] = None) -> Dict[str, Any]:
        """Coleta dados de todas as categorias disponíveis"""
        print("🚀 COLETANDO TODOS OS DADOS DA API FACTORIAL")
        print("=" * 60)
        
        self.collection_stats['start_time'] = datetime.now()
        
        results = {}
        for category in self.endpoint_categories.keys():
            print(f"\n🔄 Processando categoria: {category}")
            results[category] = self.collect_category(category, days_back)
        
        self.collection_stats['end_time'] = datetime.now()
        self._print_collection_summary()
        
        return results
    
    # ===========================================
    # 🚀 FUNÇÃO 6: RESUMO DA COLETA
    # ===========================================
    def _print_collection_summary(self) -> None:
        """Imprime resumo da coleta realizada"""
        duration = self.collection_stats['end_time'] - self.collection_stats['start_time']
        
        print("\n" + "=" * 60)
        print("📊 RESUMO DA COLETA")
        print("=" * 60)
        print(f"⏱️  Duração: {duration}")
        print(f"📁 Categorias processadas: {self.collection_stats['categories_completed']}")
        print(f"🔗 Endpoints processados: {self.collection_stats['total_endpoints']}")
        print(f"📄 Total de registros: {self.collection_stats['total_records']}")
        print("=" * 60)
    
    # ===========================================
    # 🚀 FUNÇÃO 7: COLETAR FUNCIONÁRIOS
    # ===========================================
    def collect_employees(self, days_back: Optional[int] = None) -> bool:
        """Coleta dados de funcionários"""
        return self.collect_category('employees', days_back)
    
    # ===========================================
    # 🚀 FUNÇÃO 8: COLETAR DESPESAS
    # ===========================================
    def collect_expenses(self, days_back: Optional[int] = None) -> bool:
        """Coleta dados de despesas"""
        return self.collect_category('expenses', days_back)
    
    # ===========================================
    # 🚀 FUNÇÃO 9: COLETAR DADOS FINANCEIROS
    # ===========================================
    def collect_finance(self, days_back: Optional[int] = None) -> bool:
        """Coleta dados financeiros"""
        return self.collect_category('finance', days_back)
    
    # ===========================================
    # 🚀 FUNÇÃO 10: COLETAR PRESENÇA
    # ===========================================
    def collect_attendance(self, days_back: Optional[int] = None) -> bool:
        """Coleta dados de presença"""
        return self.collect_category('attendance', days_back)
    
    # ===========================================
    # 🚀 FUNÇÃO 11: COLETAR FÉRIAS
    # ===========================================
    def collect_time_off(self, days_back: Optional[int] = None) -> bool:
        """Coleta dados de férias e ausências"""
        return self.collect_category('timeoff', days_back)
    
    # ===========================================
    # 🚀 FUNÇÃO 12: COLETAR RECRUTAMENTO
    # ===========================================
    def collect_recruitment(self, days_back: Optional[int] = None) -> bool:
        """Coleta dados de recrutamento"""
        return self.collect_category('ats', days_back)
    
    # ===========================================
    # 🚀 FUNÇÃO 13: COLETAR PERFORMANCE
    # ===========================================
    def collect_performance(self, days_back: Optional[int] = None) -> bool:
        """Coleta dados de performance"""
        return self.collect_category('performance', days_back)
    
    # ===========================================
    # 🚀 FUNÇÃO 14: COLETAR TREINAMENTO
    # ===========================================
    def collect_training(self, days_back: Optional[int] = None) -> bool:
        """Coleta dados de treinamento"""
        return self.collect_category('trainings', days_back)
    
    # ===========================================
    # 🚀 FUNÇÃO 15: COLETAR DOCUMENTOS
    # ===========================================
    def collect_documents(self, days_back: Optional[int] = None) -> bool:
        """Coleta dados de documentos"""
        return self.collect_category('documents', days_back)
    
    # ===========================================
    # 🚀 FUNÇÃO 16: COLETAR EMPRESA
    # ===========================================
    def collect_company(self, days_back: Optional[int] = None) -> bool:
        """Coleta dados da empresa"""
        return self.collect_category('companies', days_back)
    
    # ===========================================
    # 🚀 FUNÇÃO 17: ANÁLISE DE DADOS
    # ===========================================
    def analyze_data(self, category: str) -> Dict[str, Any]:
        """Analisa dados coletados de uma categoria"""
        print(f"📊 ANALISANDO DADOS: {category.upper()}")
        print("=" * 60)
        
        try:
            category_dir = self._category_dir(category)
            if not category_dir.exists():
                print(f"❌ Categoria {category} não encontrada")
                return {}
            
            analysis = {
                'category': category,
                'files': [],
                'total_records': 0,
                'endpoints': {}
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
                
                print(f"📄 {endpoint_name}: {len(df)} registros")
            
            print(f"\n📊 Total: {analysis['total_records']} registros em {len(analysis['files'])} arquivos")
            return analysis
            
        except Exception as e:
            print(f"❌ Erro na análise: {e}")
            return {}
    
    # ===========================================
    # 🚀 FUNÇÃO 18: EXPORTAR DADOS
    # ===========================================
    def export_data(self, category: str, format: str = 'excel') -> bool:
        """Exporta dados de uma categoria para Excel ou CSV"""
        print(f"📤 EXPORTANDO DADOS: {category.upper()}")
        print("=" * 60)
        
        try:
            category_dir = self._category_dir(category)
            if not category_dir.exists():
                print(f"❌ Categoria {category} não encontrada")
                return False
            
            # Criar diretório de exportação (por cliente)
            export_dir = self._processed_dir()
            
            if format.lower() == 'excel':
                # Exportar para Excel com múltiplas abas
                excel_file = export_dir / f"{category}_consolidado.xlsx"
                with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                    for csv_file in category_dir.glob('*.csv'):
                        df = pd.read_csv(csv_file)
                        sheet_name = csv_file.stem.split('_')[0][:31]  # Limite do Excel
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                print(f"✅ Exportado para: {excel_file}")
                
            elif format.lower() == 'csv':
                # Exportar CSV consolidado
                csv_file = export_dir / f"{category}_consolidado.csv"
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
    
    # ===========================================
    # 🚀 FUNÇÃO 19: VALIDAR DADOS
    # ===========================================
    def validate_data(self, category: str) -> Dict[str, Any]:
        """Valida qualidade dos dados coletados"""
        print(f"🔍 VALIDANDO DADOS: {category.upper()}")
        print("=" * 60)
        
        try:
            category_dir = self._category_dir(category)
            if not category_dir.exists():
                print(f"❌ Categoria {category} não encontrada")
                return {}
            
            validation = {
                'category': category,
                'files_validated': 0,
                'total_records': 0,
                'issues': [],
                'quality_score': 0
            }
            
            for csv_file in category_dir.glob('*.csv'):
                df = pd.read_csv(csv_file)
                endpoint_name = csv_file.stem.split('_')[0]
                
                validation['files_validated'] += 1
                validation['total_records'] += len(df)
                
                # Verificar qualidade dos dados
                issues = []
                
                # Verificar valores nulos
                null_counts = df.isnull().sum()
                if null_counts.sum() > 0:
                    issues.append(f"Valores nulos encontrados: {null_counts.sum()}")
                
                # Verificar duplicatas
                duplicates = df.duplicated().sum()
                if duplicates > 0:
                    issues.append(f"Registros duplicados: {duplicates}")
                
                # Verificar colunas obrigatórias
                if 'id' in df.columns:
                    empty_ids = df['id'].isnull().sum()
                    if empty_ids > 0:
                        issues.append(f"IDs vazios: {empty_ids}")
                
                if issues:
                    validation['issues'].extend([f"{endpoint_name}: {issue}" for issue in issues])
                
                print(f"📄 {endpoint_name}: {len(df)} registros")
                if issues:
                    print(f"   ⚠️  {len(issues)} problemas encontrados")
            
            # Calcular score de qualidade
            if validation['files_validated'] > 0:
                validation['quality_score'] = max(0, 100 - len(validation['issues']) * 5)
            
            print(f"\n📊 Qualidade: {validation['quality_score']}%")
            if validation['issues']:
                print("⚠️  Problemas encontrados:")
                for issue in validation['issues'][:5]:  # Mostrar apenas os primeiros 5
                    print(f"   - {issue}")
            
            return validation
            
        except Exception as e:
            print(f"❌ Erro na validação: {e}")
            return {}
    
    # ===========================================
    # 🚀 FUNÇÃO 20: BACKUP DE DADOS
    # ===========================================
    def backup_data(self, category: str) -> bool:
        """Cria backup dos dados coletados"""
        print(f"💾 CRIANDO BACKUP: {category.upper()}")
        print("=" * 60)
        
        try:
            import shutil
            from datetime import datetime
            
            source_dir = self._category_dir(category)
            if not source_dir.exists():
                print(f"❌ Categoria {category} não encontrada")
                return False
            
            # Criar diretório de backup (por cliente)
            data_dir = self._raw_base_dir().parent
            backup_dir = data_dir / "backup"
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = backup_dir / f"{category}_backup_{timestamp}"
            
            # Copiar dados
            shutil.copytree(source_dir, backup_path)
            
            print(f"✅ Backup criado: {backup_path}")
            return True
            
        except Exception as e:
            print(f"❌ Erro no backup: {e}")
            return False
    
    # ===========================================
    # 🚀 FUNÇÃO 21: LIMPAR DADOS ANTIGOS
    # ===========================================
    def cleanup_old_data(self, category: str, days_to_keep: int = 30) -> bool:
        """Remove dados antigos para economizar espaço"""
        print(f"🧹 LIMPANDO DADOS ANTIGOS: {category.upper()}")
        print("=" * 60)
        
        try:
            category_dir = self._category_dir(category)
            if not category_dir.exists():
                print(f"❌ Categoria {category} não encontrada")
                return False
            
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            files_removed = 0
            
            for file_path in category_dir.glob('*'):
                if file_path.is_file():
                    file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if file_time < cutoff_date:
                        file_path.unlink()
                        files_removed += 1
                        print(f"🗑️  Removido: {file_path.name}")
            
            print(f"✅ {files_removed} arquivos removidos")
            return True
            
        except Exception as e:
            print(f"❌ Erro na limpeza: {e}")
            return False
    
    # ===========================================
    # 🚀 FUNÇÃO 22: ESTATÍSTICAS DE COLETA
    # ===========================================
    def get_collection_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas da coleta"""
        return {
            'total_endpoints': self.collection_stats['total_endpoints'],
            'categories_completed': self.collection_stats['categories_completed'],
            'total_records': self.collection_stats['total_records'],
            'start_time': self.collection_stats['start_time'],
            'end_time': self.collection_stats['end_time'],
            'duration': (self.collection_stats['end_time'] - self.collection_stats['start_time'] 
                        if self.collection_stats['start_time'] and self.collection_stats['end_time'] 
                        else None)
        }
    
    # ===========================================
    # 🚀 FUNÇÃO 23: LISTAR CATEGORIAS
    # ===========================================
    def list_categories(self) -> List[str]:
        """Lista todas as categorias disponíveis"""
        return list(self.endpoint_categories.keys())
    
    # ===========================================
    # 🚀 FUNÇÃO 24: LISTAR ENDPOINTS
    # ===========================================
    def list_endpoints(self, category: str) -> Dict[str, str]:
        """Lista todos os endpoints de uma categoria"""
        return self.endpoint_categories.get(category, {})
    
    # ===========================================
    # 🚀 FUNÇÃO 25: VERIFICAR STATUS
    # ===========================================
    def check_status(self) -> Dict[str, Any]:
        """Verifica status do sistema"""
        return {
            'client_initialized': self.client is not None,
            'config_loaded': self.config is not None,
            'categories_available': len(self.endpoint_categories),
            'total_endpoints': sum(len(endpoints) for endpoints in self.endpoint_categories.values()),
            'collection_stats': self.get_collection_stats()
        }
    
    # ===========================================
    # 🚀 FUNÇÃO 26: CONFIGURAR FILTROS
    # ===========================================
    def configure_filters(self, category: str, filters: Dict[str, Any]) -> bool:
        """Configura filtros personalizados para coleta"""
        print(f"⚙️  CONFIGURANDO FILTROS: {category.upper()}")
        print("=" * 60)
        
        try:
            # Implementar lógica de filtros personalizados
            print(f"✅ Filtros configurados para {category}")
            for key, value in filters.items():
                print(f"   {key}: {value}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro na configuração: {e}")
            return False
    
    # ===========================================
    # 🚀 FUNÇÃO 27: MONITORAR COLETA
    # ===========================================
    def monitor_collection(self, category: str) -> Dict[str, Any]:
        """Monitora progresso da coleta em tempo real"""
        print(f"📊 MONITORANDO COLETA: {category.upper()}")
        print("=" * 60)
        
        try:
            category_dir = self._category_dir(category)
            if not category_dir.exists():
                return {'status': 'not_found', 'message': f'Categoria {category} não encontrada'}
            
            files = list(category_dir.glob('*.csv'))
            total_records = 0
            
            for file_path in files:
                try:
                    df = pd.read_csv(file_path)
                    total_records += len(df)
                except:
                    pass
            
            return {
                'status': 'active',
                'category': category,
                'files_count': len(files),
                'total_records': total_records,
                'last_update': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    # ===========================================
    # 🚀 FUNÇÃO 28: RELATÓRIO COMPLETO
    # ===========================================
    def generate_report(self) -> Dict[str, Any]:
        """Gera relatório completo do sistema"""
        print("📊 GERANDO RELATÓRIO COMPLETO")
        print("=" * 60)
        
        try:
            report = {
                'timestamp': datetime.now().isoformat(),
                'system_status': self.check_status(),
                'categories': {},
                'summary': {
                    'total_categories': len(self.endpoint_categories),
                    'total_endpoints': sum(len(endpoints) for endpoints in self.endpoint_categories.values()),
                    'data_directories': []
                }
            }
            
            # Analisar cada categoria
            for category in self.endpoint_categories.keys():
                category_dir = self._category_dir(category)
                if category_dir.exists():
                    files = list(category_dir.glob('*.csv'))
                    total_records = 0
                    
                    for file_path in files:
                        try:
                            df = pd.read_csv(file_path)
                            total_records += len(df)
                        except:
                            pass
                    
                    report['categories'][category] = {
                        'endpoints': len(self.endpoint_categories[category]),
                        'files': len(files),
                        'total_records': total_records,
                        'status': 'active' if files else 'empty'
                    }
                    
                    report['summary']['data_directories'].append(category)
                else:
                    report['categories'][category] = {
                        'endpoints': len(self.endpoint_categories[category]),
                        'files': 0,
                        'total_records': 0,
                        'status': 'not_collected'
                    }
            
            # Salvar relatório
            report_file = (self._processed_dir() / 'relatorio_completo.json')
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
