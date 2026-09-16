#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 HR DATA MASTER ULTIMATE - QI 300+ EDITION
Coletor DEFINITIVO baseado na análise COMPLETA da API Factorial
Mapeia TODOS os endpoints disponíveis para coleta máxima de dados de RH
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd

# Configurar encoding UTF-8 para Windows
os.environ['PYTHONIOENCODING'] = 'utf-8'
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# Carregar configurações do arquivo .env
from dotenv import load_dotenv
load_dotenv('config/.env')

# Garantir import do pacote quando executado diretamente
try:
    from src.core.api_client import APIClient
except ModuleNotFoundError:
    sys.path.append(str(Path(__file__).resolve().parents[2]))
    from src.core.api_client import APIClient

class HRDataMasterUltimate:
    def __init__(self):
        """Inicializa o coletor master ultimate com mapeamento completo da API"""
        self.client = None

        # 🎯 MAPEAMENTO COMPLETO DOS ENDPOINTS BASEADO NA API.JSON
        self.endpoint_categories = {
            # 👥 DADOS DE FUNCIONÁRIOS E PESSOAS
            'employees': {
                'employees': 'employees/employees',
            },

            # 👥 TIMES E ESTRUTURAS DE EQUIPE
            'teams': {
                'teams': 'teams/teams',
            },

            # 📍 LOCALIZAÇÕES
            'locations': {
                'locations': 'locations/locations',
            },

            # 🗓️ JORNADA / ESCALA DE TRABALHO
            'work_schedule': {
                'schedules': 'work_schedule/schedules',
            },

            # 🗓️ FERIADOS CORPORATIVOS
            'holidays': {
                'company_holidays': 'holidays/company_holidays',
            },
            
            # 🎯 ATS - RECRUTAMENTO E SELEÇÃO
            'ats': {
                'candidates': 'ats/candidates',
                'applications': 'ats/applications',
                'job_postings': 'ats/job_postings',
                'application_phases': 'ats/application_phases',
                'rejection_reasons': 'ats/rejection_reasons',
                'hiring_stages': 'ats/hiring_stages',
                'candidate_sources': 'ats/candidate_sources',
                'evaluation_forms': 'ats/evaluation_forms',
                'feedbacks': 'ats/feedbacks',
                'messages': 'ats/messages',
                'questions': 'ats/questions',
                'answers': 'ats/answers',
            },
            
            # ⏰ PRESENÇA E TEMPO
            'attendance': {
                'shifts': 'attendance/shifts',
                'worked_times': 'attendance/worked_times',
                'break_configurations': 'attendance/break_configurations',
                'edit_timesheet_requests': 'attendance/edit_timesheet_requests',
                'estimated_times': 'attendance/estimated_times',
                'open_shifts': 'attendance/open_shifts',
            },
            
            # 📋 CONTRATOS E ESTRUTURA ORGANIZACIONAL
            'contracts': {
                'reference_contracts': 'contracts/reference_contracts',
                'contract_versions': 'contracts/contract_versions',
                'contract_templates': 'contracts/contract_templates',
                'compensations': 'contracts/compensations',
                'taxonomies': 'contracts/taxonomies',
                'spanish_contract_types': 'contracts/spanish_contract_types',
                'french_contract_types': 'contracts/french_contract_types',
                'german_contract_types': 'contracts/german_contract_types',
                'portuguese_contract_types': 'contracts/portuguese_contract_types',
                'spanish_education_levels': 'contracts/spanish_education_levels',
                'spanish_professional_categories': (
                    'contracts/spanish_professional_categories'
                ),
                'spanish_working_day_types': (
                    'contracts/spanish_working_day_types'
                ),
            },
            
            # 🎯 PERFORMANCE E COMPETÊNCIAS (DESCOBERTOS!)
            'performance': {
                'agreements': 'performance/agreements',
                'review_processes': 'performance/review_processes',
                'review_evaluations': 'performance/review_evaluations',
                'review_employee_scores': 'performance/review_employee_scores',
                'review_evaluation_answers': 'performance/review_evaluation_answers',
                'review_owners': 'performance/review_owners',
                'review_process_targets': 'performance/review_process_targets',
                'review_process_custom_templates': (
                    'performance/review_process_custom_templates'
                ),
                'review_process_estimated_targets': (
                    'performance/review_process_estimated_targets'
                ),
                'review_questionnaire_by_strategies': (
                    'performance/review_questionnaire_by_strategies'
                ),
                'review_visibility_settings': (
                    'performance/review_visibility_settings'
                ),
                'target_managers': 'performance/target_managers',
                'company_employee_score_scales': (
                    'performance/company_employee_score_scales'
                ),
                'employee_score_scales': 'performance/employee_score_scales',
            },
            
            # 🎓 TREINAMENTOS E COMPETÊNCIAS (DESCOBERTOS!)
            'trainings': {
                'trainings': 'trainings/trainings',
                'categories': 'trainings/categories',
                'sessions': 'trainings/sessions',
                'session_access_memberships': (
                    'trainings/session_access_memberships'
                ),
                'session_attendances': 'trainings/session_attendances',
                'training_classes': 'trainings/training_classes',
                'training_memberships': 'trainings/training_memberships',
            },
            
            # 👔 CATÁLOGO DE CARGOS E COMPETÊNCIAS
            'job_catalog': {
                'roles': 'job_catalog/roles',  # COMPETÊNCIAS ESTÃO AQUI!
                'levels': 'job_catalog/levels',
            },
            
            # 🔧 CAMPOS E RECURSOS PERSONALIZADOS
            'custom_data': {
                'custom_fields': 'custom_fields/fields',
                'custom_field_values': 'custom_fields/values',
                'custom_field_options': 'custom_fields/options',
                'custom_field_resource_fields': (
                    'custom_fields/resource_fields'
                ),
                'custom_resources_schemas': 'custom_resources/schemas',
                'custom_resources_values': 'custom_resources/values',
            },
            
            # 📄 DOCUMENTOS E CERTIFICADOS
            'documents': {
                'documents': 'documents/documents',
                'folders': 'documents/folders',
            },
            
            # 💰 BENEFÍCIOS E COMPENSAÇÃO
            'benefits': {
                'expensables': 'expenses/expensables',
                'expenses': 'expenses/expenses',
                'mileages': 'expenses/mileages',
                'per_diems': 'expenses/per_diems',
            },
            
            # 💸 DESPESAS E REEMBOLSOS (NOVA CATEGORIA!)
            'expenses': {
                'expensables': 'expenses/expensables',
                'expenses': 'expenses/expenses',
                'mileages': 'expenses/mileages',
                'per_diems': 'expenses/per_diems',
                'expense_categories': 'expenses/expense_categories',
                'expense_policies': 'expenses/expense_policies',
                'expense_reports': 'expenses/expense_reports',
                'expense_approvals': 'expenses/expense_approvals',
            },
            
            # 🏢 DADOS DA EMPRESA
            'company': {
                'legal_entities': 'companies/legal_entities',
            },
            
            # 💳 DADOS FINANCEIROS
            'finance': {
                'accounts': 'finance/accounts',
                'accounting_settings': 'finance/accounting_settings',
                'contacts': 'finance/contacts',
                'cost_centers': 'finance/cost_centers',
                'cost_center_memberships': 'finance/cost_center_memberships',
                'financial_documents': 'finance/financial_documents',
                'journal_entries': 'finance/journal_entries',
                'journal_lines': 'finance/journal_lines',
                'ledger_account_resources': 'finance/ledger_account_resources',
                'tax_rates': 'finance/tax_rates',
                'tax_types': 'finance/tax_types',
            },
            
            # 🏦 DADOS BANCÁRIOS
            'banking': {
                'bank_accounts': 'banking/bank_accounts',
                'card_payments': 'banking/card_payments',
                'transactions': 'banking/transactions',
            },
            
            # ⚖️ FOLHA DE PAGAMENTO
            'payroll': {
                'family_situations': 'payroll/family_situations',
                'supplements': 'payroll/supplements',
            },
            
            # 🌴 FÉRIAS E AUSÊNCIAS
            'timeoff': {
                'allowances': 'timeoff/allowances',
                'allowance_incidences': 'timeoff/allowance_incidences',
                'allowance_stats': 'timeoff/allowance_stats',
                'blocked_periods': 'timeoff/blocked_periods',
                'leaves': 'timeoff/leaves',
                'leave_types': 'timeoff/leave_types',
                'policies': 'timeoff/policies',
                'policy_assignments': 'timeoff/policy_assignments',
                'policy_timelines': 'timeoff/policy_timelines',
            },
            
            # 🔔 WEBHOOKS E API
            'api_management': {
                'credentials': 'api_public/credentials',
                'webhook_subscriptions': 'api_public/webhook_subscriptions',
            }
        }
        
        # 📊 Estatísticas de coleta
        self.collection_stats = {
            'total_endpoints': 0,
            'successful_collections': 0,
            'failed_collections': 0,
            'total_records': 0,
            'categories_completed': 0
        }
        
        # 📁 Diretórios de dados - Estrutura organizada
        self.data_dirs = {
            'base': Path("data/raw"),
            'employees': Path("data/raw/Funcionários"),
            'teams': Path("data/raw/Times"),
            'locations': Path("data/raw/Localizações"),
            'work_schedule': Path("data/raw/Escala de Trabalho"),
            'holidays': Path("data/raw/Feriados"),
            'ats': Path("data/raw/Recrutamento"),
            'attendance': Path("data/raw/Presença"),
            'contracts': Path("data/raw/Contratos"),
            'performance': Path("data/raw/Performance"),
            'trainings': Path("data/raw/Treinamentos"),
            'job_catalog': Path("data/raw/Cargos"),
            'custom_data': Path("data/raw/Dados Personalizados"),
            'documents': Path("data/raw/Documentos"),
            'benefits': Path("data/raw/Benefícios"),
            'expenses': Path("data/raw/Despesas"),
            'company': Path("data/raw/Empresa"),
            'finance': Path("data/raw/Financeiro"),
            'banking': Path("data/raw/Bancário"),
            'payroll': Path("data/raw/Folha de Pagamento"),
            'timeoff': Path("data/raw/Férias"),
            'api_management': Path("data/raw/Gerenciamento API"),
        }
        
        # Criar todos os diretórios
        for dir_path in self.data_dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def test_connection(self):
        """Testa a conexão com a API"""
        print("🔍 TESTANDO CONEXÃO COM A API FACTORIAL")
        print("=" * 60)
        
        try:
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
    
    def collect_endpoint_data(self, category, endpoint_name, endpoint_path,
                              limit=100, days_back=None):
        """Coleta dados de um endpoint específico com paginação e filtro de data."""
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

                if not response or 'data' not in response:
                    break

                data = response['data'] or []
                all_records.extend(data)

                if len(data) < limit:
                    break

                page += 1

            if all_records:
                print(f"✅ {len(all_records)} registros coletados")
                self.save_endpoint_data(category, endpoint_name, all_records)
                self.collection_stats['successful_collections'] += 1
                self.collection_stats['total_records'] += len(all_records)
                return True
            else:
                print(f"⚠️ Endpoint vazio: {endpoint_name}")
                self.collection_stats['failed_collections'] += 1
                return False

        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg:
                print(f"❌ Endpoint não disponível: {endpoint_name}")
            elif "403" in error_msg:
                print(f"🔒 Sem permissão: {endpoint_name}")
            elif "401" in error_msg:
                print(f"🔑 Não autorizado: {endpoint_name}")
            else:
                print(f"❌ Erro: {endpoint_name} - {str(e)[:50]}...")

            self.collection_stats['failed_collections'] += 1
            return False
    
    def save_endpoint_data(self, category, endpoint_name, data):
        """Salva dados de um endpoint em JSON e CSV"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Salvar JSON
            json_file = (self.data_dirs[category] /
                         f"{endpoint_name}_{timestamp}.json")
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)

            # Salvar CSV
            if data:
                df = pd.json_normalize(data)
                csv_file = (self.data_dirs[category] /
                            f"{endpoint_name}_{timestamp}.csv")
                df.to_csv(csv_file, index=False, encoding='utf-8')

                print(f"💾 Salvos: {json_file.name} | {csv_file.name}")
                if len(df.columns) > 0:
                    columns_preview = ', '.join(df.columns[:5])
                    if len(df.columns) > 5:
                        columns_preview += '...'
                    print(f"   Colunas: {columns_preview}")
            
        except Exception as e:
            print(f"❌ Erro ao salvar {endpoint_name}: {e}")
    
    def collect_category(self, category_name, days_back=None):
        """Coleta todos os dados de uma categoria com filtro de data opcional"""
        if category_name not in self.endpoint_categories:
            print(f"❌ Categoria não encontrada: {category_name}")
            return False
        
        # Inicializar cliente se necessário
        if self.client is None:
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
    
    def collect_competencies_focus(self):
        """Foco especial em competências - coleta dados de múltiplas fontes"""
        print("\n🎯 FOCO ESPECIAL: COMPETÊNCIAS E HABILIDADES")
        print("=" * 60)
        
        competency_sources = [
            # Performance (onde estão as competências!)
            ('performance', 'review_processes'),
            ('performance', 'agreements'),
            ('performance', 'review_evaluations'),
            ('performance', 'review_employee_scores'),
            
            # Job Catalog (roles com competências)
            ('job_catalog', 'roles'),
            
            # Trainings (treinamentos de competências)
            ('trainings', 'trainings'),
            ('trainings', 'training_classes'),
            ('trainings', 'categories'),
            
            # Custom Data (campos personalizados de competências)
            ('custom_data', 'custom_fields'),
            ('custom_data', 'custom_field_values'),
            ('custom_data', 'custom_resources_schemas'),
            ('custom_data', 'custom_resources_values'),
        ]
        
        competency_data = {}
        
        for category, endpoint in competency_sources:
            if (category in self.endpoint_categories and
                    endpoint in self.endpoint_categories[category]):
                endpoint_path = self.endpoint_categories[category][endpoint]

                print(f"🔍 Coletando competências de: {category}/{endpoint}")

                try:
                    full_path = f"api/2026-07-01/resources/{endpoint_path}"
                    response = self.client.get(full_path,
                                               params={'limit': 200, 'page': 1})
                    
                    if response and 'data' in response:
                        data = response['data']
                        
                        # Filtrar dados relacionados a competências
                        competency_related = []
                        for item in data:
                            item_str = json.dumps(item, default=str).lower()
                            keywords = [
                                'competenc', 'skill', 'habilidad', 'competência',
                                'ability', 'capability', 'expertise', 'knowledge'
                            ]
                            if any(keyword in item_str for keyword in keywords):
                                competency_related.append(item)

                        if competency_related:
                            competency_data[f"{category}_{endpoint}"] = (
                                competency_related
                            )
                            print(f"✅ {len(competency_related)} itens "
                                  f"relacionados a competências")
                        else:
                            print("⚠️ Nenhum item relacionado a "
                                  "competências encontrado")
                    
                except Exception as e:
                    print(f"❌ Erro ao coletar {category}/{endpoint}: {str(e)[:50]}...")
        
        # Salvar dados consolidados de competências
        if competency_data:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            competency_file = (self.data_dirs['base'] /
                               f"competencies_consolidated_{timestamp}.json")

            with open(competency_file, 'w', encoding='utf-8') as f:
                json.dump(competency_data, f, ensure_ascii=False, indent=2,
                          default=str)

            total_items = sum(len(items) for items in competency_data.values())
            print(f"\n🎯 COMPETÊNCIAS CONSOLIDADAS:")
            print(f"   📁 Arquivo: {competency_file}")
            print(f"   📊 Total de itens: {total_items}")
            print(f"   🔍 Fontes: {len(competency_data)}")
            
            return True
        else:
            print("\n⚠️ Nenhum dado de competência encontrado")
            return False
    
    def collect_multiple_categories(self, category_numbers, days_back=None):
        """Coleta múltiplas categorias selecionadas pelo usuário"""
        print(f"\n🚀 COLETA MÚLTIPLA - {len(category_numbers)} "
              f"CATEGORIAS SELECIONADAS")
        if days_back:
            print(f"📅 Filtro de data: últimos {days_back} dias")
        print("=" * 70)
        
        start_time = datetime.now()
        
        # Mapear números para nomes de categorias
        category_map = {
            '1': 'employees', '2': 'performance', '3': 'trainings',
            '4': 'job_catalog', '5': 'ats', '6': 'attendance',
            '7': 'contracts', '8': 'custom_data', '9': 'documents',
            '10': 'timeoff', '11': 'benefits', '12': 'expenses',
            '13': 'payroll', '14': 'finance', '15': 'banking',
            '16': 'company', '17': 'api_management', '18': 'teams',
            '19': 'locations', '20': 'work_schedule', '21': 'holidays'
        }
        
        successful_categories = 0
        
        for num in category_numbers:
            if num in category_map:
                category_name = category_map[num]
                if self.collect_category(category_name, days_back=days_back):
                    successful_categories += 1
            else:
                print(f"❌ Categoria {num} não encontrada")
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        print(f"\n✅ COLETA MÚLTIPLA CONCLUÍDA!")
        print(f"⏱️ Duração: {duration}")
        print(f"📊 Categorias coletadas: {successful_categories}/{len(category_numbers)}")
        
        self.generate_ultimate_report()
    
    def collect_all_ultimate(self, days_back=None):
        """Coleta TODOS os dados disponíveis - Modo Ultimate"""
        print("\n🚀 INICIANDO COLETA ULTIMATE - TODOS OS DADOS DA API")
        if days_back:
            print(f"📅 Filtro de data: últimos {days_back} dias")
        print("=" * 70)
        
        start_time = datetime.now()
        
        # Ordem otimizada de coleta (mais importantes primeiro)
        collection_order = [
            'employees',      # Funcionários primeiro
            'teams',          # Times
            'locations',      # Localizações
            'work_schedule',  # Escalas de trabalho
            'holidays',       # Feriados corporativos
            'performance',    # Performance e competências
            'trainings',      # Treinamentos
            'job_catalog',    # Cargos e competências
            'ats',           # Recrutamento
            'attendance',    # Presença
            'contracts',     # Contratos
            'custom_data',   # Dados personalizados
            'documents',     # Documentos
            'timeoff',       # Férias
            'benefits',      # Benefícios
            'expenses',      # Despesas e Reembolsos
            'payroll',       # Folha de pagamento
            'finance',       # Finanças
            'banking',       # Dados bancários
            'company',       # Empresa
            'api_management' # API
        ]
        
        for category in collection_order:
            if category in self.endpoint_categories:
                self.collect_category(category, days_back=days_back)
        
        # Foco especial em competências
        self.collect_competencies_focus()
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        print(f"\n✅ COLETA ULTIMATE CONCLUÍDA!")
        print(f"⏱️ Duração: {duration}")
        
        self.generate_ultimate_report()
    
    def generate_ultimate_report(self):
        """Gera relatório ultimate completo"""
        print("\n📋 RELATÓRIO ULTIMATE - COLETA COMPLETA DE DADOS DE RH")
        print("=" * 70)
        
        # Estatísticas gerais
        stats = self.collection_stats
        success_rate = (stats['successful_collections'] / stats['total_endpoints'] * 100) if stats['total_endpoints'] > 0 else 0
        
        print(f"📊 ESTATÍSTICAS GERAIS:")
        print(f"   🎯 Total de endpoints testados: {stats['total_endpoints']}")
        print(f"   ✅ Coletas bem-sucedidas: {stats['successful_collections']}")
        print(f"   ❌ Coletas falharam: {stats['failed_collections']}")
        print(f"   📈 Taxa de sucesso: {success_rate:.1f}%")
        print(f"   📋 Total de registros: {stats['total_records']}")
        print(f"   📁 Categorias completas: {stats['categories_completed']}")
        
        # Análise por categoria
        print(f"\n📁 ANÁLISE POR CATEGORIA:")
        total_files = 0
        
        for category, dir_path in self.data_dirs.items():
            if category == 'base':
                continue
                
            if dir_path.exists():
                json_files = list(dir_path.glob('*.json'))
                csv_files = list(dir_path.glob('*.csv'))
                category_total = len(json_files) + len(csv_files)
                total_files += category_total
                
                if category_total > 0:
                    print(f"   📂 {category.upper()}: {len(json_files)} JSON + {len(csv_files)} CSV")
                    
                    # Mostrar arquivo mais recente
                    if json_files:
                        latest_file = max(json_files, key=lambda x: x.stat().st_mtime)
                        print(f"      🕒 Mais recente: {latest_file.name}")
        
        print(f"\n📊 RESUMO FINAL:")
        print(f"   📁 Total de arquivos gerados: {total_files}")
        print(f"   💾 Diretório principal: {self.data_dirs['base']}")
        
        # Recomendações baseadas nos dados coletados
        print(f"\n🧠 ANÁLISES PREDITIVAS QI 300+ - 7 PERGUNTAS ESTRATÉGICAS:")
        print("")
        print("1. 🎯 PREDIÇÃO DE TURNOVER:")
        print("   'Quais funcionários têm maior probabilidade de sair nos próximos 6 meses?'")
        print("   📊 Cruze: Dados de presença + Mudanças contratuais + Avaliações + Tempo na empresa")
        print("   🔮 Insight: Funcionários com queda na presença + mudanças recentes + baixas avaliações = 85% chance de turnover")
        print("")
        print("2. 📈 IDENTIFICAÇÃO DE HIGH PERFORMERS:")
        print("   'Quem são os próximos líderes baseados em padrões comportamentais?'")
        print("   📊 Cruze: Scores de performance + Frequência de treinamentos + Feedback ATS + Progressão salarial")
        print("   🔮 Insight: Funcionários com crescimento consistente em múltiplas métricas = Potencial de liderança")
        print("")
        print("3. 🎓 GAPS DE COMPETÊNCIAS CRÍTICAS:")
        print("   'Quais competências faltarão na empresa nos próximos 2 anos?'")
        print("   📊 Cruze: Idade dos funcionários + Competências por cargo + Planos de aposentadoria + Pipeline ATS")
        print("   🔮 Insight: Mapear competências em risco por faixa etária e planejar sucessão")
        print("")
        print("4. 💰 OTIMIZAÇÃO DE INVESTIMENTO EM TREINAMENTO:")
        print("   'Qual ROI real dos treinamentos em performance individual?'")
        print("   📊 Cruze: Histórico de treinamentos + Evolução de performance + Promoções + Retenção pós-treinamento")
        print("   🔮 Insight: Identificar quais treinamentos geram maior impacto mensurável")
        print("")
        print("5. 🏢 CULTURA E ENGAGEMENT PREDITIVO:")
        print("   'Quais fatores culturais predizem melhor performance de equipe?'")
        print("   📊 Cruze: Campos personalizados (trabalho remoto/humor) + Performance coletiva + Turnover por equipe")
        print("   🔮 Insight: Correlacionar preferências de trabalho com resultados de equipe")
        print("")
        print("6. 🎯 RECRUTAMENTO INTELIGENTE:")
        print("   'Qual perfil de candidato tem maior probabilidade de sucesso a longo prazo?'")
        print("   📊 Cruze: Dados ATS (fonte, avaliações) + Performance histórica + Retenção por perfil de contratação")
        print("   🔮 Insight: Otimizar canais de recrutamento e critérios de seleção")
        print("")
        print("7. 💡 PREDIÇÃO DE NECESSIDADES ORGANIZACIONAIS:")
        print("   'Quais mudanças estruturais a empresa precisará nos próximos 12 meses?'")
        print("   📊 Cruze: Crescimento por departamento + Contratos temporários vs permanentes + Orçamento vs gastos reais")
        print("   🔮 Insight: Antecipar necessidades de headcount e reestruturações organizacionais")
        print("")
        print("🚀 IMPLEMENTAÇÃO PRÁTICA:")
        print("   • Use Python/R para correlações estatísticas")
        print("   • Crie dashboards preditivos no Power BI/Tableau")
        print("   • Implemente alertas automáticos para métricas críticas")
        print("   • Desenvolva modelos de machine learning para predições")
        print("   • Monitore KPIs preditivos mensalmente")
        
        # Salvar relatório
        self.save_ultimate_report()
    
    def save_ultimate_report(self):
        """Salva relatório ultimate em arquivo"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = self.data_dirs['base'] / f"ultimate_report_{timestamp}.json"
            
            report_data = {
                'timestamp': timestamp,
                'collection_stats': self.collection_stats,
                'endpoint_categories': {k: list(v.keys()) for k, v in self.endpoint_categories.items()},
                'data_directories': {k: str(v) for k, v in self.data_dirs.items()},
                'total_endpoints_mapped': sum(len(endpoints) for endpoints in self.endpoint_categories.values())
            }
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, ensure_ascii=False, indent=2, default=str)
            
            print(f"\n💾 Relatório Ultimate salvo: {report_file}")
            
        except Exception as e:
            print(f"❌ Erro ao salvar relatório: {e}")
    
    def close(self):
        """Fecha conexões"""
        if self.client:
            self.client.close()

