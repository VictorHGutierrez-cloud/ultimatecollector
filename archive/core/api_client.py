#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cliente base para APIs com funcionalidades essenciais
"""

import requests
import json
import time
import logging
from typing import Dict, Any, Optional, List
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from .config import Config

class APIClient:
    """Cliente base para integração com APIs"""
    
    def __init__(self, config_name: str = None):
        """Inicializa o cliente da API"""
        self.config = Config()
        self.session = self._create_session()
        self._setup_logging()
        
    def _create_session(self) -> requests.Session:
        """Cria uma sessão HTTP com configurações de retry"""
        session = requests.Session()
        
        # Configurar retry automático
        retry_strategy = Retry(
            total=self.config.MAX_RETRIES,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"],
            backoff_factor=self.config.RETRY_DELAY
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def _setup_logging(self):
        """Configura o sistema de logging"""
        logging.basicConfig(
            level=getattr(logging, self.config.LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.config.LOG_FILE),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _get_oauth2_token(self) -> str:
        """Obtém token OAuth2 usando client credentials flow"""
        try:
            token_data = {
                'grant_type': 'client_credentials',
                'client_id': self.config.CLIENT_ID,
                'client_secret': self.config.CLIENT_SECRET,
                'scope': 'read'  # Escopo padrão para leitura
            }
            
            response = requests.post(
                self.config.TOKEN_URL,
                data=token_data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                timeout=self.config.REQUEST_TIMEOUT
            )
            
            response.raise_for_status()
            token_response = response.json()
            
            self.logger.info("Token OAuth2 obtido com sucesso")
            return token_response['access_token']
            
        except Exception as e:
            self.logger.error(f"Erro ao obter token OAuth2: {e}")
            raise

    def _get_headers(self, custom_headers: Dict[str, str] = None) -> Dict[str, str]:
        """Retorna os headers padrão para as requisições"""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': f'{self.config.API_NAME}/{self.config.API_VERSION}'
        }
        
        # Adicionar autenticação
        if self.config.AUTH_TYPE == 'oauth2':
            # OAuth2 - obter token dinamicamente
            try:
                access_token = self._get_oauth2_token()
                headers['Authorization'] = f'Bearer {access_token}'
                self.logger.debug(f"Usando autenticação OAuth2 com token: {access_token[:10]}...")
            except Exception as e:
                self.logger.error(f"Falha na autenticação OAuth2: {e}")
                raise
        elif self.config.API_KEY:
            if self.config.AUTH_TYPE == 'bearer':
                headers['Authorization'] = f'Bearer {self.config.API_KEY}'
                self.logger.debug(f"Usando autenticação Bearer com chave: {self.config.API_KEY[:10]}...")
            elif self.config.AUTH_TYPE == 'x-api-key':
                headers['x-api-key'] = self.config.API_KEY
                self.logger.debug(f"Usando autenticação x-api-key com chave: {self.config.API_KEY[:10]}...")
            elif self.config.AUTH_TYPE == 'basic':
                import base64
                credentials = f"{self.config.API_KEY}:{self.config.API_SECRET}"
                encoded = base64.b64encode(credentials.encode()).decode()
                headers['Authorization'] = f'Basic {encoded}'
        
        # Adicionar headers customizados
        if custom_headers:
            headers.update(custom_headers)
        
        return headers
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Executa uma requisição HTTP com tratamento de erros"""
        # Corrigir duplicação do path da API
        base_url = self.config.BASE_URL.rstrip('/')
        endpoint = endpoint.lstrip('/')
        
        # Construir URL inicial
        url = f"{base_url}/{endpoint}"
        
        # Corrigir duplicação do path da API se existir
        if '/api/2026-07-01/api/2026-07-01/' in url:
            url = url.replace('/api/2026-07-01/api/2026-07-01/', '/api/2026-07-01/')
        
        # Log da URL final para debug
        self.logger.debug(f"URL construída: {url}")
        
        # Configurar timeout
        kwargs.setdefault('timeout', self.config.REQUEST_TIMEOUT)
        
        # Configurar headers
        kwargs.setdefault('headers', self._get_headers())
        
        try:
            self.logger.info(f"Fazendo requisição {method.upper()} para {url}")
            response = self.session.request(method, url, **kwargs)
            
            # Log da resposta
            self.logger.info(f"Resposta: {response.status_code} - {response.reason}")
            
            # Verificar se a resposta foi bem-sucedida
            response.raise_for_status()
            
            return response
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Erro na requisição: {e}")
            raise
    
    def get(self, endpoint: str, params: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
        """Executa uma requisição GET"""
        response = self._make_request('GET', endpoint, params=params, **kwargs)
        return response.json()
    
    def post(self, endpoint: str, data: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
        """Executa uma requisição POST"""
        if data:
            kwargs['json'] = data
        response = self._make_request('POST', endpoint, **kwargs)
        return response.json()
    
    def put(self, endpoint: str, data: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
        """Executa uma requisição PUT"""
        if data:
            kwargs['json'] = data
        response = self._make_request('PUT', endpoint, **kwargs)
        return response.json()
    
    def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Executa uma requisição DELETE"""
        response = self._make_request('DELETE', endpoint, **kwargs)
        return response.json()
    
    def patch(self, endpoint: str, data: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
        """Executa uma requisição PATCH"""
        if data:
            kwargs['json'] = data
        response = self._make_request('PATCH', endpoint, **kwargs)
        return response.json()
    

    def test_connection(self) -> bool:
        """Testa a conexão com a API usando um endpoint simples"""
        try:
            # Tentar um endpoint comum da API Factorial (usando método corrigido)
            response = self._make_request(
                'GET', 
                'api/2026-07-01/resources/api_public/credentials'
            )
            # Se chegou aqui, a requisição foi bem-sucedida
            self.logger.info(f"API respondeu com status {response.status_code} - Conexão OK")
            return True
                
        except Exception as e:
            # Se for erro 401, ainda significa que a API está respondendo
            if "401" in str(e):
                self.logger.info("API respondeu com 401 - Conexão OK, problema de autenticação")
                return True
            self.logger.error(f"Erro no teste de conexão: {e}")
            return False
    
    def get_rate_limit_info(self) -> Dict[str, Any]:
        """Retorna informações sobre rate limiting"""
        try:
            response = self.session.get(
                f"{self.config.BASE_URL}/api/2026-07-01",
                headers=self._get_headers()
            )
            
            rate_limit_info = {}
            
            # Verificar headers de rate limiting comuns
            if 'X-RateLimit-Limit' in response.headers:
                rate_limit_info['limit'] = response.headers['X-RateLimit-Limit']
            if 'X-RateLimit-Remaining' in response.headers:
                rate_limit_info['remaining'] = response.headers['X-RateLimit-Remaining']
            if 'X-RateLimit-Reset' in response.headers:
                rate_limit_info['reset'] = response.headers['X-RateLimit-Reset']
            
            return rate_limit_info
            
        except Exception as e:
            self.logger.error(f"Erro ao obter informações de rate limiting: {e}")
            return {}
    
    def close(self):
        """Fecha a sessão HTTP"""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
