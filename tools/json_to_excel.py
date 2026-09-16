"""
Script para converter JSON em arquivo Excel (.xlsx)
Converte dados JSON estruturados em planilha Excel
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import json
import sys
from openpyxl.utils import get_column_letter


def load_json_from_file(filepath):
    """Carrega JSON de um arquivo"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def convert_json_to_excel(json_data, output_filename=None):
    """
    Converte dados JSON em arquivo Excel (.xlsx)

    Args:
        json_data: Dicionário com estrutura contendo 'data' e 'meta'
        output_filename: Nome do arquivo de saída (opcional)

    Returns:
        Caminho do arquivo Excel criado
    """
    # Gerar nome do arquivo se não fornecido
    if output_filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"dados_exportados_{timestamp}.xlsx"

    # Garantir extensão .xlsx
    if not output_filename.endswith('.xlsx'):
        output_filename += '.xlsx'

    print("🔄 Convertendo JSON para Excel...")
    num_records = len(json_data.get('data', []))
    print(f"📊 Processando {num_records} registros...")

    try:
        # Criar DataFrame a partir dos dados
        if json_data.get('data'):
            # Converter arrays para strings (Excel não suporta arrays)
            data_normalized = []
            for item in json_data['data']:
                item_copy = item.copy()
                # Converter listas em strings separadas por vírgula
                for key, value in item_copy.items():
                    if isinstance(value, list):
                        item_copy[key] = ', '.join(map(str, value))
                    elif value is None:
                        item_copy[key] = ''  # Converter None para string vazia
                data_normalized.append(item_copy)

            df_data = pd.DataFrame(data_normalized)
        else:
            df_data = pd.DataFrame()

        # Criar DataFrame para metadados
        if json_data.get('meta'):
            df_meta = pd.DataFrame([json_data['meta']])
        else:
            df_meta = pd.DataFrame()

        # Criar arquivo Excel com múltiplas abas
        with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
            # Aba 1: Dados principais
            if not df_data.empty:
                df_data.to_excel(writer, sheet_name='Dados', index=False)
                
                # Ajustar largura das colunas
                worksheet = writer.sheets['Dados']
                for idx, col in enumerate(df_data.columns, 1):
                    max_length = max(
                        df_data[col].astype(str).map(len).max(),
                        len(str(col))
                    )
                    adjusted_width = min(max_length + 2, 50)
                    column_letter = get_column_letter(idx)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
                
                num_rows = len(df_data)
                num_cols = len(df_data.columns)
                print(f"✅ Aba 'Dados' criada com {num_rows} linhas "
                      f"e {num_cols} colunas")

            # Aba 2: Metadados
            if not df_meta.empty:
                df_meta.to_excel(writer, sheet_name='Metadados',
                                 index=False)
                print("✅ Aba 'Metadados' criada")

        print(f"✅ Arquivo Excel criado com sucesso: {output_filename}")
        file_path = Path(output_filename).absolute()
        print(f"📁 Localização: {file_path}")

        return output_filename

    except Exception as e:
        print(f"❌ Erro ao converter para Excel: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    # Verificar se foi passado um arquivo como argumento
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        print(f"📂 Carregando JSON de: {input_file}")
        json_data = load_json_from_file(input_file)
    else:
        # Dados JSON de exemplo (fallback)
        json_data = {
            "data": [
                {
                    "id": 1,
                    "company_id": 1,
                    "name": "CFO",
                    "description": "Financial director of the company.",
                    "legal_entities_ids": [1, 2],
                    "supervisors_ids": [1, 2],
                    "competencies_ids": [1, 2],
                    "archived": True
                }
            ],
            "meta": {
                "start_cursor": "string",
                "end_cursor": "string",
                "has_previous_page": True,
                "has_next_page": True,
                "limit": 0,
                "total": 0
            }
        }
        print("⚠️  Nenhum arquivo fornecido. Usando dados de exemplo.")
        print("💡 Use: python json_to_excel.py arquivo.json")

    # Executar conversão
    output_file = convert_json_to_excel(json_data)
    print(f"\n🎉 Conversão concluída! Arquivo salvo como: {output_file}")
