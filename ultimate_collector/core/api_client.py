#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cliente API unificado do Ultimate Collector.
Suporta OAuth2, Bearer, x-api-key e Basic auth.
"""

import base64
import logging
from typing import Any, Dict, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import Config


class APIClient:
    """Cliente base para integração com APIs."""

    def __init__(self, config_name: str = None):
        self.config = Config()
        self.session = self._create_session()
        self._setup_logging()

    def _create_session(self) -> requests.Session:
        session = requests.Session()
        retry_strategy = Retry(
            total=self.config.MAX_RETRIES,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "PATCH", "DELETE"],
            backoff_factor=self.config.RETRY_DELAY,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def _setup_logging(self):
        logging.basicConfig(
            level=getattr(logging, self.config.LOG_LEVEL),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(self.config.LOG_FILE),
                logging.StreamHandler(),
            ],
        )
        self.logger = logging.getLogger(__name__)

    def _get_oauth2_token(self) -> str:
        try:
            token_data = {
                "grant_type": "client_credentials",
                "client_id": self.config.CLIENT_ID,
                "client_secret": self.config.CLIENT_SECRET,
                "scope": "read",
            }
            response = requests.post(
                self.config.TOKEN_URL,
                data=token_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=self.config.REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            token_response = response.json()
            self.logger.info("Token OAuth2 obtido com sucesso")
            return token_response["access_token"]
        except Exception as e:
            self.logger.error("Erro ao obter token OAuth2: %s", e)
            raise

    def _get_headers(self, custom_headers: Dict[str, str] = None) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": f"{self.config.API_NAME}/{self.config.API_VERSION}",
        }

        if self.config.AUTH_TYPE == "oauth2":
            access_token = self._get_oauth2_token()
            headers["Authorization"] = f"Bearer {access_token}"
        elif self.config.API_KEY:
            if self.config.AUTH_TYPE == "bearer":
                headers["Authorization"] = f"Bearer {self.config.API_KEY}"
            elif self.config.AUTH_TYPE == "x-api-key":
                headers["x-api-key"] = self.config.API_KEY
            elif self.config.AUTH_TYPE == "basic":
                credentials = f"{self.config.API_KEY}:{self.config.API_SECRET}"
                encoded = base64.b64encode(credentials.encode()).decode()
                headers["Authorization"] = f"Basic {encoded}"

        if custom_headers:
            headers.update(custom_headers)
        return headers

    def _build_url(self, endpoint: str) -> str:
        if endpoint.startswith("http"):
            return endpoint

        base_url = self.config.BASE_URL.rstrip("/")
        endpoint = endpoint.lstrip("/")
        url = f"{base_url}/{endpoint}"

        api_version = self.config.API_VERSION
        duplicate = f"/api/{api_version}/api/{api_version}/"
        if duplicate in url:
            url = url.replace(duplicate, f"/api/{api_version}/")

        self.logger.debug("URL construída: %s", url)
        return url

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = self._build_url(endpoint)
        kwargs.setdefault("timeout", self.config.REQUEST_TIMEOUT)
        kwargs.setdefault("headers", self._get_headers())

        self.logger.info("Fazendo requisição %s para %s", method.upper(), url)
        response = self.session.request(method, url, **kwargs)
        self.logger.info("Resposta: %s - %s", response.status_code, response.reason)
        return response

    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> Optional[Dict]:
        try:
            response = self._make_request("GET", endpoint, params=params, **kwargs)
            if response.status_code == 200:
                return response.json()
            if response.status_code == 404:
                self.logger.warning("Endpoint não encontrado: %s %s", response.status_code, response.reason)
                return {"data": [], "_not_found": True}
            self.logger.error("Erro na requisição: %s %s", response.status_code, response.reason)
            return None
        except Exception as e:
            self.logger.error("Erro na requisição GET: %s", e)
            return None

    def post(self, endpoint: str, data: Optional[Dict] = None, **kwargs) -> Optional[Dict]:
        try:
            if data is not None:
                kwargs["json"] = data
            response = self._make_request("POST", endpoint, **kwargs)
            if response.status_code in (200, 201):
                return response.json()
            self.logger.error("Erro na requisição: %s %s", response.status_code, response.reason)
            return None
        except Exception as e:
            self.logger.error("Erro na requisição POST: %s", e)
            return None

    def put(self, endpoint: str, data: Optional[Dict] = None, **kwargs) -> Optional[Dict]:
        try:
            if data is not None:
                kwargs["json"] = data
            response = self._make_request("PUT", endpoint, **kwargs)
            if response.status_code in (200, 201, 204):
                return response.json() if response.content else {}
            self.logger.error("Erro na requisição: %s %s", response.status_code, response.reason)
            return None
        except Exception as e:
            self.logger.error("Erro na requisição PUT: %s", e)
            return None

    def delete(self, endpoint: str, **kwargs) -> bool:
        try:
            response = self._make_request("DELETE", endpoint, **kwargs)
            return response.status_code in (200, 204, 404)
        except Exception as e:
            self.logger.error("Erro na requisição DELETE: %s", e)
            return False

    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
    ) -> Optional[Dict]:
        try:
            kwargs = {}
            if params is not None:
                kwargs["params"] = params
            if data is not None:
                kwargs["json"] = data

            response = self._make_request(method, endpoint, **kwargs)

            if response.status_code in (200, 201, 202, 204):
                return response.json() if response.content else {}
            if response.status_code == 404:
                self.logger.warning("Endpoint não encontrado: %s %s", response.status_code, response.reason)
                return {"_not_found": True, "status_code": response.status_code}

            error_body = response.text
            self.logger.error("Erro na requisição: %s %s", response.status_code, response.reason)
            if error_body:
                self.logger.error("Resposta erro: %s", error_body[:1000])
            return None
        except Exception as e:
            self.logger.error("Erro na requisição %s: %s", method, e)
            return None

    def patch(self, endpoint: str, data: Optional[Dict] = None, **kwargs) -> Optional[Dict]:
        return self.request("PATCH", endpoint, data=data)

    def test_connection(self) -> bool:
        try:
            response = self.get(
                f"api/{self.config.API_VERSION}/resources/employees/employees",
                params={"limit": 1},
            )
            if response is not None:
                return True

            response = self._make_request(
                "GET",
                f"api/{self.config.API_VERSION}/resources/api_public/credentials",
            )
            self.logger.info("API respondeu com status %s - Conexão OK", response.status_code)
            return True
        except Exception as e:
            if "401" in str(e):
                self.logger.info("API respondeu com 401 - Conexão OK, problema de autenticação")
                return True
            self.logger.error("Erro no teste de conexão: %s", e)
            return False

    def get_rate_limit_info(self) -> Dict[str, Any]:
        try:
            response = self.session.get(
                f"{self.config.BASE_URL}/api/{self.config.API_VERSION}",
                headers=self._get_headers(),
            )
            rate_limit_info = {}
            for header in ("X-RateLimit-Limit", "X-RateLimit-Remaining", "X-RateLimit-Reset"):
                if header in response.headers:
                    rate_limit_info[header.replace("X-RateLimit-", "").lower()] = response.headers[header]
            return rate_limit_info
        except Exception as e:
            self.logger.error("Erro ao obter informações de rate limiting: %s", e)
            return {}

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
