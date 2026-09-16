#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 FERRAMENTA DE DEBUG PARA ATTENDANCE SENDER
Detecta e corrige problemas no attendance sender
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv

# Adicionar o diretório do projeto ao path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Carregar variáveis de ambiente
env_files = ['config_unificado.env', '.env', 'config.env']
for env_file in env_files:
    if Path(env_file).exists():
        load_dotenv(env_file, override=True)
        break

def check_environment():
    """Verifica as configurações de ambiente"""
    print("=" * 70)
    print("🔍 VERIFICAÇÃO DE AMBIENTE")
    print("=" * 70)
    
    issues = []
    
    # 1. Verificar arquivos .env
    env_files = [
        'config_unificado.env',
        'config.env',
        '.env',
        'config_factorial.env'
    ]
    
    found_env = False
    for env_file in env_files:
        if os.path.exists(env_file):
            print(f"✅ Arquivo encontrado: {env_file}")
            found_env = True
            break
    
    if not found_env:
        issues.append("❌ NENHUM ARQUIVO .env ENCONTRADO!")
        issues.append("   Você precisa criar um arquivo de configuração.")
        issues.append("   Sugestão: Copie config/config.example.env e renomeie para config_unificado.env")
    else:
        print(f"✅ Usando arquivo: {env_file}")
    
    # 2. Verificar variáveis de ambiente críticas
    print("\n📋 Verificando variáveis de ambiente:")
    critical_vars = {
        'BASE_URL': 'URL da API',
        'API_KEY': 'Token de autenticação',
        'AUTH_TYPE': 'Tipo de autenticação'
    }
    
    for var, description in critical_vars.items():
        value = os.getenv(var)
        if value:
            # Esconder valor sensível
            if var == 'API_KEY' and len(value) > 10:
                masked_value = f"{value[:10]}...{value[-4:]}"
            else:
                masked_value = value[:20] + '...' if len(str(value)) > 20 else value
            print(f"  ✅ {var}: {masked_value}")
        else:
            print(f"  ❌ {var}: NÃO CONFIGURADO")
            issues.append(f"❌ Variável {var} ({description}) não configurada")
    
    return issues

def check_imports():
    """Verifica se os imports estão corretos"""
    print("\n" + "=" * 70)
    print("📦 VERIFICAÇÃO DE IMPORTS")
    print("=" * 70)
    
    issues = []
    
    # Testar imports principais
    imports_to_test = [
        ('senders.attendance_sender', 'AttendanceSender'),
        ('senders.clock_interface', 'ClockInterface'),
        ('core.api_client', 'APIClient'),
        ('core.config', 'Config'),
    ]
    
    for module_path, class_name in imports_to_test:
        try:
            module = __import__(module_path, fromlist=[class_name])
            cls = getattr(module, class_name)
            print(f"✅ {module_path}.{class_name}")
        except ImportError as e:
            print(f"❌ {module_path}.{class_name}: {e}")
            issues.append(f"❌ Erro ao importar {module_path}.{class_name}: {e}")
        except AttributeError as e:
            print(f"❌ Classe {class_name} não encontrada em {module_path}: {e}")
            issues.append(f"❌ Classe {class_name} não encontrada em {module_path}")
    
    return issues

def test_attendance_sender():
    """Testa o attendance sender"""
    print("\n" + "=" * 70)
    print("🧪 TESTE DO ATTENDANCE SENDER")
    print("=" * 70)
    
    issues = []
    
    try:
        from senders.attendance_sender import AttendanceSender
        
        print("\n1️⃣ Testando inicialização do AttendanceSender...")
        try:
            sender = AttendanceSender()
            print("✅ AttendanceSender inicializado com sucesso")
        except Exception as e:
            print(f"❌ Erro ao inicializar AttendanceSender: {e}")
            issues.append(f"❌ Erro ao inicializar: {e}")
            return issues
        
        print("\n2️⃣ Testando conexão com a API...")
        try:
            connection_ok = sender.test_connection()
            if connection_ok:
                print("✅ Conexão com API estabelecida")
            else:
                print("❌ Falha na conexão com a API")
                issues.append("❌ Falha na conexão com a API")
        except Exception as e:
            print(f"❌ Erro ao testar conexão: {e}")
            issues.append(f"❌ Erro ao testar conexão: {e}")
            return issues
        
        print("\n3️⃣ Testando validação de employee_id...")
        try:
            # Buscar um employee_id válido
            from core.config import Config
            config = Config()
            
            if hasattr(config, 'AUTO_ATTENDANCE_EMPLOYEES') and config.AUTO_ATTENDANCE_EMPLOYEES:
                test_employee_id = config.AUTO_ATTENDANCE_EMPLOYEES[0]
                print(f"   Testando com employee_id: {test_employee_id}")
                
                # Testar get sem validation para ver se funciona
                try:
                    response = sender.get(
                        "api/2026-07-01/resources/employees/employees",
                        params={"limit": 10}
                    )
                    employees = response.get('data', [])
                    if employees:
                        print(f"✅ API respondeu: {len(employees)} funcionários encontrados")
                        print(f"   IDs disponíveis: {[emp.get('id') for emp in employees[:5]]}")
                        
                        # Verificar se o test_employee_id existe
                        employee_ids = [emp.get('id') for emp in employees]
                        if test_employee_id in employee_ids:
                            print(f"✅ Employee ID {test_employee_id} existe na API")
                        else:
                            print(f"⚠️ Employee ID {test_employee_id} NÃO encontrado na API")
                            issues.append(f"⚠️ Employee ID {test_employee_id} não encontrado")
                    else:
                        print("⚠️ Nenhum funcionário retornado pela API")
                except Exception as e:
                    print(f"❌ Erro ao buscar funcionários: {e}")
                    issues.append(f"❌ Erro ao buscar funcionários: {e}")
            else:
                print("⚠️ Nenhum employee_id configurado para teste")
                
        except Exception as e:
            print(f"❌ Erro ao testar validação: {e}")
            issues.append(f"❌ Erro ao testar validação: {e}")
        
        # Limpar recursos
        sender.close()
        
    except Exception as e:
        print(f"❌ Erro geral nos testes: {e}")
        issues.append(f"❌ Erro geral: {e}")
    
    return issues

