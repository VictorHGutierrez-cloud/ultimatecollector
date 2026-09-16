#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 ANALISADOR DE DADOS REAIS - Analisa os dados coletados da API Factorial
"""

import json
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

def analisar_dados_presenca():
    """Analisa os dados de presença coletados"""
    print("📊 ANALISANDO DADOS REAIS DE PRESENÇA")
    print("=" * 50)
    
    # Carregar dados
    arquivo = Path("Dados_Coletados/Dados_Brutos/Dados da API/Presença/teste_shifts_20250909_232732.json")
    
    if not arquivo.exists():
        print("❌ Arquivo de dados não encontrado!")
        return
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    print(f"📋 Total de registros: {len(dados)}")
    
    # Converter para DataFrame
    df = pd.DataFrame(dados)
    
    # Análises básicas
    print(f"\n📊 ESTATÍSTICAS GERAIS:")
    print(f"   👥 Funcionários únicos: {df['employee_id'].nunique()}")
    print(f"   📅 Período: {df['date'].min()} até {df['date'].max()}")
    print(f"   ⏰ Horas médias por dia: {df['minutes'].mean()/60:.1f}h")
    print(f"   🏢 Localização principal: {df['location_type'].mode().iloc[0]}")
    
    # Análise por funcionário
    print(f"\n👥 ANÁLISE POR FUNCIONÁRIO:")
    funcionarios = df.groupby('employee_id').agg({
        'date': 'count',
        'minutes': ['sum', 'mean'],
        'clock_in': 'first',
        'clock_out': 'first'
    }).round(2)
    
    funcionarios.columns = ['Dias_Trabalhados', 'Total_Minutos', 'Media_Minutos', 'Primeiro_Entrada', 'Primeiro_Saida']
    funcionarios['Total_Horas'] = (funcionarios['Total_Minutos'] / 60).round(1)
    funcionarios['Media_Horas'] = (funcionarios['Media_Minutos'] / 60).round(1)
    
    print(funcionarios)
    
    # Análise temporal
    print(f"\n📅 ANÁLISE TEMPORAL:")
    df['date'] = pd.to_datetime(df['date'])
    df['dia_semana'] = df['date'].dt.day_name()
    df['mes'] = df['date'].dt.month
    
    # Horas por dia da semana
    horas_por_dia = df.groupby('dia_semana')['minutes'].mean() / 60
    print(f"   ⏰ Média de horas por dia da semana:")
    for dia, horas in horas_por_dia.items():
        print(f"      {dia}: {horas:.1f}h")
    
    # Análise de pontualidade
    print(f"\n⏰ ANÁLISE DE PONTUALIDADE:")
    df['clock_in_time'] = pd.to_datetime(df['clock_in'], format='%H:%M').dt.time
    df['clock_out_time'] = pd.to_datetime(df['clock_out'], format='%H:%M').dt.time
    
    # Funcionários mais pontuais (chegam cedo)
    mais_pontuais = df.groupby('employee_id')['clock_in'].min().sort_values()
    print(f"   🏆 Funcionário mais pontual: {mais_pontuais.index[0]} (chega às {mais_pontuais.iloc[0]})")
    
    # Funcionários que trabalham mais
    mais_trabalhadores = df.groupby('employee_id')['minutes'].sum().sort_values(ascending=False)
    print(f"   💪 Funcionário que mais trabalha: {mais_trabalhadores.index[0]} ({mais_trabalhadores.iloc[0]/60:.1f}h total)")
    
    # Análise de localização
    print(f"\n🏢 ANÁLISE DE LOCALIZAÇÃO:")
    localizacoes = df['location_type'].value_counts()
    for loc, count in localizacoes.items():
        print(f"   {loc}: {count} registros ({count/len(df)*100:.1f}%)")
    
    # Salvar relatório
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    relatorio_file = f"relatorio_presenca_{timestamp}.txt"
    
    with open(relatorio_file, 'w', encoding='utf-8') as f:
        f.write("📊 RELATÓRIO DE ANÁLISE DE DADOS REAIS DE PRESENÇA\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"📋 Total de registros: {len(dados)}\n")
        f.write(f"👥 Funcionários únicos: {df['employee_id'].nunique()}\n")
        f.write(f"📅 Período: {df['date'].min()} até {df['date'].max()}\n")
        f.write(f"⏰ Horas médias por dia: {df['minutes'].mean()/60:.1f}h\n\n")
        
        f.write("👥 ANÁLISE POR FUNCIONÁRIO:\n")
        f.write(str(funcionarios))
        f.write("\n\n")
        
        f.write("📅 HORAS POR DIA DA SEMANA:\n")
        for dia, horas in horas_por_dia.items():
            f.write(f"   {dia}: {horas:.1f}h\n")
    
    print(f"\n💾 Relatório salvo: {relatorio_file}")
    
    return df

def analisar_outros_dados():
    """Verifica se há outros dados coletados"""
    print(f"\n🔍 PROCURANDO OUTROS DADOS COLETADOS:")
    print("=" * 50)
    
    base_dir = Path("Dados_Coletados/Dados_Brutos/Dados da API")
    
    categorias_com_dados = []
    
    for categoria_dir in base_dir.iterdir():
        if categoria_dir.is_dir():
            json_files = list(categoria_dir.glob("*.json"))
            if json_files:
                total_size = sum(f.stat().st_size for f in json_files)
                categorias_com_dados.append({
                    'categoria': categoria_dir.name,
                    'arquivos': len(json_files),
                    'tamanho_mb': total_size / (1024*1024)
                })
                print(f"   📁 {categoria_dir.name}: {len(json_files)} arquivos ({total_size/(1024*1024):.1f}MB)")
    
    if categorias_com_dados:
        print(f"\n✅ Categorias com dados encontradas: {len(categorias_com_dados)}")
        return categorias_com_dados
    else:
        print(f"\n⚠️ Apenas dados de presença encontrados")
        return []

def main():
    """Função principal"""
    print("📊 ANALISADOR DE DADOS REAIS DA API FACTORIAL")
    print("=" * 60)
    print("🔍 Analisando os dados que foram coletados com sucesso")
    print("=" * 60)
    
    # Analisar dados de presença
    df_presenca = analisar_dados_presenca()
    
    # Procurar outros dados
    outras_categorias = analisar_outros_dados()
    
    print(f"\n🎯 CONCLUSÕES:")
    print(f"   ✅ Você TEM dados reais da API Factorial!")
    print(f"   📊 {len(df_presenca)} registros de presença analisados")
    print(f"   📁 {len(outras_categorias)} categorias com dados")
    print(f"   🚀 Sistema funcionou perfeitamente antes!")
    
    print(f"\n💡 PRÓXIMOS PASSOS:")
    print(f"   1. Analisar os dados existentes em detalhes")
    print(f"   2. Criar dashboards e relatórios")
    print(f"   3. Obter nova API Key para coletar mais dados")
    print(f"   4. Expandir análise para outras categorias")

if __name__ == "__main__":
    main()
