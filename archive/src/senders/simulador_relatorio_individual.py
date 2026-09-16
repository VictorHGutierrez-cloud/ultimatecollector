#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulador de Relatório Individual de Sobreaviso
Converte dados da query SQL em batidas reais via SENDER
"""

import sys
import os
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional
import json

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from senders.attendance_sender import AttendanceSender


class SimuladorRelatorioIndividual:
    """Simulador que converte dados do relatório individual em batidas reais"""
    
    def __init__(self, config_name: str = None):
        """Inicializa o simulador"""
        self.sender = AttendanceSender(config_name)
        self.logger = self.sender.logger
        
    def processar_dados_relatorio(self, dados_relatorio: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Processa dados do relatório individual e converte em batidas
        
        Args:
            dados_relatorio: Lista de dicionários com dados da query SQL
            
        Returns:
            Lista de batidas processadas para envio
        """
        batidas_processadas = []
        
        for registro in dados_relatorio:
            colaborador_id = registro.get('colaborador_id')
            nome_completo = registro.get('nome_completo')
            data_str = registro.get('data')  # Formato: DD/MM/YYYY
            
            if not colaborador_id or not data_str:
                continue
                
            # Converter data para datetime
            try:
                data = datetime.strptime(data_str, '%d/%m/%Y').date()
            except ValueError:
                self.logger.warning(f"Data inválida: {data_str}")
                continue
            
            # Processar batidas do dia
            batidas_dia = self._extrair_batidas_dia(registro, data)
            
            if batidas_dia:
                batidas_processadas.extend(batidas_dia)
                self.logger.info(f"Processadas {len(batidas_dia)} batidas para {nome_completo} em {data_str}")
        
        return batidas_processadas
    
    def _extrair_batidas_dia(self, registro: Dict[str, Any], data: datetime.date) -> List[Dict[str, Any]]:
        """
        Extrai todas as batidas de um dia específico
        
        Args:
            registro: Dados do registro do dia
            data: Data do registro
            
        Returns:
            Lista de batidas (entrada/saída) do dia
        """
        batidas = []
        colaborador_id = registro.get('colaborador_id')
        
        # Processar até 4 pares de batidas
        for i in range(1, 5):
            entrada_key = f'entrada_{i}'
            saida_key = f'saida_{i}'
            
            entrada_hora = registro.get(entrada_key)
            saida_hora = registro.get(saida_key)
            
            # Se tem entrada, processar
            if entrada_hora:
                entrada_dt = self._criar_datetime(data, entrada_hora)
                batidas.append({
                    'tipo': 'clock_in',
                    'employee_id': colaborador_id,
                    'datetime': entrada_dt,
                    'observations': f'Entrada {i} - Simulação Relatório Individual'
                })
            
            # Se tem saída, processar
            if saida_hora:
                saida_dt = self._criar_datetime(data, saida_hora)
                batidas.append({
                    'tipo': 'clock_out',
                    'employee_id': colaborador_id,
                    'datetime': saida_dt,
                    'observations': f'Saída {i} - Simulação Relatório Individual'
                })
        
        return batidas
    
    def _criar_datetime(self, data: datetime.date, hora_str: str) -> datetime:
        """
        Cria datetime combinando data e hora
        
        Args:
            data: Data do registro
            hora_str: Hora no formato HH:MM
            
        Returns:
            datetime com timezone UTC
        """
        try:
            hora = datetime.strptime(hora_str, '%H:%M').time()
            return datetime.combine(data, hora).replace(tzinfo=timezone.utc)
        except ValueError:
            self.logger.warning(f"Hora inválida: {hora_str}")
            return datetime.now(timezone.utc)
    
    def enviar_batidas_simuladas(self, batidas: List[Dict[str, Any]], modo_simulacao: bool = True) -> Dict[str, Any]:
        """
        Envia batidas simuladas para a API
        
        Args:
            batidas: Lista de batidas para enviar
            modo_simulacao: Se True, apenas simula (não envia realmente)
            
        Returns:
            Resultado do envio
        """
        resultados = {
            'total_batidas': len(batidas),
            'sucessos': 0,
            'erros': 0,
            'detalhes': []
        }
        
        if modo_simulacao:
            self.logger.info("🔍 MODO SIMULAÇÃO ATIVADO - Nenhuma batida será enviada realmente")
        
        for i, batida in enumerate(batidas, 1):
            try:
                if modo_simulacao:
                    # Simular envio
                    resultado = {
                        'status': 'simulado',
                        'mensagem': f'Batida {i} simulada com sucesso',
                        'dados': batida
                    }
                    resultados['sucessos'] += 1
                else:
                    # Envio real
                    if batida['tipo'] == 'clock_in':
                        response = self.sender.clock_in(
                            employee_id=batida['employee_id'],
                            clock_time=batida['datetime'],
                            observations=batida['observations']
                        )
                    else:  # clock_out
                        response = self.sender.clock_out(
                            employee_id=batida['employee_id'],
                            clock_time=batida['datetime'],
                            observations=batida['observations']
                        )
                    
                    resultado = {
                        'status': 'enviado',
                        'response': response,
                        'dados': batida
                    }
                    resultados['sucessos'] += 1
                
                resultados['detalhes'].append(resultado)
                self.logger.info(f"✅ Batida {i}/{len(batidas)} processada: {batida['tipo']} para funcionário {batida['employee_id']}")
                
            except Exception as e:
                erro = {
                    'status': 'erro',
                    'erro': str(e),
                    'dados': batida
                }
                resultados['erros'] += 1
                resultados['detalhes'].append(erro)
                self.logger.error(f"❌ Erro na batida {i}: {e}")
        
        return resultados
    
    def simular_cenario_sobreaviso(self, colaborador_id: int, data_inicio: str, dias: int = 7) -> List[Dict[str, Any]]:
        """
        Simula um cenário de sobreaviso para um colaborador
        
        Args:
            colaborador_id: ID do colaborador
            data_inicio: Data de início no formato DD/MM/YYYY
            dias: Número de dias para simular
            
        Returns:
            Lista de batidas simuladas
        """
        batidas_simuladas = []
        
        try:
            data_base = datetime.strptime(data_inicio, '%d/%m/%Y').date()
        except ValueError:
            self.logger.error(f"Data inválida: {data_inicio}")
            return []
        
        for i in range(dias):
            data_atual = data_base + timedelta(days=i)
            dia_semana = data_atual.weekday()  # 0=Segunda, 6=Domingo
            
            # Criar cenário baseado no dia da semana
            if dia_semana < 5:  # Segunda a Sexta
                batidas_dia = self._criar_cenario_segunda_sexta(data_atual, colaborador_id)
            else:  # Sábado e Domingo
                batidas_dia = self._criar_cenario_fim_semana(data_atual, colaborador_id)
            
            batidas_simuladas.extend(batidas_dia)
        
        return batidas_simuladas
    
    def _criar_cenario_segunda_sexta(self, data: datetime.date, colaborador_id: int) -> List[Dict[str, Any]]:
        """Cria cenário de batidas para Segunda a Sexta"""
        batidas = []
        
        # Jornada regular: 08:00 - 12:00, 13:00 - 17:00
        entrada_1 = datetime.combine(data, datetime.strptime('08:00', '%H:%M').time()).replace(tzinfo=timezone.utc)
        saida_1 = datetime.combine(data, datetime.strptime('12:00', '%H:%M').time()).replace(tzinfo=timezone.utc)
        entrada_2 = datetime.combine(data, datetime.strptime('13:00', '%H:%M').time()).replace(tzinfo=timezone.utc)
        saida_2 = datetime.combine(data, datetime.strptime('17:00', '%H:%M').time()).replace(tzinfo=timezone.utc)
        
        # Sobreaviso: 19:00 - 22:00 (apenas alguns dias)
        if data.day % 3 == 0:  # A cada 3 dias
            entrada_3 = datetime.combine(data, datetime.strptime('19:00', '%H:%M').time()).replace(tzinfo=timezone.utc)
            saida_3 = datetime.combine(data, datetime.strptime('22:00', '%H:%M').time()).replace(tzinfo=timezone.utc)
            
            batidas.extend([
                {'tipo': 'clock_in', 'employee_id': colaborador_id, 'datetime': entrada_3, 'observations': 'Sobreaviso - Entrada'},
                {'tipo': 'clock_out', 'employee_id': colaborador_id, 'datetime': saida_3, 'observations': 'Sobreaviso - Saída'}
            ])
        
        # Jornada regular
        batidas.extend([
            {'tipo': 'clock_in', 'employee_id': colaborador_id, 'datetime': entrada_1, 'observations': 'Jornada Regular - Entrada'},
            {'tipo': 'clock_out', 'employee_id': colaborador_id, 'datetime': saida_1, 'observations': 'Jornada Regular - Saída Almoço'},
            {'tipo': 'clock_in', 'employee_id': colaborador_id, 'datetime': entrada_2, 'observations': 'Jornada Regular - Retorno Almoço'},
            {'tipo': 'clock_out', 'employee_id': colaborador_id, 'datetime': saida_2, 'observations': 'Jornada Regular - Saída'}
        ])
        
        return batidas
    
    def _criar_cenario_fim_semana(self, data: datetime.date, colaborador_id: int) -> List[Dict[str, Any]]:
        """Cria cenário de batidas para Sábado e Domingo"""
        batidas = []
        
        # Sobreaviso fim de semana: 09:00 - 21:00 (apenas alguns dias)
        if data.day % 4 == 0:  # A cada 4 dias
            entrada_1 = datetime.combine(data, datetime.strptime('09:00', '%H:%M').time()).replace(tzinfo=timezone.utc)
            saida_1 = datetime.combine(data, datetime.strptime('21:00', '%H:%M').time()).replace(tzinfo=timezone.utc)
            
            batidas.extend([
                {'tipo': 'clock_in', 'employee_id': colaborador_id, 'datetime': entrada_1, 'observations': 'Sobreaviso Fim de Semana - Entrada'},
                {'tipo': 'clock_out', 'employee_id': colaborador_id, 'datetime': saida_1, 'observations': 'Sobreaviso Fim de Semana - Saída'}
            ])
        
        return batidas


