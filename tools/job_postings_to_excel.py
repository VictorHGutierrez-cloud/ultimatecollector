"""
Script para converter dados de Job Postings (JSON) em arquivo Excel (.xlsx)
Converte dados JSON de vagas de emprego em planilha Excel formatada
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import json
import re
from html import unescape
from openpyxl.utils import get_column_letter


def clean_html(html_text):
    """
    Remove tags HTML e limpa o texto
    """
    if html_text is None:
        return None
    
    # Remove tags HTML
    text = re.sub(r'<[^>]+>', '', html_text)
    # Decodifica entidades HTML
    text = unescape(text)
    # Remove espaços extras
    text = ' '.join(text.split())
    return text


def format_salary(salary_cents, salary_period):
    """
    Formata salário de centavos para formato legível
    """
    if salary_cents is None:
        return None
    
    salary = salary_cents / 100
    
    if salary_period == "monthly":
        return f"R$ {salary:,.2f}/mês"
    elif salary_period == "annual":
        return f"R$ {salary:,.2f}/ano"
    else:
        return f"R$ {salary:,.2f}"


def convert_job_postings_to_excel(json_data, output_filename=None):
    """
    Converte dados JSON de job postings em arquivo Excel (.xlsx)

    Args:
        json_data: Dicionário com estrutura contendo 'data' e 'meta'
        output_filename: Nome do arquivo de saída (opcional)

    Returns:
        Caminho do arquivo Excel criado
    """
    # Gerar nome do arquivo se não fornecido
    if output_filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"job_postings_{timestamp}.xlsx"

    # Garantir extensão .xlsx
    if not output_filename.endswith('.xlsx'):
        output_filename += '.xlsx'

    print("🔄 Convertendo Job Postings para Excel...")
    num_records = len(json_data.get('data', []))
    print(f"📊 Processando {num_records} registros...")

    try:
        # Criar DataFrame a partir dos dados
        if json_data.get('data'):
            # Processar e normalizar os dados
            data_normalized = []
            for item in json_data['data']:
                item_copy = item.copy()
                
                # Limpar HTML da descrição
                if 'description' in item_copy and item_copy['description']:
                    item_copy['description'] = clean_html(item_copy['description'])
                
                # Formatar salários
                if 'salary_from_amount_in_cents' in item_copy:
                    salary_from = item_copy.get('salary_from_amount_in_cents')
                    salary_to = item_copy.get('salary_to_amount_in_cents')
                    salary_period = item_copy.get('salary_period', '')
                    
                    if salary_from is not None:
                        if salary_to is not None:
                            salary_from_fmt = format_salary(salary_from, salary_period)
                            salary_to_fmt = format_salary(salary_to, salary_period)
                            item_copy['salary_range'] = f"{salary_from_fmt} - {salary_to_fmt}"
                        else:
                            item_copy['salary_range'] = format_salary(
                                salary_from, salary_period)
                    else:
                        item_copy['salary_range'] = None
                
                # Converter valores booleanos para texto mais legível
                if 'remote' in item_copy:
                    item_copy['remote'] = 'Sim' if item_copy['remote'] else 'Não'
                if 'hide_salary' in item_copy:
                    item_copy['hide_salary'] = 'Sim' if item_copy['hide_salary'] else 'Não'
                
                # Converter valores None para string vazia
                # para melhor visualização no Excel
                for key, value in item_copy.items():
                    if value is None:
                        item_copy[key] = ''
                
                data_normalized.append(item_copy)

            df_data = pd.DataFrame(data_normalized)
            
            # Reordenar colunas para melhor visualização
            preferred_order = [
                'id', 'title', 'status', 'description', 'contract_type', 
                'workplace_type', 'remote', 'schedule_type', 'salary_range',
                'salary_format', 'salary_from_amount_in_cents', 'salary_to_amount_in_cents',
                'salary_period', 'hide_salary', 'url', 'published_at', 'created_at',
                'company_id', 'ats_company_id', 'team_id', 'location_id', 
                'legal_entity_id', 'cv_requirement', 'cover_letter_requirement',
                'phone_requirement', 'photo_requirement', 'personal_url_requirement'
            ]
            
            # Reordenar colunas (mantém as que não estão na lista no final)
            existing_cols = [col for col in preferred_order
                             if col in df_data.columns]
            other_cols = [col for col in df_data.columns
                          if col not in preferred_order]
            df_data = df_data[existing_cols + other_cols]
            
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
                df_data.to_excel(writer, sheet_name='Vagas', index=False)
                
                # Ajustar largura das colunas
                worksheet = writer.sheets['Vagas']
                for idx, col in enumerate(df_data.columns, 1):
                    max_length = max(
                        df_data[col].astype(str).map(len).max(),
                        len(str(col))
                    )
                    # Limitar largura máxima
                    adjusted_width = min(max_length + 2, 50)
                    column_letter = get_column_letter(idx)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
                
                num_rows = len(df_data)
                num_cols = len(df_data.columns)
                print(f"✅ Aba 'Vagas' criada com {num_rows} linhas "
                      f"e {num_cols} colunas")

            # Aba 2: Metadados
            if not df_meta.empty:
                df_meta.to_excel(writer, sheet_name='Metadados', index=False)
                print("✅ Aba 'Metadados' criada")

        print(f"✅ Arquivo Excel criado com sucesso: {output_filename}")
        file_path = Path(output_filename).absolute()
        print(f"📁 Localização: {file_path}")

        return output_filename

    except Exception as e:
        print(f"❌ Erro ao converter para Excel: {e}")
        raise


def load_json_from_file(filepath):
    """
    Carrega JSON de um arquivo
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