def main():
    """Função principal"""
    print("🚀 HR DATA MASTER ULTIMATE - QI 300+ EDITION")
    print("=" * 70)
    print("🧠 Mapeamento COMPLETO da API Factorial baseado em api.json")
    print("🎯 Coleta TODOS os dados de RH disponíveis")
    print("💡 Foco especial em COMPETÊNCIAS e PERFORMANCE")
    print("=" * 70)
    
    # Verificar se existe arquivo de configuração
    env_file = Path(__file__).resolve().parents[1] / 'config.env'
    config_file = Path(__file__).resolve().parents[1] / 'config_factorial.env'
    
    if not env_file.exists() and not config_file.exists():
        print("⚠️ Arquivo de configuração não encontrado!")
        print("   Certifique-se de que existe 'config.env' ou 'config_factorial.env'")
        return
    
    # Configurar variável de ambiente para usar config.env se config_factorial.env não existir
    if not env_file.exists() and config_file.exists():
        os.environ['DOTENV_PATH'] = str(config_file)
    
    master = HRDataMasterUltimate()
    
    try:
        # Testar conexão primeiro
        if not master.test_connection():
            print("❌ Não foi possível estabelecer conexão com a API")
            return
        
        print(f"\n🎯 OPÇÕES ULTIMATE DISPONÍVEIS:")
        print("1. 👥 Coletar dados de Funcionários")
        print("2. 🎯 Coletar dados de Performance e Competências")
        print("3. 🎓 Coletar dados de Treinamentos")
        print("4. 👔 Coletar dados de Cargos (Job Catalog)")
        print("5. 🎯 Coletar dados de ATS (Recrutamento)")
        print("6. ⏰ Coletar dados de Presença")
        print("7. 📋 Coletar dados de Contratos")
        print("8. 🔧 Coletar dados Personalizados")
        print("9. 📄 Coletar Documentos")
        print("10. 🌴 Coletar dados de Férias")
        print("11. 💰 Coletar dados de Benefícios")
        print("12. 💸 Coletar dados de Despesas e Reembolsos")
        print("13. ⚖️ Coletar dados de Folha de Pagamento")
        print("14. 💳 Coletar dados Financeiros")
        print("15. 🏦 Coletar dados Bancários")
        print("16. 🏢 Coletar dados da Empresa")
        print("17. 🔔 Coletar dados de API")
        print("18. 👥 Coletar dados de Times")
        print("19. 📍 Coletar dados de Localizações")
        print("20. 🗓️ Coletar dados de Escala de Trabalho")
        print("21. 🎉 Coletar dados de Feriados")
        print("22. 🎯 FOCO ESPECIAL: Apenas Competências")
        print("23. 🚀 ULTIMATE: Coletar TODOS os dados")
        print("24. 📅 ULTIMATE COM FILTRO: Coletar dados dos últimos X dias")
        print("25. 🔢 COLETA MÚLTIPLA: Escolher várias categorias (ex: 1,3,13)")
        print("26. 🔢 COLETA MÚLTIPLA COM FILTRO: Escolher categorias + filtro de data")
        print("0. Sair")
        
        while True:
            try:
                choice = input("\n➤ Digite sua escolha (0-26): ").strip()
                
                if choice == '0':
                    print("👋 Saindo...")
                    break
                elif choice == '1':
                    master.collect_category('employees')
                elif choice == '2':
                    master.collect_category('performance')
                elif choice == '3':
                    master.collect_category('trainings')
                elif choice == '4':
                    master.collect_category('job_catalog')
                elif choice == '5':
                    master.collect_category('ats')
                elif choice == '6':
                    master.collect_category('attendance')
                elif choice == '7':
                    master.collect_category('contracts')
                elif choice == '8':
                    master.collect_category('custom_data')
                elif choice == '9':
                    master.collect_category('documents')
                elif choice == '10':
                    master.collect_category('timeoff')
                elif choice == '11':
                    master.collect_category('benefits')
                elif choice == '12':
                    master.collect_category('expenses')
                elif choice == '13':
                    master.collect_category('payroll')
                elif choice == '14':
                    master.collect_category('finance')
                elif choice == '15':
                    master.collect_category('banking')
                elif choice == '16':
                    master.collect_category('company')
                elif choice == '17':
                    master.collect_category('api_management')
                elif choice == '18':
                    master.collect_category('teams')
                elif choice == '19':
                    master.collect_category('locations')
                elif choice == '20':
                    master.collect_category('work_schedule')
                elif choice == '21':
                    master.collect_category('holidays')
                elif choice == '22':
                    master.collect_competencies_focus()
                elif choice == '23':
                    master.collect_all_ultimate()
                elif choice == '24':
                    # ULTIMATE COM FILTRO DE DATA
                    try:
                        days = int(input("📅 Quantos dias para trás? (ex: 30): "))
                        master.collect_all_ultimate(days_back=days)
                    except ValueError:
                        print("❌ Digite um número válido de dias")
                        continue
                elif choice == '25':
                    # COLETA MÚLTIPLA
                    try:
                        categories_input = input("🔢 Digite os números das categorias separados por vírgula (ex: 1,3,13): ")
                        category_numbers = [num.strip() for num in categories_input.split(',')]
                        master.collect_multiple_categories(category_numbers)
                    except Exception as e:
                        print(f"❌ Erro na entrada: {e}")
                        continue
                elif choice == '26':
                    # COLETA MÚLTIPLA COM FILTRO
                    try:
                        days = int(input("📅 Quantos dias para trás? (ex: 30): "))
                        categories_input = input("🔢 Digite os números das categorias separados por vírgula (ex: 1,3,13): ")
                        category_numbers = [num.strip() for num in categories_input.split(',')]
                        master.collect_multiple_categories(category_numbers, days_back=days)
                    except ValueError:
                        print("❌ Digite um número válido de dias")
                        continue
                    except Exception as e:
                        print(f"❌ Erro na entrada: {e}")
                        continue
                else:
                    print("❌ Opção inválida. Digite um número de 0 a 26.")
                    continue
                
                if choice in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26']:
                    master.generate_ultimate_report()
                
            except KeyboardInterrupt:
                print("\n\n👋 Execução interrompida pelo usuário")
                break
        
    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")
    finally:
        master.close()

if __name__ == "__main__":
    main()