def exemplo_simulacao_dados_reais():
    """Exemplo usando dados reais do relatório"""
    print("=" * 60)
    print("EXEMPLO: SIMULAÇÃO COM DADOS REAIS DO RELATÓRIO")
    print("=" * 60)
    
    # Dados simulados do relatório (substitua pelos dados reais da query)
    dados_relatorio = [
        {
            'colaborador_id': 1,
            'nome_completo': 'João Silva',
            'data': '05/05/2024',
            'entrada_1': '08:00',
            'saida_1': '12:15',
            'entrada_2': '13:15',
            'saida_2': '17:00',
            'entrada_3': '19:00',
            'saida_3': '22:00',
            'codigo_empresa': '001',
            'horas_regulares': '08:00',
            'horas_sobreaviso_regra': '03:00'
        },
        {
            'colaborador_id': 1,
            'nome_completo': 'João Silva',
            'data': '06/05/2024',
            'entrada_1': '08:13',
            'saida_1': '14:28',
            'entrada_2': '15:28',
            'saida_2': '17:08',
            'entrada_3': '19:08',
            'saida_3': '21:06',
            'codigo_empresa': '001',
            'horas_regulares': '08:30',
            'horas_sobreaviso_regra': '01:58'
        }
    ]
    
    # Criar simulador
    simulador = SimuladorRelatorioIndividual()
    
    # Processar dados do relatório
    print("📊 Processando dados do relatório...")
    batidas = simulador.processar_dados_relatorio(dados_relatorio)
    print(f"✅ Processadas {len(batidas)} batidas")
    
    # Simular envio (modo simulação)
    print("\n🔍 Simulando envio das batidas...")
    resultado = simulador.enviar_batidas_simuladas(batidas, modo_simulacao=True)
    
    print(f"\n📈 RESULTADO DA SIMULAÇÃO:")
    print(f"   Total de batidas: {resultado['total_batidas']}")
    print(f"   Sucessos: {resultado['sucessos']}")
    print(f"   Erros: {resultado['erros']}")
    
    # Mostrar detalhes das primeiras 5 batidas
    print(f"\n📋 DETALHES (primeiras 5 batidas):")
    for i, detalhe in enumerate(resultado['detalhes'][:5], 1):
        print(f"   {i}. {detalhe['dados']['tipo']} - Funcionário {detalhe['dados']['employee_id']} - {detalhe['dados']['datetime']}")


