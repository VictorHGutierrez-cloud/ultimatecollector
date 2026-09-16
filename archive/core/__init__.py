"""
Core module - Sistema base do Ultimate Collector
Contém as funcionalidades essenciais: API client e configurações
"""

from .api_client import APIClient
from .config import get_config, Config

__all__ = ['APIClient', 'get_config', 'Config']