if __name__ == "__main__":
    # Dados JSON de exemplo
    json_data = {
        "data": [
            {
                "id": 249078,
                "company_id": 281337,
                "ats_company_id": 50021,
                "title": "teste",
                "description": None,
                "contract_type": None,
                "workplace_type": "hybrid",
                "remote": False,
                "status": "cancelled",
                "schedule_type": None,
                "team_id": 176860,
                "location_id": 352601,
                "legal_entity_id": 294306,
                "salary_format": None,
                "salary_from_amount_in_cents": None,
                "salary_to_amount_in_cents": None,
                "hide_salary": False,
                "cv_requirement": "mandatory",
                "cover_letter_requirement": "optional",
                "phone_requirement": "optional",
                "photo_requirement": "optional",
                "personal_url_requirement": "optional",
                "url": None,
                "salary_period": "annual",
                "published_at": None,
                "created_at": "2025-06-09T18:48:29.000Z"
            },
            {
                "id": 257828,
                "company_id": 281337,
                "ats_company_id": 50021,
                "title": "MOTORISTA",
                "description": "<p class=\"TextEditorTheme__paragraph\" dir=\"ltr\"><span style=\"white-space:pre-wrap;\">TESTE TESTE TESTE</span></p>",
                "contract_type": "indefinite",
                "workplace_type": "onsite",
                "remote": False,
                "status": "draft",
                "schedule_type": "full_time",
                "team_id": 177073,
                "location_id": 355009,
                "legal_entity_id": 296020,
                "salary_format": "fixed_amount",
                "salary_from_amount_in_cents": 309100,
                "salary_to_amount_in_cents": None,
                "hide_salary": False,
                "cv_requirement": "mandatory",
                "cover_letter_requirement": "optional",
                "phone_requirement": "optional",
                "photo_requirement": "optional",
                "personal_url_requirement": "optional",
                "url": None,
                "salary_period": "monthly",
                "published_at": None,
                "created_at": "2025-07-24T14:56:27.000Z"
            },
            {
                "id": 258919,
                "company_id": 281337,
                "ats_company_id": 50021,
                "title": "AUXILIAR DE LOGÍSTICA",
                "description": "<p class=\"TextEditorTheme__paragraph\" dir=\"ltr\" style=\"text-align:justify;\"><span style=\"white-space:pre-wrap;\">Descrição de atividades:</span></p><p class=\"TextEditorTheme__paragraph\" style=\"text-align:justify;\"><br></p><p class=\"TextEditorTheme__paragraph\" dir=\"ltr\" style=\"text-align:justify;\"><span style=\"white-space:pre-wrap;\">          Realizar a conferência e análise de documentos e mantê-los em segurança;</span></p><p class=\"TextEditorTheme__paragraph\" dir=\"ltr\" style=\"text-align:justify;\"><span style=\"white-space:pre-wrap;\">·         Realizar ordem de coleta;</span></p><p class=\"TextEditorTheme__paragraph\" dir=\"ltr\" style=\"text-align:justify;\"><span style=\"white-space:pre-wrap;\">·         Acompanhar ordem de coleta;</span></p><p class=\"TextEditorTheme__paragraph\" dir=\"ltr\" style=\"text-align:justify;\"><span style=\"white-space:pre-wrap;\">·         Acompanhar o andamento dos transportes do início ao fim;</span></p><p class=\"TextEditorTheme__paragraph\" dir=\"ltr\" style=\"text-align:justify;\"><span style=\"white-space:pre-wrap;\">·         Participar de programa de treinamento, sempre que convocado.</span></p><p class=\"TextEditorTheme__paragraph\" dir=\"ltr\" style=\"text-align:justify;\"><span style=\"white-space:pre-wrap;\">·         Responsável pelo faturamento;</span></p><p class=\"TextEditorTheme__paragraph\" dir=\"ltr\"><span style=\"white-space:pre-wrap;\">          Ordenar ordem de coleta para o motorista designado.</span></p><p class=\"TextEditorTheme__paragraph\"><br></p><p class=\"TextEditorTheme__paragraph\" dir=\"ltr\"><span style=\"white-space:pre-wrap;\">Requisitos :</span></p><p class=\"TextEditorTheme__paragraph\"><br></p><p class=\"TextEditorTheme__paragraph\" dir=\"ltr\" style=\"text-align:justify;\"><span style=\"white-space:pre-wrap;\">Superior em Logística (cursando ou completo)</span></p><p class=\"TextEditorTheme__paragraph\" dir=\"ltr\" style=\"text-align:justify;\"><span style=\"white-space:pre-wrap;\">Conhecimento em sistema para emissão de Processos, ordem, CT-e, MDF-e, contrato de frete e relatórios de processos administitivos (Transporte). </span></p>",
                "contract_type": "indefinite",
                "workplace_type": "onsite",
                "remote": False,
                "status": "published",
                "schedule_type": "full_time",
                "team_id": 177073,
                "location_id": 355009,
                "legal_entity_id": 296020,
                "salary_format": "fixed_amount",
                "salary_from_amount_in_cents": 200000,
                "salary_to_amount_in_cents": None,
                "hide_salary": False,
                "cv_requirement": "mandatory",
                "cover_letter_requirement": "optional",
                "phone_requirement": "optional",
                "photo_requirement": "optional",
                "personal_url_requirement": "optional",
                "url": "https://omega-solutions.factorialhr.com.br/job_posting/auxiliar-de-logistica-258919",
                "salary_period": "monthly",
                "published_at": "2025-08-04T13:31:02.072Z",
                "created_at": "2025-08-04T13:07:20.000Z"
            },
            {
                "id": 260006,
                "company_id": 281337,
                "ats_company_id": 50021,
                "title": "ASSISTENTE DE COEMX",
                "description": None,
                "contract_type": None,
                "workplace_type": "hybrid",
                "remote": False,
                "status": "draft",
                "schedule_type": None,
                "team_id": 177063,
                "location_id": 352601,
                "legal_entity_id": 294306,
                "salary_format": None,
                "salary_from_amount_in_cents": None,
                "salary_to_amount_in_cents": None,
                "hide_salary": False,
                "cv_requirement": "mandatory",
                "cover_letter_requirement": "optional",
                "phone_requirement": "optional",
                "photo_requirement": "optional",
                "personal_url_requirement": "optional",
                "url": None,
                "salary_period": "annual",
                "published_at": None,
                "created_at": "2025-08-12T17:23:02.000Z"
            },
            {
                "id": 260007,
                "company_id": 281337,
                "ats_company_id": 50021,
                "title": "ASSISTENTE COMEX",
                "description": "<p class=\"TextEditorTheme__paragraph\" dir=\"ltr\"><span style=\"white-space:pre-wrap;\">TESTETETSTETETSTETETS</span></p>",
                "contract_type": "indefinite",
                "workplace_type": "hybrid",
                "remote": False,
                "status": "published",
                "schedule_type": "full_time",
                "team_id": 177064,
                "location_id": 352601,
                "legal_entity_id": 294306,
                "salary_format": "fixed_amount",
                "salary_from_amount_in_cents": 250000,
                "salary_to_amount_in_cents": None,
                "hide_salary": False,
                "cv_requirement": "mandatory",
                "cover_letter_requirement": "optional",
                "phone_requirement": "mandatory",
                "photo_requirement": "optional",
                "personal_url_requirement": "optional",
                "url": "https://omega-solutions.factorialhr.com.br/job_posting/assistente-comex-260007",
                "salary_period": "monthly",
                "published_at": "2025-08-12T17:45:05.789Z",
                "created_at": "2025-08-12T17:28:11.000Z"
            },
            {
                "id": 265923,
                "company_id": 281337,
                "ats_company_id": 50021,
                "title": "Assistente Faturamento (Comércio Exterior)",
                "description": "<p>Oportunidade para atuar com Comércio Exterior na área financeira</p><p>Requisitos:</p><p>Ter atuado com acompanhamento, conferência e validação das notas fiscais recebidas.</p><p>Cadastro de NF faturadas no sistema da empresa;</p><p>Garantir que todos os processos sejam realizados com precisão e dentro dos prazos estabelecidos.</p><p>Desejável formação completa em: Comércio Exterior / Administração / Gestão Financeira</p><p>Desejável ter conhecimento com pacote office intermediário</p>",
                "contract_type": "clt",
                "workplace_type": "hybrid",
                "remote": False,
                "status": "unlisted",
                "schedule_type": "full_time",
                "team_id": None,
                "location_id": 352601,
                "legal_entity_id": 294306,
                "salary_format": "fixed_amount",
                "salary_from_amount_in_cents": 250,
                "salary_to_amount_in_cents": None,
                "hide_salary": False,
                "cv_requirement": "optional",
                "cover_letter_requirement": "optional",
                "phone_requirement": "optional",
                "photo_requirement": "optional",
                "personal_url_requirement": "optional",
                "url": "https://omega-solutions.factorialhr.com.br/job_posting/assistente-faturamento-comercio-exterior-265923",
                "salary_period": "monthly",
                "published_at": "2025-09-26T12:11:41.343Z",
                "created_at": "2025-09-26T12:03:33.000Z"
            },
            {
                "id": 266190,
                "company_id": 281337,
                "ats_company_id": 50021,
                "title": "Assistente",
                "description": None,
                "contract_type": None,
                "workplace_type": "onsite",
                "remote": False,
                "status": "draft",
                "schedule_type": None,
                "team_id": None,
                "location_id": 352601,
                "legal_entity_id": None,
                "salary_format": None,
                "salary_from_amount_in_cents": None,
                "salary_to_amount_in_cents": None,
                "hide_salary": False,
                "cv_requirement": "mandatory",
                "cover_letter_requirement": "optional",
                "phone_requirement": "optional",
                "photo_requirement": "optional",
                "personal_url_requirement": "optional",
                "url": None,
                "salary_period": "annual",
                "published_at": None,
                "created_at": "2025-09-29T16:45:43.000Z"
            },
            {
                "id": 266383,
                "company_id": 281337,
                "ats_company_id": 50021,
                "title": "Teste",
                "description": None,
                "contract_type": None,
                "workplace_type": "hybrid",
                "remote": False,
                "status": "draft",
                "schedule_type": None,
                "team_id": None,
                "location_id": 352601,
                "legal_entity_id": 294306,
                "salary_format": None,
                "salary_from_amount_in_cents": None,
                "salary_to_amount_in_cents": None,
                "hide_salary": False,
                "cv_requirement": "optional",
                "cover_letter_requirement": "optional",
                "phone_requirement": "optional",
                "photo_requirement": "optional",
                "personal_url_requirement": "optional",
                "url": None,
                "salary_period": "annual",
                "published_at": None,
                "created_at": "2025-09-30T16:16:46.000Z"
            },
            {
                "id": 266384,
                "company_id": 281337,
                "ats_company_id": 50021,
                "title": "Teste",
                "description": None,
                "contract_type": None,
                "workplace_type": "hybrid",
                "remote": False,
                "status": "draft",
                "schedule_type": None,
                "team_id": 176860,
                "location_id": 352601,
                "legal_entity_id": 294306,
                "salary_format": None,
                "salary_from_amount_in_cents": None,
                "salary_to_amount_in_cents": None,
                "hide_salary": False,
                "cv_requirement": "optional",
                "cover_letter_requirement": "optional",
                "phone_requirement": "optional",
                "photo_requirement": "optional",
                "personal_url_requirement": "optional",
                "url": None,
                "salary_period": "annual",
                "published_at": None,
                "created_at": "2025-09-30T16:18:33.000Z"
            }
        ],
        "meta": {
            "has_next_page": False,
            "has_previous_page": False,
            "start_cursor": "MjQ5MDc4",
            "end_cursor": "MjY2Mzg0",
            "total": 9,
            "limit": 100
        }
    }
    
    # Para usar com arquivo JSON, descomente as linhas abaixo:
    # json_data = load_json_from_file('seu_arquivo.json')  # noqa: E501
    
    # Executar conversão
    output_file = convert_job_postings_to_excel(json_data)
    print(f"\n🎉 Conversão concluída! Arquivo salvo como: {output_file}")

