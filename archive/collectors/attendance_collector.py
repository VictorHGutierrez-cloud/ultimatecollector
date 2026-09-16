
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 ATTENDANCE SPECIALIST - Coletor Especializado em Presença
Foca em filtros de data funcionais para dados de presença
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

# Remover overrides hardcoded de ambiente; usaremos Configuracoes.config
# os.environ['BASE_URL'] = 'https://api.eu2.demo.factorial.dev'
# os.environ['API_KEY'] = '...'
# os.environ['AUTH_TYPE'] = 'x-api-key'
# os.environ['API_NAME'] = 'Factorial API'
# os.environ['API_VERSION'] = '2026-07-01'
# os.environ['LOG_LEVEL'] = 'DEBUG'
# os.environ['LOG_FILE'] = 'Logs_Sistema/factorial_api.log'

try:
    from core.api_client import APIClient
except ModuleNotFoundError:
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    from core.api_client import APIClient

class AttendanceSpecialist:
    def __init__(self):
        """Inicializa o especialista em presença"""
        self.client = None
        
        # 🎯 ENDPOINTS DE PRESENÇA ESPECÍFICOS (limitado a shifts para evitar 401)
        self.attendance_endpoints = {
            'shifts': 'attendance/shifts',
        }
        
        # 📁 Diretório de dados
        self.data_dir = Path("Dados_Coletados/Dados_Brutos/Dados da API/Presença")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 📊 Estatísticas
        self.stats = {
            'total_endpoints': 0,
            'successful_collections': 0,
            'failed_collections': 0,
            'total_records': 0
        }
    
    def test_connection(self):
        """Testa a conexão com a API"""
        print("🔍 TESTANDO CONEXÃO COM A API FACTORIAL")
        print("=" * 50)
        
        try:
            self.client = APIClient()
            
            if self.client.test_connection():
                print("✅ Conexão estabelecida com sucesso!")
                return True
            else:
                print("❌ Falha na conexão")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao testar conexão: {e}")
            return False
    
    def test_date_filters(self, endpoint_name, endpoint_path):
        """Testa diferentes tipos de filtros de data para um endpoint"""
        print(f"\n🧪 TESTANDO FILTROS DE DATA: {endpoint_name}")
        print("-" * 50)
        
        # Diferentes tipos de filtros para testar
        date_filters = [
            # Filtro padrão
            {'created_at_from': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')},
            
            # Filtros alternativos
            {'date_from': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')},
            {'start_date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')},
            {'from_date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')},
            
            # Filtros com range
            {
                'date_from': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
                'date_to': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'start_date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
                'end_date': datetime.now().strftime('%Y-%m-%d')
            },
            
            # Filtros específicos para presença
            {'work_date_from': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')},
            {'shift_date_from': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')},
            {'attendance_date_from': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')},
        ]
        
        best_filter = None
        min_records = float('inf')
        
        for i, filter_params in enumerate(date_filters, 1):
            print(f"\n🔍 Teste {i}: {list(filter_params.keys())}")
            
            try:
                full_path = f"api/2026-07-01/resources/{endpoint_path}"
                params = {'limit': 10, 'page': 1}
                params.update(filter_params)
                
                response = self.client.get(full_path, params=params)
                
                if response and 'data' in response:
                    data = response['data'] or []
                    record_count = len(data)
                    
                    print(f"   📊 Registros: {record_count}")
                    
                    # Se retornou poucos registros, pode ser o filtro certo
                    if 0 < record_count < min_records:
                        min_records = record_count
                        best_filter = filter_params
                        print(f"   ✅ MELHOR FILTRO ATÉ AGORA!")
                    
                    # Mostrar alguns campos dos registros para debug
                    if data:
                        sample_record = data[0]
                        date_fields = [k for k in sample_record.keys() if 'date' in k.lower() or 'time' in k.lower()]
                        print(f"   📅 Campos de data: {date_fields[:3]}")
                        
            except Exception as e:
                print(f"   ❌ Erro: {str(e)[:50]}...")
        
        return best_filter, min_records
    
    def collect_with_best_filter(self, endpoint_name, endpoint_path, days_back=1):
        """Coleta dados usando o melhor filtro encontrado"""
        print(f"\n🎯 COLETANDO COM MELHOR FILTRO: {endpoint_name}")
        print("-" * 50)
        
        # Primeiro, encontrar o melhor filtro
        best_filter, test_records = self.test_date_filters(endpoint_name, endpoint_path)
        
        if not best_filter:
            print("❌ Nenhum filtro funcionou!")
            return False
        
        print(f"✅ Melhor filtro encontrado: {best_filter}")
        print(f"📊 Registros no teste: {test_records}")
        
        # Agora coletar todos os dados com o filtro
        try:
            full_path = f"api/2026-07-01/resources/{endpoint_path}"
            all_records = []
            page = 1
            limit = 100
            
            while True:
                params = {'limit': limit, 'page': page}
                
                # Aplicar o melhor filtro com a data correta
                if days_back:
                    start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
                    end_date = datetime.now().strftime('%Y-%m-%d')
                    
                    # Ajustar o filtro com a data correta
                    adjusted_filter = {}
                    for key, value in best_filter.items():
                        if 'from' in key:
                            adjusted_filter[key] = start_date
                        elif 'to' in key or 'end' in key:
                            adjusted_filter[key] = end_date
                        else:
                            adjusted_filter[key] = value
                    
                    params.update(adjusted_filter)
                    print(f"   📅 Filtro aplicado: {adjusted_filter}")
                
                response = self.client.get(full_path, params=params)
                
                if not response or 'data' not in response:
                    break
                
                data = response['data'] or []
                all_records.extend(data)
                
                print(f"   📄 Página {page}: {len(data)} registros")
                
                if len(data) < limit:
                    break
                
                page += 1
                
                # Limite de segurança
                if page > 50:
                    print("   ⚠️ Limite de páginas atingido (50)")
                    break
            
            if all_records:
                print(f"✅ Total coletado: {len(all_records)} registros")
                self.save_attendance_data(endpoint_name, all_records)
                self.stats['successful_collections'] += 1
                self.stats['total_records'] += len(all_records)
                return True
            else:
                print("⚠️ Nenhum registro encontrado")
                self.stats['failed_collections'] += 1
                return False
                
        except Exception as e:
            print(f"❌ Erro na coleta: {e}")
            self.stats['failed_collections'] += 1
            return False
    
    def save_attendance_data(self, endpoint_name, data):
        """Salva dados de presença em JSON e CSV"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Salvar JSON
            json_file = self.data_dir / f"{endpoint_name}_{timestamp}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            
            # Salvar CSV
            if data:
                df = pd.json_normalize(data)
                csv_file = self.data_dir / f"{endpoint_name}_{timestamp}.csv"
                df.to_csv(csv_file, index=False, encoding='utf-8')
                
                print(f"💾 Salvos: {json_file.name} | {csv_file.name}")
                if len(df.columns) > 0:
                    print(f"   Colunas: {', '.join(df.columns[:5])}{'...' if len(df.columns) > 5 else ''}")
            
        except Exception as e:
            print(f"❌ Erro ao salvar {endpoint_name}: {e}")
    
    def collect_attendance_smart(self, days_back=1):
        """Coleta inteligente de presença com filtros otimizados"""
        print(f"\n🎯 COLETA INTELIGENTE DE PRESENÇA - {days_back} DIA(S)")
        print("=" * 60)
        
        if not self.test_connection():
            return False
        
        successful = 0
        
        for endpoint_name, endpoint_path in self.attendance_endpoints.items():
            # Evitar endpoints sem permissao conhecidos
            if endpoint_name == 'overtime_requests':
                print("\n⏭️  Pulando endpoint sem permissao: overtime_requests (401)")
                self.stats['total_endpoints'] += 1
                continue
            self.stats['total_endpoints'] += 1
            
            print(f"\n{'='*60}")
            print(f"🎯 PROCESSANDO: {endpoint_name.upper()}")
            print(f"{'='*60}")
            
            if self.collect_with_best_filter(endpoint_name, endpoint_path, days_back):
                successful += 1
        
        print(f"\n📊 RELATÓRIO FINAL:")
        print(f"   ✅ Endpoints coletados: {successful}/{self.stats['total_endpoints']}")
        print(f"   📋 Total de registros: {self.stats['total_records']}")
        print(f"   💾 Diretório: {self.data_dir}")
        
        return successful > 0
    
    def close(self):
        """Fecha conexões"""
        if self.client:
            self.client.close()

def main():
    """Função principal"""
    print("🎯 ATTENDANCE SPECIALIST - Coletor Especializado em Presença")
    print("=" * 70)
    print("🔍 Testa diferentes filtros de data até encontrar o que funciona")
    print("⚡ Otimizado para dados de presença com filtros inteligentes")
    print("=" * 70)
    
    specialist = AttendanceSpecialist()
    
    try:
        print("\n🎯 OPÇÕES DISPONÍVEIS:")
        print("1. 🧪 Testar filtros de data (sem coletar)")
        print("2. ⚡ Coleta rápida (1 dia)")
        print("3. 📅 Coleta com filtro personalizado")
        print("4. 🎯 Coleta inteligente (encontra melhor filtro)")
        print("0. Sair")
        
        while True:
            try:
                choice = input("\n➤ Digite sua escolha (0-4): ").strip()
                
                if choice == '0':
                    print("👋 Saindo...")
                    break
                elif choice == '1':
                    # Testar filtros
                    if specialist.test_connection():
                        for endpoint_name, endpoint_path in specialist.attendance_endpoints.items():
                            if endpoint_name == 'overtime_requests':
                                print("⏭️  Pulando teste de filtros para overtime_requests (401)")
                                continue
                            specialist.test_date_filters(endpoint_name, endpoint_path)
                elif choice == '2':
                    # Coleta rápida 1 dia
                    specialist.collect_attendance_smart(days_back=1)
                elif choice == '3':
                    # Coleta com filtro personalizado
                    try:
                        days = int(input("📅 Quantos dias para trás? (ex: 7): "))
                        specialist.collect_attendance_smart(days_back=days)
                    except ValueError:
                        print("❌ Digite um número válido de dias")
                        continue
                elif choice == '4':
                    # Coleta inteligente
                    specialist.collect_attendance_smart(days_back=1)
                else:
                    print("❌ Opção inválida. Digite um número de 0 a 4.")
                    continue
                
            except KeyboardInterrupt:
                print("\n\n👋 Execução interrompida pelo usuário")
                break
        
    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")
    finally:
        specialist.close()

if __name__ == "__main__":
    main()
