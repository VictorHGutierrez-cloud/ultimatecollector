"""
Collectors module - Módulo de coleta de dados (PULL)
Contém todos os coletores para buscar dados da API Factorial
"""

from .hr_data_master import HRDataMasterUltimate
from .attendance_collector import AttendanceSpecialist

__all__ = ['HRDataMasterUltimate', 'AttendanceSpecialist']
