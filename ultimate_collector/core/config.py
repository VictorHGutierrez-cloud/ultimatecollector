#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configurações centralizadas do Ultimate Collector.
Carrega variáveis de ambiente com prioridade: config/unificado.env > config/.env > example.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

project_root = Path(__file__).resolve().parents[2]
config_path = project_root / "config" / ".env"
unified_path = project_root / "config" / "unificado.env"
legacy_unified_path = project_root / "config_unificado.env"
example_path = project_root / "config" / "config.example.env"

ENV_CANDIDATES = (unified_path, legacy_unified_path, config_path, example_path)


def _load_env_file(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ[key.strip()] = value.strip().strip('"').strip("'")
        return True
    except Exception:
        return False


for env_path in ENV_CANDIDATES:
    if env_path.exists():
        load_dotenv(env_path, override=True)
        break

required_keys = ("API_VERSION", "BASE_URL", "API_KEY", "AUTH_TYPE")
if not all(key in os.environ for key in required_keys):
    for path in ENV_CANDIDATES:
        if _load_env_file(path) and all(key in os.environ for key in required_keys):
            break


class Config:
    """Configurações centralizadas do Ultimate Collector."""

    # API
    API_NAME = os.getenv("API_NAME", "Factorial API")
    API_VERSION = os.getenv("API_VERSION", "2026-07-01")
    API_DESCRIPTION = os.getenv("API_DESCRIPTION", "API para integração com sistemas externos")
    BASE_URL = os.getenv("BASE_URL", "https://api.eu2.demo.factorial.dev")
    API_KEY = os.getenv("API_KEY", "")
    API_SECRET = os.getenv("API_SECRET", "")

    # Autenticação
    AUTH_TYPE = os.getenv("AUTH_TYPE", "bearer")
    TOKEN_URL = os.getenv("TOKEN_URL", "")
    CLIENT_ID = os.getenv("CLIENT_ID", "")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")

    # Timeout e retry
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", os.getenv("TIMEOUT", "30")))
    TIMEOUT = REQUEST_TIMEOUT
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_DELAY = int(os.getenv("RETRY_DELAY", "1"))

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/factorial_api.log")
    LOGS_DIR = os.getenv("LOGS_DIR", "logs")

    # Cache e rate limiting
    CACHE_ENABLED = os.getenv("CACHE_ENABLED", "False").lower() == "true"
    CACHE_TTL = int(os.getenv("CACHE_TTL", "300"))
    RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "False").lower() == "true"
    RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "3600"))

    # Diretórios de dados
    DATA_DIR = os.getenv("DATA_DIR", "data")
    RAW_DATA_DIR = os.getenv("RAW_DATA_DIR", "data/raw")
    PROCESSED_DATA_DIR = os.getenv("PROCESSED_DATA_DIR", "data/processed")
    BACKUP_DATA_DIR = os.getenv("BACKUP_DATA_DIR", "data/backup")
    DATA_RAW_DIR = RAW_DATA_DIR
    DATA_PROCESSED_DIR = PROCESSED_DATA_DIR
    DATA_REPORTS_DIR = os.getenv("DATA_REPORTS_DIR", "data/reports")

    # Coleta
    DEFAULT_LIMIT = int(os.getenv("DEFAULT_LIMIT", "100"))
    DEFAULT_DAYS_BACK = int(os.getenv("DEFAULT_DAYS_BACK", "90"))
    ENABLE_PAGINATION = os.getenv("ENABLE_PAGINATION", "True").lower() == "true"
    AUTO_COLLECT_ON_START = os.getenv("AUTO_COLLECT_ON_START", "False").lower() == "true"
    AUTO_COLLECT_CATEGORIES = os.getenv("AUTO_COLLECT_CATEGORIES", "employees,expenses").split(",")
    AUTO_COLLECT_INTERVAL = int(os.getenv("AUTO_COLLECT_INTERVAL", "60"))

    # Envio
    AUTO_SEND_ON_START = os.getenv("AUTO_SEND_ON_START", "False").lower() == "true"
    AUTO_SEND_TYPES = os.getenv("AUTO_SEND_TYPES", "attendance").split(",")
    AUTO_SEND_INTERVAL = int(os.getenv("AUTO_SEND_INTERVAL", "30"))

    # Presença
    AUTO_ATTENDANCE_EMPLOYEES = [
        int(x.strip()) for x in os.getenv("AUTO_ATTENDANCE_EMPLOYEES", "").split(",") if x.strip()
    ]
    DEFAULT_CLOCK_IN_TIME = os.getenv("DEFAULT_CLOCK_IN_TIME", "08:00")
    DEFAULT_CLOCK_OUT_TIME = os.getenv("DEFAULT_CLOCK_OUT_TIME", "17:00")
    INCLUDE_LOCATION = os.getenv("INCLUDE_LOCATION", "True").lower() == "true"
    DEFAULT_LATITUDE = float(os.getenv("DEFAULT_LATITUDE", "-23.5505"))
    DEFAULT_LONGITUDE = float(os.getenv("DEFAULT_LONGITUDE", "-46.6333"))

    # Turnos
    AUTO_GENERATE_SHIFTS = os.getenv("AUTO_GENERATE_SHIFTS", "False").lower() == "true"
    AUTO_SHIFT_EMPLOYEES = [
        int(x.strip()) for x in os.getenv("AUTO_SHIFT_EMPLOYEES", "").split(",") if x.strip()
    ]
    SHIFT_GENERATION_DAYS = int(os.getenv("SHIFT_GENERATION_DAYS", "30"))
    SHIFT_START_TIME = os.getenv("SHIFT_START_TIME", "08:00")
    SHIFT_END_TIME = os.getenv("SHIFT_END_TIME", "17:00")
    SHIFT_BREAK_START = os.getenv("SHIFT_BREAK_START", "12:00")
    SHIFT_BREAK_END = os.getenv("SHIFT_BREAK_END", "13:00")

    # Simulação
    AUTO_SIMULATE = os.getenv("AUTO_SIMULATE", "False").lower() == "true"
    AUTO_SIMULATE_TYPES = os.getenv("AUTO_SIMULATE_TYPES", "attendance").split(",")
    AUTO_SIMULATE_INTERVAL = int(os.getenv("AUTO_SIMULATE_INTERVAL", "60"))

    # Financeiro
    AUTO_FINANCE_COLLECT = os.getenv("AUTO_FINANCE_COLLECT", "True").lower() == "true"
    AUTO_FINANCE_SEND = os.getenv("AUTO_FINANCE_SEND", "False").lower() == "true"
    AUTO_FINANCE_CATEGORIES = os.getenv("AUTO_FINANCE_CATEGORIES", "accounts,categories").split(",")
    AUTO_FINANCE_COLLECT_INTERVAL = int(os.getenv("AUTO_FINANCE_COLLECT_INTERVAL", "120"))
    AUTO_FINANCE_SEND_INTERVAL = int(os.getenv("AUTO_FINANCE_SEND_INTERVAL", "60"))

    # Contábil
    AUTO_CREATE_ACCOUNTS = os.getenv("AUTO_CREATE_ACCOUNTS", "False").lower() == "true"
    AUTO_CREATE_COST_CENTERS = os.getenv("AUTO_CREATE_COST_CENTERS", "False").lower() == "true"
    AUTO_CREATE_CATEGORIES = os.getenv("AUTO_CREATE_CATEGORIES", "False").lower() == "true"
    AUTO_CREATE_CONTACTS = os.getenv("AUTO_CREATE_CONTACTS", "False").lower() == "true"
    AUTO_CREATE_JOURNAL_ENTRIES = os.getenv("AUTO_CREATE_JOURNAL_ENTRIES", "False").lower() == "true"
    MAX_JOURNAL_ENTRIES_PER_BATCH = int(os.getenv("MAX_JOURNAL_ENTRIES_PER_BATCH", "50"))
    DEFAULT_DEBIT_ACCOUNT = os.getenv("DEFAULT_DEBIT_ACCOUNT", "1001")
    DEFAULT_CREDIT_ACCOUNT = os.getenv("DEFAULT_CREDIT_ACCOUNT", "2001")

    # Impostos
    AUTO_CREATE_TAX_RATES = os.getenv("AUTO_CREATE_TAX_RATES", "False").lower() == "true"
    AUTO_CREATE_TAX_TYPES = os.getenv("AUTO_CREATE_TAX_TYPES", "False").lower() == "true"
    DEFAULT_ICMS_RATE = float(os.getenv("DEFAULT_ICMS_RATE", "18.0"))
    DEFAULT_IPI_RATE = float(os.getenv("DEFAULT_IPI_RATE", "10.0"))
    DEFAULT_PIS_RATE = float(os.getenv("DEFAULT_PIS_RATE", "1.65"))
    DEFAULT_COFINS_RATE = float(os.getenv("DEFAULT_COFINS_RATE", "7.6"))

    # Notificações
    EMAIL_NOTIFICATIONS = os.getenv("EMAIL_NOTIFICATIONS", "False").lower() == "true"
    EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER", "smtp.gmail.com")
    EMAIL_SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", "587"))
    EMAIL_USERNAME = os.getenv("EMAIL_USERNAME", "")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
    EMAIL_TO = os.getenv("EMAIL_TO", "")

    # Performance
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", "100"))

    @classmethod
    def reload(cls) -> None:
        """Recarrega valores a partir de os.environ (após trocar cliente)."""
        cls.API_NAME = os.getenv("API_NAME", "Factorial API")
        cls.API_VERSION = os.getenv("API_VERSION", "2026-07-01")
        cls.BASE_URL = os.getenv("BASE_URL", "https://api.eu2.demo.factorial.dev")
        cls.API_KEY = os.getenv("API_KEY", "")
        cls.AUTH_TYPE = os.getenv("AUTH_TYPE", "bearer")
        cls.RAW_DATA_DIR = os.getenv("RAW_DATA_DIR", "data/raw")
        cls.DATA_DIR = os.getenv("DATA_DIR", "data")
        cls.AUTO_COLLECT_CATEGORIES = os.getenv(
            "AUTO_COLLECT_CATEGORIES", "employees,expenses"
        ).split(",")
        cls.AUTO_ATTENDANCE_EMPLOYEES = [
            int(x.strip())
            for x in os.getenv("AUTO_ATTENDANCE_EMPLOYEES", "").split(",")
            if x.strip()
        ]


class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = "WARNING"


class TestingConfig(Config):
    TESTING = True
    LOG_LEVEL = "DEBUG"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}


def get_config(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "default")
    return config.get(config_name, config["default"])
