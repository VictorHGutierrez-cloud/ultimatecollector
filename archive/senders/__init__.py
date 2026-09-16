"""
Senders module - Módulo de envio de dados (PUSH)
Contém todos os enviadores para enviar dados para a API Factorial
"""

from .attendance_sender import AttendanceSender

__all__ = ['AttendanceSender']
