#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arquivo de configuração principal para projetos de API
"""

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo config_unificado.env (centralizado)
if os.path.exists('config_unificado.env'):
    load_dotenv('config_unificado.env')
elif os.path.exists('config.env'):
    load_dotenv('config.env')
elif os.path.exists('.env'):
    load_dotenv('.env')
elif os.path.exists('config_factorial.env'):
    load_dotenv('config_factorial.env')
else:
    load_dotenv()  # Tentar carregar do padrão

class Config:
    """Configurações principais da aplicação"""
    
    # Configurações da API
    API_NAME = os.getenv('API_NAME', 'Minha API')
    API_VERSION = os.getenv('API_VERSION', '2026-07-01')
    API_DESCRIPTION = os.getenv('API_DESCRIPTION', 'API para integração com sistemas externos')
    
    # Configurações de conexão
    BASE_URL = os.getenv('BASE_URL', 'https://api.exemplo.com')
    API_KEY = os.getenv('API_KEY', '')
    API_SECRET = os.getenv('API_SECRET', '')
    
    # Configurações de autenticação
    AUTH_TYPE = os.getenv('AUTH_TYPE', 'bearer')  # bearer, basic, oauth2
    TOKEN_URL = os.getenv('TOKEN_URL', '')
    CLIENT_ID = os.getenv('CLIENT_ID', '')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET', '')
    
    # Configurações de timeout e retry
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '30'))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
    RETRY_DELAY = int(os.getenv('RETRY_DELAY', '1'))
    
    # Configurações de logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/api.log')
    
    # Configurações de cache
    CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'False').lower() == 'true'
    CACHE_TTL = int(os.getenv('CACHE_TTL', '300'))  # 5 minutos
    
    # Configurações de rate limiting
    RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'False').lower() == 'true'
    RATE_LIMIT_REQUESTS = int(os.getenv('RATE_LIMIT_REQUESTS', '100'))
    RATE_LIMIT_WINDOW = int(os.getenv('RATE_LIMIT_WINDOW', '3600'))  # 1 hora
    
    # Configurações de diretórios
    DATA_RAW_DIR = os.getenv('DATA_RAW_DIR', 'Dados_Coletados/Dados_Brutos/Dados da API')
    DATA_PROCESSED_DIR = os.getenv('DATA_PROCESSED_DIR', 'Dados_Coletados/Dados_Processados')
    DATA_REPORTS_DIR = os.getenv('DATA_REPORTS_DIR', 'Dados_Coletados/Relatorios')
    LOGS_DIR = os.getenv('LOGS_DIR', 'Logs_Sistema')
    
    # Configurações de coleta
    DEFAULT_LIMIT = int(os.getenv('DEFAULT_LIMIT', '100'))
    DEFAULT_DAYS_BACK = int(os.getenv('DEFAULT_DAYS_BACK', '90'))
    ENABLE_PAGINATION = os.getenv('ENABLE_PAGINATION', 'True').lower() == 'true'
    
    # Configurações de automação
    AUTO_COLLECT_ON_START = os.getenv('AUTO_COLLECT_ON_START', 'False').lower() == 'true'
    AUTO_COLLECT_CATEGORIES = os.getenv('AUTO_COLLECT_CATEGORIES', 'employees').split(',')
    AUTO_COLLECT_INTERVAL = int(os.getenv('AUTO_COLLECT_INTERVAL', '60'))
    
    # Configurações de email
    EMAIL_NOTIFICATIONS = os.getenv('EMAIL_NOTIFICATIONS', 'False').lower() == 'true'
    EMAIL_SMTP_SERVER = os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
    EMAIL_SMTP_PORT = int(os.getenv('EMAIL_SMTP_PORT', '587'))
    EMAIL_USERNAME = os.getenv('EMAIL_USERNAME', '')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
    EMAIL_TO = os.getenv('EMAIL_TO', '')
    
    # Configurações de senders
    AUTO_SEND_ON_START = os.getenv('AUTO_SEND_ON_START', 'False').lower() == 'true'
    AUTO_SEND_TYPES = os.getenv('AUTO_SEND_TYPES', 'attendance').split(',')
    AUTO_SEND_INTERVAL = int(os.getenv('AUTO_SEND_INTERVAL', '30'))
    
    # Configurações de presença
    AUTO_ATTENDANCE_EMPLOYEES = [int(x.strip()) for x in os.getenv('AUTO_ATTENDANCE_EMPLOYEES', '').split(',') if x.strip()]
    DEFAULT_CLOCK_IN_TIME = os.getenv('DEFAULT_CLOCK_IN_TIME', '08:00')
    DEFAULT_CLOCK_OUT_TIME = os.getenv('DEFAULT_CLOCK_OUT_TIME', '17:00')
    INCLUDE_LOCATION = os.getenv('INCLUDE_LOCATION', 'True').lower() == 'true'
    DEFAULT_LATITUDE = float(os.getenv('DEFAULT_LATITUDE', '-23.5505'))
    DEFAULT_LONGITUDE = float(os.getenv('DEFAULT_LONGITUDE', '-46.6333'))
    
    # Configurações de turnos
    AUTO_GENERATE_SHIFTS = os.getenv('AUTO_GENERATE_SHIFTS', 'False').lower() == 'true'
    AUTO_SHIFT_EMPLOYEES = [int(x.strip()) for x in os.getenv('AUTO_SHIFT_EMPLOYEES', '').split(',') if x.strip()]
    SHIFT_GENERATION_DAYS = int(os.getenv('SHIFT_GENERATION_DAYS', '30'))
    SHIFT_START_TIME = os.getenv('SHIFT_START_TIME', '08:00')
    SHIFT_END_TIME = os.getenv('SHIFT_END_TIME', '17:00')
    SHIFT_BREAK_START = os.getenv('SHIFT_BREAK_START', '12:00')
    SHIFT_BREAK_END = os.getenv('SHIFT_BREAK_END', '13:00')
    
    # Configurações de simulação
    AUTO_SIMULATE = os.getenv('AUTO_SIMULATE', 'False').lower() == 'true'
    AUTO_SIMULATE_TYPES = os.getenv('AUTO_SIMULATE_TYPES', 'attendance').split(',')
    AUTO_SIMULATE_INTERVAL = int(os.getenv('AUTO_SIMULATE_INTERVAL', '60'))
    
    # Configurações financeiras
    AUTO_FINANCE_COLLECT = os.getenv('AUTO_FINANCE_COLLECT', 'True').lower() == 'true'
    AUTO_FINANCE_SEND = os.getenv('AUTO_FINANCE_SEND', 'False').lower() == 'true'
    AUTO_FINANCE_CATEGORIES = os.getenv('AUTO_FINANCE_CATEGORIES', 'accounts,categories').split(',')
    AUTO_FINANCE_COLLECT_INTERVAL = int(os.getenv('AUTO_FINANCE_COLLECT_INTERVAL', '120'))
    AUTO_FINANCE_SEND_INTERVAL = int(os.getenv('AUTO_FINANCE_SEND_INTERVAL', '60'))
    
    # Configurações contábeis
    AUTO_CREATE_ACCOUNTS = os.getenv('AUTO_CREATE_ACCOUNTS', 'False').lower() == 'true'
    AUTO_CREATE_COST_CENTERS = os.getenv('AUTO_CREATE_COST_CENTERS', 'False').lower() == 'true'
    AUTO_CREATE_CATEGORIES = os.getenv('AUTO_CREATE_CATEGORIES', 'False').lower() == 'true'
    AUTO_CREATE_CONTACTS = os.getenv('AUTO_CREATE_CONTACTS', 'False').lower() == 'true'
    
    # Configurações de lançamentos contábeis
    AUTO_CREATE_JOURNAL_ENTRIES = os.getenv('AUTO_CREATE_JOURNAL_ENTRIES', 'False').lower() == 'true'
    MAX_JOURNAL_ENTRIES_PER_BATCH = int(os.getenv('MAX_JOURNAL_ENTRIES_PER_BATCH', '50'))
    DEFAULT_DEBIT_ACCOUNT = os.getenv('DEFAULT_DEBIT_ACCOUNT', '1001')
    DEFAULT_CREDIT_ACCOUNT = os.getenv('DEFAULT_CREDIT_ACCOUNT', '2001')
    
    # Configurações de impostos
    AUTO_CREATE_TAX_RATES = os.getenv('AUTO_CREATE_TAX_RATES', 'False').lower() == 'true'
    AUTO_CREATE_TAX_TYPES = os.getenv('AUTO_CREATE_TAX_TYPES', 'False').lower() == 'true'
    DEFAULT_ICMS_RATE = float(os.getenv('DEFAULT_ICMS_RATE', '18.0'))
    DEFAULT_IPI_RATE = float(os.getenv('DEFAULT_IPI_RATE', '10.0'))
    DEFAULT_PIS_RATE = float(os.getenv('DEFAULT_PIS_RATE', '1.65'))
    DEFAULT_COFINS_RATE = float(os.getenv('DEFAULT_COFINS_RATE', '7.6'))

class DevelopmentConfig(Config):
    """Configurações para desenvolvimento"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Configurações para produção"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'

class TestingConfig(Config):
    """Configurações para testes"""
    TESTING = True
    LOG_LEVEL = 'DEBUG'

# Dicionário de configurações
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(config_name=None):
    """Retorna a configuração baseada no nome"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
    return config.get(config_name, config['default'])