def test_clock_interface():
    """Testa a interface de clock"""
    print("\n" + "=" * 70)
    print("🕐 TESTE DA INTERFACE DE CLOCK")
    print("=" * 70)
    
    issues = []
    
    try:
        from senders.clock_interface import ClockInterface
        
        print("\n1️⃣ Testando inicialização do ClockInterface...")
        try:
            interface = ClockInterface()
            print("✅ ClockInterface inicializado com sucesso")
        except Exception as e:
            print(f"❌ Erro ao inicializar ClockInterface: {e}")
            issues.append(f"❌ Erro ao inicializar ClockInterface: {e}")
            return issues
        
        print("\n2️⃣ Verificando métodos disponíveis...")
        methods = ['clock_in', 'clock_out', 'register_shift', 'show_employee_shifts']
        for method in methods:
            if hasattr(interface, method):
                print(f"✅ Método {method} disponível")
            else:
                print(f"❌ Método {method} NÃO disponível")
                issues.append(f"❌ Método {method} não encontrado")
        
    except Exception as e:
        print(f"❌ Erro ao testar ClockInterface: {e}")
        issues.append(f"❌ Erro ao testar ClockInterface: {e}")
    
    return issues

def fix_common_issues():
    """Tenta corrigir problemas comuns"""
    print("\n" + "=" * 70)
    print("🔧 CORREÇÃO DE PROBLEMAS COMUNS")
    print("=" * 70)
    
    fixes_applied = []
    
    # 1. Verificar se o arquivo .env existe
    if not os.path.exists('config_unificado.env'):
        if os.path.exists('config/config.example.env'):
            print("📝 Criando config_unificado.env a partir do exemplo...")
            try:
                import shutil
                shutil.copy('config/config.example.env', 'config_unificado.env')
                print("✅ Arquivo config_unificado.env criado")
                fixes_applied.append("✅ Arquivo config_unificado.env criado")
                print("\n⚠️ IMPORTANTE: Configure sua API_KEY no arquivo config_unificado.env")
            except Exception as e:
                print(f"❌ Erro ao criar config_unificado.env: {e}")
    
    # 2. Criar diretório de logs se não existir
    if not os.path.exists('logs'):
        print("📁 Criando diretório logs/...")
        os.makedirs('logs', exist_ok=True)
        fixes_applied.append("✅ Diretório logs/ criado")
    
    return fixes_applied

def main():
    """Função principal"""
    print("\n" + "=" * 70)
    print("🔧 FERRAMENTA DE DEBUG - ATTENDANCE SENDER")
    print("=" * 70)
    print("Esta ferramenta verifica e corrige problemas comuns")
    print("=" * 70)
    
    all_issues = []
    
    # 1. Verificar ambiente
    env_issues = check_environment()
    all_issues.extend(env_issues)
    
    # 2. Verificar imports
    import_issues = check_imports()
    all_issues.extend(import_issues)
    
    # 3. Tentar corrigir problemas comuns
    fixes = fix_common_issues()
    
    # 4. Testar attendance sender (só se não houver problemas críticos)
    if not all_issues:
        attendance_issues = test_attendance_sender()
        all_issues.extend(attendance_issues)
    
    # 5. Testar clock interface
    if not all_issues:
        clock_issues = test_clock_interface()
        all_issues.extend(clock_issues)
    
    # Relatório final
    print("\n" + "=" * 70)
    print("📊 RELATÓRIO FINAL")
    print("=" * 70)
    
    if fixes:
        print("\n✅ CORREÇÕES APLICADAS:")
        for fix in fixes:
            print(f"   {fix}")
    
    if all_issues:
        print("\n❌ PROBLEMAS ENCONTRADOS:")
        for issue in all_issues:
            print(f"   {issue}")
        
        print("\n💡 PRÓXIMOS PASSOS:")
        print("1. Configure seu arquivo config_unificado.env com suas credenciais")
        print("2. Execute este script novamente para verificar")
        print("3. Se o problema persistir, verifique os logs em logs/")
    else:
        print("\n✅ TUDO OK! Seu attendance sender está funcionando corretamente.")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Erro crítico: {e}")
        import traceback
        traceback.print_exc()

