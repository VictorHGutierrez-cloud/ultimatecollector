#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 ULTIMATE COLLECTOR - QI 300+ EDITION
Sistema definitivo de coleta de dados da API Factorial
Com 28 funções avançadas para máxima eficiência
"""

__version__ = "3.0.0"
__author__ = "Ultimate Collector Team"
__description__ = "Sistema definitivo de coleta de dados da API Factorial"

from .collectors.hr_data_masterultimate import HRDataMasterUltimate
from .core.api_client import APIClient
from .core.client_config import activate_client, list_clients, verify_client_token
from .core.config import Config
from .core.paths import PROJECT_ROOT
from .senders.attendance_sender import AttendanceSender
from .senders.ultimate_sender import UltimateSender

__all__ = [
    "HRDataMasterUltimate",
    "AttendanceSender",
    "UltimateSender",
    "APIClient",
    "Config",
    "PROJECT_ROOT",
    "activate_client",
    "list_clients",
    "verify_client_token",
]
