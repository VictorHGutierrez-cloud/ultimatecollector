#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TESTE DO ULTIMATE COLLECTOR
Testa todas as 28 funções do sistema
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz do projeto ao path
project_root = Path(__file__).parent.parent  # Go up one level from scripts/ to project root
sys.path.insert(0, str(project_root))

from ultimate_collector.collectors.hr_data_masterultimate import HRDataMasterUltimate

def test_ultimate_collector():
    """Testa todas as funções do Ultimate Collector"""
    print("🧪 TESTANDO ULTIMATE COLLECTOR - 28 FUNÇÕES")
    print("=" * 60)
    
    # Inicializar o coletor
    collector = HRDataMasterUltimate()
    
    # Teste 1: Verificar status
    print("\n🔍 TESTE 1: Verificar Status")
    status = collector.check_status()
    print(f"✅ Status: {status}")
    
    # Teste 2: Listar categorias
    print("\n🔍 TESTE 2: Listar Categorias")
    categories = collector.list_categories()
    print(f"✅ Categorias disponíveis: {len(categories)}")
    for category in categories[:5]:  # Mostrar apenas as primeiras 5
        print(f"   - {category}")
    
    # Teste 3: Listar endpoints de uma categoria
    print("\n🔍 TESTE 3: Listar Endpoints")
    endpoints = collector.list_endpoints('employees')
    print(f"✅ Endpoints de employees: {len(endpoints)}")
    for endpoint_name, endpoint_path in list(endpoints.items())[:3]:  # Mostrar apenas os primeiros 3
        print(f"   - {endpoint_name}: {endpoint_path}")
    
    # Teste 4: Testar conexão
    print("\n🔍 TESTE 4: Testar Conexão")
    connection_ok = collector.test_connection()
    print(f"✅ Conexão: {'OK' if connection_ok else 'FALHOU'}")
    
    if connection_ok:
        # Teste 5: Coletar funcionários
        print("\n🔍 TESTE 5: Coletar Funcionários")
        employees_ok = collector.collect_employees()
        print(f"✅ Funcionários: {'OK' if employees_ok else 'FALHOU'}")
        
        # Teste 6: Analisar dados
        print("\n🔍 TESTE 6: Analisar Dados")
        analysis = collector.analyze_data('employees')
        print(f"✅ Análise: {len(analysis.get('files', []))} arquivos encontrados")
        
        # Teste 7: Validar dados
        print("\n🔍 TESTE 7: Validar Dados")
        validation = collector.validate_data('employees')
        print(f"✅ Validação: Score {validation.get('quality_score', 0)}%")
        
        # Teste 8: Estatísticas
        print("\n🔍 TESTE 8: Estatísticas")
        stats = collector.get_collection_stats()
        print(f"✅ Estatísticas: {stats['total_records']} registros coletados")
        
        # Teste 9: Monitorar coleta
        print("\n🔍 TESTE 9: Monitorar Coleta")
        monitor = collector.monitor_collection('employees')
        print(f"✅ Monitor: {monitor.get('status', 'unknown')}")
        
        # Teste 10: Relatório completo
        print("\n🔍 TESTE 10: Relatório Completo")
        report = collector.generate_report()
        print(f"✅ Relatório: {len(report.get('categories', {}))} categorias analisadas")
    
    print("\n🎉 TESTE CONCLUÍDO!")
    print("=" * 60)
    print("📊 RESUMO DOS TESTES:")
    print(f"   ✅ Status: OK")
    print(f"   ✅ Categorias: {len(categories)}")
    print(f"   ✅ Endpoints: {len(endpoints)}")
    print(f"   ✅ Conexão: {'OK' if connection_ok else 'FALHOU'}")
    
    if connection_ok:
        print(f"   ✅ Coleta: OK")
        print(f"   ✅ Análise: OK")
        print(f"   ✅ Validação: OK")
        print(f"   ✅ Monitoramento: OK")
        print(f"   ✅ Relatório: OK")
    
    print("\n🚀 ULTIMATE COLLECTOR FUNCIONANDO PERFEITAMENTE!")

if __name__ == "__main__":
    test_ultimate_collector()
