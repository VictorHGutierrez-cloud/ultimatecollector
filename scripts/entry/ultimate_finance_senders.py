#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📤 ULTIMATE FINANCE SENDERS - QI 300+ EDITION
Senders para todos os módulos financeiros e contábeis
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

class UltimateFinanceSenders:
    """
    📤 ULTIMATE FINANCE SENDERS - QI 300+ EDITION
    
    Senders para todos os módulos financeiros e contábeis
    com validação e tratamento de erros avançados
    """
    
    def __init__(self):
        """Inicializa os senders financeiros"""
        self.client = None
        self.config = Config()
        self.sending_stats = {
            'total_sends': 0,
            'successful_sends': 0,
            'failed_sends': 0,
            'start_time': None,
            'end_time': None
        }
        
        # Mapeamento de senders financeiros
        self.finance_senders = {
            'accounts': self.send_account,
            'accounting_settings': self.send_accounting_setting,
            'categories': self.send_category,
            'contacts': self.send_contact,
            'cost_centers': self.send_cost_center,
            'financial_documents': self.send_financial_document,
            'journal_entries': self.send_journal_entry,
            'ledger_account_resources': self.send_ledger_account_resource,
            'tax_rates': self.send_tax_rate,
            'tax_types': self.send_tax_type
        }
        
        # Configurar logging
        self._setup_logging()
    
    def _setup_logging(self):
        """Configura o sistema de logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/finance_senders.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def test_connection(self) -> bool:
        """Testa a conexão para envio"""
        print("🔍 TESTANDO CONEXÃO PARA ENVIO FINANCEIRO")
        print("=" * 60)
        
        try:
            self.client = APIClient()
            
            print(f"📋 Configurações:")
            print(f"   API: {self.client.config.API_NAME}")
            print(f"   URL: {self.client.config.BASE_URL}")
            print(f"   Módulo: Finance Senders")
            
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
    
    def send_account(self, data: Dict) -> bool:
        """Envia dados de conta contábil"""
        try:
            endpoint = "api/2026-07-01/resources/finance/accounts"
            
            # Validar dados obrigatórios
            required_fields = ['name', 'legal_entity_id']
            for field in required_fields:
                if field not in data:
                    print(f"❌ Campo obrigatório ausente: {field}")
                    return False
            
            # Enviar dados
            response = self.client.post(endpoint, data)
            
            if response:
                print(f"✅ Conta '{data.get('name')}' enviada com sucesso!")
                self.sending_stats['successful_sends'] += 1
                return True
            else:
                print(f"❌ Erro ao enviar conta '{data.get('name')}'")
                self.sending_stats['failed_sends'] += 1
                return False
                
        except Exception as e:
            print(f"❌ Erro ao enviar conta: {e}")
            self.sending_stats['failed_sends'] += 1
            return False
    
    def send_accounting_setting(self, data: Dict) -> bool:
        """Envia configuração contábil"""
        try:
            endpoint = "api/2026-07-01/resources/finance/accounting_settings"
            
            # Validar dados obrigatórios
            required_fields = ['legal_entity_id']
            for field in required_fields:
                if field not in data:
                    print(f"❌ Campo obrigatório ausente: {field}")
                    return False
            
            # Enviar dados
            response = self.client.post(endpoint, data)
            
            if response:
                print(f"✅ Configuração contábil enviada com sucesso!")
                self.sending_stats['successful_sends'] += 1
                return True
            else:
                print(f"❌ Erro ao enviar configuração contábil")
                self.sending_stats['failed_sends'] += 1
                return False
                
        except Exception as e:
            print(f"❌ Erro ao enviar configuração contábil: {e}")
            self.sending_stats['failed_sends'] += 1
            return False
    
    def send_category(self, data: Dict) -> bool:
        """Envia categoria financeira"""
        try:
            endpoint = "api/2026-07-01/resources/finance/categories"
            
            # Validar dados obrigatórios
            required_fields = ['label']
            for field in required_fields:
                if field not in data:
                    print(f"❌ Campo obrigatório ausente: {field}")
                    return False
            
            # Enviar dados
            response = self.client.post(endpoint, data)
            
            if response:
                print(f"✅ Categoria '{data.get('label')}' enviada com sucesso!")
                self.sending_stats['successful_sends'] += 1
                return True
            else:
                print(f"❌ Erro ao enviar categoria '{data.get('label')}'")
                self.sending_stats['failed_sends'] += 1
                return False
                
        except Exception as e:
            print(f"❌ Erro ao enviar categoria: {e}")
            self.sending_stats['failed_sends'] += 1
            return False
    
    def send_contact(self, data: Dict) -> bool:
        """Envia contato financeiro"""
        try:
            endpoint = "api/2026-07-01/resources/finance/contacts"
            
            # Validar dados obrigatórios
            required_fields = ['name']
            for field in required_fields:
                if field not in data:
                    print(f"❌ Campo obrigatório ausente: {field}")
                    return False
            
            # Enviar dados
            response = self.client.post(endpoint, data)
            
            if response:
                print(f"✅ Contato '{data.get('name')}' enviado com sucesso!")
                self.sending_stats['successful_sends'] += 1
                return True
            else:
                print(f"❌ Erro ao enviar contato '{data.get('name')}'")
                self.sending_stats['failed_sends'] += 1
                return False
                
        except Exception as e:
            print(f"❌ Erro ao enviar contato: {e}")
            self.sending_stats['failed_sends'] += 1
            return False
    
    def send_cost_center(self, data: Dict) -> bool:
        """Envia centro de custo"""
        try:
            endpoint = "api/2026-07-01/resources/finance/cost_centers"
            
            # Validar dados obrigatórios
            required_fields = ['name', 'company_id']
            for field in required_fields:
                if field not in data:
                    print(f"❌ Campo obrigatório ausente: {field}")
                    return False
            
            # Enviar dados
            response = self.client.post(endpoint, data)
            
            if response:
                print(f"✅ Centro de custo '{data.get('name')}' enviado com sucesso!")
                self.sending_stats['successful_sends'] += 1
                return True
            else:
                print(f"❌ Erro ao enviar centro de custo '{data.get('name')}'")
                self.sending_stats['failed_sends'] += 1
                return False
                
        except Exception as e:
            print(f"❌ Erro ao enviar centro de custo: {e}")
            self.sending_stats['failed_sends'] += 1
            return False
    
    def send_financial_document(self, data: Dict) -> bool:
        """Envia documento financeiro"""
        try:
            endpoint = "api/2026-07-01/resources/finance/financial_documents"
            
            # Validar dados obrigatórios
            required_fields = ['document_number', 'net_amount_cents']
            for field in required_fields:
                if field not in data:
                    print(f"❌ Campo obrigatório ausente: {field}")
                    return False
            
            # Enviar dados
            response = self.client.post(endpoint, data)
            
            if response:
                print(f"✅ Documento '{data.get('document_number')}' enviado com sucesso!")
                self.sending_stats['successful_sends'] += 1
                return True
            else:
                print(f"❌ Erro ao enviar documento '{data.get('document_number')}'")
                self.sending_stats['failed_sends'] += 1
                return False
                
        except Exception as e:
            print(f"❌ Erro ao enviar documento financeiro: {e}")
            self.sending_stats['failed_sends'] += 1
            return False
    
    def send_journal_entry(self, data: Dict) -> bool:
        """Envia lançamento contábil"""
        try:
            endpoint = "api/2026-07-01/resources/finance/journal_entries"
            
            # Validar dados obrigatórios
            required_fields = ['type']
            for field in required_fields:
                if field not in data:
                    print(f"❌ Campo obrigatório ausente: {field}")
                    return False
            
            # Enviar dados
            response = self.client.post(endpoint, data)
            
            if response:
                print(f"✅ Lançamento contábil enviado com sucesso!")
                self.sending_stats['successful_sends'] += 1
                return True
            else:
                print(f"❌ Erro ao enviar lançamento contábil")
                self.sending_stats['failed_sends'] += 1
                return False
                
        except Exception as e:
            print(f"❌ Erro ao enviar lançamento contábil: {e}")
            self.sending_stats['failed_sends'] += 1
            return False
    
    def send_ledger_account_resource(self, data: Dict) -> bool:
        """Envia recurso de conta"""
        try:
            endpoint = "api/2026-07-01/resources/finance/ledger_account_resources"
            
            # Validar dados obrigatórios
            required_fields = ['resource_type', 'resource_id', 'account_id']
            for field in required_fields:
                if field not in data:
                    print(f"❌ Campo obrigatório ausente: {field}")
                    return False
            
            # Enviar dados
            response = self.client.post(endpoint, data)
            
            if response:
                print(f"✅ Recurso de conta enviado com sucesso!")
                self.sending_stats['successful_sends'] += 1
                return True
            else:
                print(f"❌ Erro ao enviar recurso de conta")
                self.sending_stats['failed_sends'] += 1
                return False
                
        except Exception as e:
            print(f"❌ Erro ao enviar recurso de conta: {e}")
            self.sending_stats['failed_sends'] += 1
            return False
    
    def send_tax_rate(self, data: Dict) -> bool:
        """Envia taxa de imposto"""
        try:
            endpoint = "api/2026-07-01/resources/finance/tax_rates"
            
            # Validar dados obrigatórios
            required_fields = ['rate', 'tax_type_id']
            for field in required_fields:
                if field not in data:
                    print(f"❌ Campo obrigatório ausente: {field}")
                    return False
            
            # Enviar dados
            response = self.client.post(endpoint, data)
            
            if response:
                print(f"✅ Taxa de imposto enviada com sucesso!")
                self.sending_stats['successful_sends'] += 1
                return True
            else:
                print(f"❌ Erro ao enviar taxa de imposto")
                self.sending_stats['failed_sends'] += 1
                return False
                
        except Exception as e:
            print(f"❌ Erro ao enviar taxa de imposto: {e}")
            self.sending_stats['failed_sends'] += 1
            return False
    
    def send_tax_type(self, data: Dict) -> bool:
        """Envia tipo de imposto"""
        try:
            endpoint = "api/2026-07-01/resources/finance/tax_types"
            
            # Validar dados obrigatórios
            required_fields = ['name', 'type']
            for field in required_fields:
                if field not in data:
                    print(f"❌ Campo obrigatório ausente: {field}")
                    return False
            
            # Enviar dados
            response = self.client.post(endpoint, data)
            
            if response:
                print(f"✅ Tipo de imposto '{data.get('name')}' enviado com sucesso!")
                self.sending_stats['successful_sends'] += 1
                return True
            else:
                print(f"❌ Erro ao enviar tipo de imposto '{data.get('name')}'")
                self.sending_stats['failed_sends'] += 1
                return False
                
        except Exception as e:
            print(f"❌ Erro ao enviar tipo de imposto: {e}")
            self.sending_stats['failed_sends'] += 1
            return False
    
    def send_finance_data(self, category: str, data: Dict) -> bool:
        """Envia dados financeiros de uma categoria"""
        if category not in self.finance_senders:
            print(f"❌ Categoria financeira não encontrada: {category}")
            return False
        
        print(f"📤 ENVIANDO DADOS FINANCEIROS: {category.upper()}")
        print("=" * 60)
        
        self.sending_stats['start_time'] = datetime.now()
        self.sending_stats['total_sends'] += 1
        
        # Enviar dados usando o sender apropriado
        sender_func = self.finance_senders[category]
        success = sender_func(data)
        
        self.sending_stats['end_time'] = datetime.now()
        
        return success
    
    def send_batch_finance_data(self, category: str, data_list: List[Dict]) -> Dict[str, int]:
        """Envia lote de dados financeiros"""
        print(f"📤 ENVIANDO LOTE DE DADOS FINANCEIROS: {category.upper()}")
        print("=" * 60)
        
        results = {
            'total': len(data_list),
            'successful': 0,
            'failed': 0
        }
        
        for i, data in enumerate(data_list, 1):
            print(f"🔄 Enviando item {i}/{len(data_list)}...")
            
            if self.send_finance_data(category, data):
                results['successful'] += 1
            else:
                results['failed'] += 1
        
        print(f"\n📊 Resultado do lote:")
        print(f"   ✅ Sucessos: {results['successful']}")
        print(f"   ❌ Falhas: {results['failed']}")
        print(f"   📊 Total: {results['total']}")
        
        return results
    
    def create_sample_finance_data(self, category: str) -> Dict:
        """Cria dados de exemplo para teste"""
        sample_data = {
            'accounts': {
                'name': 'Conta Teste',
                'legal_entity_id': 1,
                'number': '1001',
                'disabled': False
            },
            'accounting_settings': {
                'legal_entity_id': 1,
                'fiscal_year_start': '2025-01-01',
                'fiscal_year_end': '2025-12-31'
            },
            'categories': {
                'label': 'Categoria Teste',
                'default_label': 'Categoria Padrão',
                'identifier': 'TESTE'
            },
            'contacts': {
                'name': 'Contato Teste',
                'legal_name': 'Contato Teste LTDA',
                'tax_id': '12345678000199'
            },
            'cost_centers': {
                'name': 'Centro de Custo Teste',
                'company_id': 1,
                'code': 'CC001'
            },
            'financial_documents': {
                'document_number': 'DOC001',
                'net_amount_cents': 100000,
                'total_amount_cents': 118000,
                'currency': 'BRL'
            },
            'journal_entries': {
                'type': 'manual',
                'description': 'Lançamento de teste'
            },
            'ledger_account_resources': {
                'resource_type': 'account',
                'resource_id': 1,
                'account_id': 1,
                'balance_type': 'debit'
            },
            'tax_rates': {
                'rate': 18.0,
                'tax_type_id': 1,
                'description': 'ICMS Teste'
            },
            'tax_types': {
                'name': 'ICMS',
                'type': 'sales_tax',
                'country_code': 'BR'
            }
        }
        
        return sample_data.get(category, {})
    
    def get_sending_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de envio"""
        return {
            'total_sends': self.sending_stats['total_sends'],
            'successful_sends': self.sending_stats['successful_sends'],
            'failed_sends': self.sending_stats['failed_sends'],
            'success_rate': (self.sending_stats['successful_sends'] / self.sending_stats['total_sends'] * 100) if self.sending_stats['total_sends'] > 0 else 0,
            'start_time': self.sending_stats['start_time'],
            'end_time': self.sending_stats['end_time'],
            'duration': (self.sending_stats['end_time'] - self.sending_stats['start_time'] 
                        if self.sending_stats['start_time'] and self.sending_stats['end_time'] 
                        else None)
        }
    
    def list_available_senders(self) -> List[str]:
        """Lista senders financeiros disponíveis"""
        return list(self.finance_senders.keys())

