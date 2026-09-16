#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classe para envio de dados de presença (clock in/clock out) para a API Factorial
"""

import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from core.api_client import APIClient
from dotenv import load_dotenv

# Carregar configurações do arquivo config_unificado.env
env_files = ['config_unificado.env', '.env', 'config.env']
loaded = False
for env_file in env_files:
    if Path(env_file).exists():
        load_dotenv(env_file)
        loaded = True
        break


class AttendanceSender(APIClient):
    """Classe especializada para envio de dados de presença para a API Factorial"""

    def __init__(self, config_name: str = None):
        """Inicializa o sender de presença"""
        super().__init__(config_name)
        self.logger = logging.getLogger(__name__)

    def clock_in(self,
                 employee_id: int,
                 clock_time: Optional[datetime] = None,
                 latitude: Optional[float] = None,
                 longitude: Optional[float] = None,
                 observations: Optional[str] = None) -> Dict[str, Any]:
        """
        Registra clock in de um funcionário

        Args:
            employee_id: ID do funcionário
            clock_time: Data/hora do clock in (se None, usa hora atual)
            latitude: Latitude da localização (opcional)
            longitude: Longitude da localização (opcional)
            observations: Observações sobre o ponto (opcional)

        Returns:
            Dict com a resposta da API

        Raises:
            ValueError: Se employee_id for inválido
            Exception: Se houver erro na requisição
        """
        try:
            # Validar employee_id
            if not isinstance(employee_id, int) or employee_id <= 0:
                raise ValueError("employee_id deve ser um número inteiro positivo")

            # Usar hora atual se não fornecida
            if clock_time is None:
                clock_time = datetime.now(timezone.utc)

            # Preparar dados da requisição
            data = {
                "employee_id": employee_id,
                "now": clock_time.isoformat()
            }

            # Adicionar localização se fornecida
            if latitude is not None and longitude is not None:
                data["latitude"] = latitude
                data["longitude"] = longitude

            # Adicionar observações se fornecidas
            if observations:
                data["observations"] = observations

            self.logger.info("Enviando clock in para funcionário %s às %s",
                            employee_id, clock_time)

            # Fazer requisição para a API
            response = self.post(
                "api/2026-07-01/resources/attendance/shifts/clock_in",
                data=data
            )

            self.logger.info("Clock in registrado com sucesso para funcionário %s",
                            employee_id)
            return response

        except Exception as e:
            self.logger.error("Erro ao registrar clock in: %s", e)
            raise

    def clock_out(self,
                  employee_id: int,
                  clock_time: Optional[datetime] = None,
                  latitude: Optional[float] = None,
                  longitude: Optional[float] = None,
                  observations: Optional[str] = None) -> Dict[str, Any]:
        """
        Registra clock out de um funcionário

        Args:
            employee_id: ID do funcionário
            clock_time: Data/hora do clock out (se None, usa hora atual)
            latitude: Latitude da localização (opcional)
            longitude: Longitude da localização (opcional)
            observations: Observações sobre o ponto (opcional)

        Returns:
            Dict com a resposta da API

        Raises:
            ValueError: Se employee_id for inválido
            Exception: Se houver erro na requisição
        """
        try:
            # Validar employee_id
            if not isinstance(employee_id, int) or employee_id <= 0:
                raise ValueError("employee_id deve ser um número inteiro positivo")

            # Usar hora atual se não fornecida
            if clock_time is None:
                clock_time = datetime.now(timezone.utc)

            # Preparar dados da requisição
            data = {
                "employee_id": employee_id,
                "now": clock_time.isoformat()
            }

            # Adicionar localização se fornecida
            if latitude is not None and longitude is not None:
                data["latitude"] = latitude
                data["longitude"] = longitude

            # Adicionar observações se fornecidas
            if observations:
                data["observations"] = observations

            self.logger.info("Enviando clock out para funcionário %s às %s",
                            employee_id, clock_time)

            # Fazer requisição para a API
            response = self.post(
                "api/2026-07-01/resources/attendance/shifts/clock_out",
                data=data
            )

            self.logger.info("Clock out registrado com sucesso para funcionário %s",
                            employee_id)
            return response

        except Exception as e:
            self.logger.error("Erro ao registrar clock out: %s", e)
            raise

    def register_complete_shift(self,
                               employee_id: int,
                               clock_in_time: datetime,
                               clock_out_time: datetime,
                               latitude: Optional[float] = None,
                               longitude: Optional[float] = None,
                               observations: Optional[str] = None) -> Dict[str, Any]:
        """
        Registra um turno completo (clock in + clock out) de uma vez

        Args:
            employee_id: ID do funcionário
            clock_in_time: Data/hora do clock in
            clock_out_time: Data/hora do clock out
            latitude: Latitude da localização (opcional)
            longitude: Longitude da localização (opcional)
            observations: Observações sobre o ponto (opcional)

        Returns:
            Dict com a resposta da API
        """
        try:
            # Validar employee_id
            if not isinstance(employee_id, int) or employee_id <= 0:
                raise ValueError("employee_id deve ser um número inteiro positivo")

            # Validar que clock_out_time é posterior ao clock_in_time
            if clock_out_time <= clock_in_time:
                raise ValueError("clock_out_time deve ser posterior ao clock_in_time")

            # Preparar dados da requisição
            data = {
                "employee_id": employee_id,
                "date": clock_in_time.strftime("%Y-%m-%d"),
                "clock_in": clock_in_time.strftime("%H:%M"),
                "clock_out": clock_out_time.strftime("%H:%M")
            }

            # Adicionar localização se fornecida
            if latitude is not None and longitude is not None:
                data["latitude"] = latitude
                data["longitude"] = longitude

            # Adicionar observações se fornecidas
            if observations:
                data["observations"] = observations

            self.logger.info("Registrando turno completo para funcionário %s: %s - %s",
                            employee_id, clock_in_time, clock_out_time)

            # Fazer requisição para a API
            response = self.post(
                "api/2026-07-01/resources/attendance/shifts",
                data=data
            )

            self.logger.info("Turno completo registrado com sucesso para funcionário %s",
                            employee_id)
            return response

        except Exception as e:
            self.logger.error("Erro ao registrar turno completo: %s", e)
            raise

    def get_employee_shifts(self, employee_id: int, date: Optional[str] = None) -> Dict[str, Any]:
        """
        Busca os turnos de um funcionário

        Args:
            employee_id: ID do funcionário
            date: Data no formato YYYY-MM-DD (opcional)

        Returns:
            Dict com os turnos do funcionário
        """
        try:
            params = {"employee_id": employee_id}
            if date:
                params["date"] = date

            self.logger.info("Buscando turnos do funcionário %s", employee_id)

            response = self.get(
                "api/2026-07-01/resources/attendance/shifts",
                params=params
            )

            return response

        except Exception as e:
            self.logger.error("Erro ao buscar turnos do funcionário %s: %s",
                            employee_id, e)
            raise

    def validate_employee_id(self, employee_id: int) -> bool:
        """
        Valida se um employee_id existe na API

        Args:
            employee_id: ID do funcionário a validar

        Returns:
            True se o funcionário existe, False caso contrário
        """
        try:
            # Buscar funcionários diretamente da API de employees
            response = self.get("api/2026-07-01/resources/employees/employees", 
                              params={"limit": 100})
            
            # Verificar se o funcionário existe na lista
            employees = response.get('data', [])
            for employee in employees:
                if employee.get('id') == employee_id:
                    return True
            
            return False
            
        except Exception as e:
            self.logger.warning("Erro ao validar funcionário %s: %s", employee_id, e)
            return False