def exemplo_simulacao_cenario():
    """Exemplo criando cenário de sobreaviso"""
    print("\n" + "=" * 60)
    print("EXEMPLO: SIMULAÇÃO DE CENÁRIO DE SOBREAVISO")
    print("=" * 60)
    
    simulador = SimuladorRelatorioIndividual()
    
    # Simular 7 dias de sobreaviso para funcionário ID 1
    print("🎭 Criando cenário de sobreaviso para 7 dias...")
    batidas = simulador.simular_cenario_sobreaviso(
        colaborador_id=1,
        data_inicio='01/05/2024',
        dias=7
    )
    
    print(f"✅ Criadas {len(batidas)} batidas simuladas")
    
    # Simular envio
    print("\n🔍 Simulando envio do cenário...")
    resultado = simulador.enviar_batidas_simuladas(batidas, modo_simulacao=True)
    
    print(f"\n📈 RESULTADO DO CENÁRIO:")
    print(f"   Total de batidas: {resultado['total_batidas']}")
    print(f"   Sucessos: {resultado['sucessos']}")
    print(f"   Erros: {resultado['erros']}")


def main():
    """Função principal"""
    print("🎭 SIMULADOR DE RELATÓRIO INDIVIDUAL DE SOBREAVISO")
    print("=" * 60)
    print("Este simulador converte dados da query SQL em batidas reais")
    print("e permite testar diferentes cenários de sobreaviso.")
    print()
    
    try:
        # Exemplo 1: Dados reais do relatório
        exemplo_simulacao_dados_reais()
        
        # Exemplo 2: Cenário simulado
        exemplo_simulacao_cenario()
        
        print("\n" + "=" * 60)
        print("✅ SIMULAÇÕES CONCLUÍDAS!")
        print("=" * 60)
        print()
        print("📝 COMO USAR:")
        print("-" * 20)
        print("1. Execute a query SQL para obter dados do relatório")
        print("2. Use SimuladorRelatorioIndividual.processar_dados_relatorio()")
        print("3. Use enviar_batidas_simuladas() para simular ou enviar")
        print("4. Use simular_cenario_sobreaviso() para criar cenários")
        print()
        print("⚠️  IMPORTANTE:")
        print("- Use modo_simulacao=True para testar sem enviar")
        print("- Use modo_simulacao=False para envio real")
        print("- Verifique sempre os dados antes do envio real")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Simulação interrompida pelo usuário")
    except Exception as e:
        print(f"\n\n❌ Erro: {e}")


if __name__ == "__main__":
    main()
