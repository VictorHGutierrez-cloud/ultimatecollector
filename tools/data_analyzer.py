#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calcula horas extras por dia a partir de dados de "shifts" (presenca)

Entrada padrao: ultimo arquivo JSON contendo "shifts" salvo em
Dados_Coletados/Dados_Brutos/Dados da API/Presenca

Saida: CSV em Dados_Coletados/Dados_Processados com colunas:
employee_id, date, worked_minutes, worked_hours,
scheduled_hours, overtime_minutes, overtime_hours

Uso rapido:
  python Scripts_Utilitarios/calcular_horas_extras.py --horas-previstas 8

Observacao:
  Se voce ainda nao tem a escala oficial (work_schedule) coletada,
  o script usa uma meta diaria fixa (padrao 8h). Voce pode ajustar
  com --horas-previstas.
"""

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd


PRESENCA_DIR = Path(
    "Dados_Coletados/Dados_Brutos/Dados da API/Presença"
)
SCHEDULE_DIR = Path(
    "Dados_Coletados/Dados_Brutos/Dados da API/Escala de Trabalho"
)
PROCESSADOS_DIR = Path("Dados_Coletados/Dados_Processados")


@dataclass
class OvertimeConfig:
    scheduled_hours_per_day: float = 8.0  # Meta diária padrão em horas


def find_latest_shifts_file(directory: Path) -> Optional[Path]:
    """Encontra o arquivo mais recente com 'shifts' no nome
    dentro do diretorio informado.
    """
    if not directory.exists():
        return None
    candidates = sorted(
        [p for p in directory.glob("*shifts*.json") if p.is_file()],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def find_latest_estimated_times(directory: Path) -> Optional[Path]:
    """Encontra o arquivo mais recente contendo 'estimated_times' no nome."""
    if not directory.exists():
        return None
    candidates = sorted(
        [p for p in directory.glob("*estimated_times*.json") if p.is_file()],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def load_shifts_to_dataframe(file_path: Path) -> pd.DataFrame:
    """Carrega o JSON de shifts para DataFrame normalizado."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as exc:
        raise RuntimeError(f"Erro ao ler JSON '{file_path}': {exc}") from exc

    if not isinstance(data, list) or len(data) == 0:
        raise RuntimeError(
            "Arquivo de shifts vazio ou em formato inesperado "
            "(esperado: lista de objetos)"
        )

    df = pd.DataFrame(data)

    # Campos mínimos esperados
    required_cols = {"employee_id", "date", "minutes"}
    missing = required_cols - set(df.columns)
    if missing:
        raise RuntimeError(
            "Arquivo nao possui colunas necessarias: "
            + ", ".join(sorted(missing))
        )

    # Tipagem e limpeza
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    df["minutes"] = (
        pd.to_numeric(df["minutes"], errors="coerce").fillna(0).astype(int)
    )
    # garante chaves para agrupamento
    df = df.dropna(subset=["employee_id", "date"])

    return df


def compute_daily_overtime(
    df_shifts: pd.DataFrame, config: OvertimeConfig
) -> pd.DataFrame:
    """Agrupa por funcionario e data, soma minutos trabalhados
    e calcula horas extras diarias.

    Horas extras = max(0, horas_trabalhadas - horas_previstas_dia)
    """
    grouped = (
        df_shifts
        .groupby(["employee_id", "date"], as_index=False)["minutes"].sum()
        .rename(columns={"minutes": "worked_minutes"})
    )

    grouped["worked_hours"] = grouped["worked_minutes"] / 60.0
    grouped["scheduled_hours"] = float(config.scheduled_hours_per_day)

    overtime_hours = (
        (grouped["worked_hours"] - grouped["scheduled_hours"])
        .clip(lower=0)
    )
    grouped["overtime_hours"] = overtime_hours
    grouped["overtime_minutes"] = (
        (grouped["overtime_hours"] * 60).round().astype(int)
    )

    # Ordenação amigável
    grouped = (
        grouped.sort_values(["employee_id", "date"]).reset_index(drop=True)
    )
    return grouped[
        [
            "employee_id",
            "date",
            "worked_minutes",
            "worked_hours",
            "scheduled_hours",
            "overtime_minutes",
            "overtime_hours",
        ]
    ]


def maybe_enrich_with_estimated_times(
    df_daily: pd.DataFrame, estimated_json_path: Optional[Path]
) -> pd.DataFrame:
    """Se existir arquivo de estimated_times, usa os campos previstos por dia
    por funcionario para substituir scheduled_hours.

    Esperado no JSON (ajustar conforme estrutura real): campos
    "employee_id", "date" e "estimated_minutes" (ou similar). Caso nao
    exista, ignora.
    """
    if not estimated_json_path or not estimated_json_path.exists():
        return df_daily

    try:
        with open(estimated_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list) or len(data) == 0:
            return df_daily
        est = pd.DataFrame(data)
        # Tentativas de nomes de campos comuns
        candidate_minutes_cols = [
            "estimated_minutes",
            "expected_minutes",
            "planned_minutes",
            "minutes",
        ]
        minutes_col = next(
            (c for c in candidate_minutes_cols if c in est.columns), None
        )
        if minutes_col is None:
            return df_daily

        if "date" not in est.columns or "employee_id" not in est.columns:
            return df_daily

        est = est[["employee_id", "date", minutes_col]].copy()
        est["date"] = pd.to_datetime(
            est["date"], errors="coerce"
        ).dt.date
        est[minutes_col] = pd.to_numeric(
            est[minutes_col], errors="coerce"
        ).fillna(0)
        est = est.groupby(["employee_id", "date"], as_index=False)[
            minutes_col
        ].sum()
        est.rename(columns={minutes_col: "scheduled_minutes"}, inplace=True)
        est["scheduled_hours"] = est["scheduled_minutes"] / 60.0

        merged = df_daily.merge(
            est[["employee_id", "date", "scheduled_hours"]],
            on=["employee_id", "date"],
            how="left",
            suffixes=("", "_est"),
        )

        # Substituir quando houver valor estimado
        mask = merged["scheduled_hours_est"].notna()
        merged.loc[mask, "scheduled_hours"] = merged.loc[
            mask, "scheduled_hours_est"
        ]
        merged = merged.drop(
            columns=[c for c in merged.columns if c.endswith("_est")]
        )

        # Recalcular overtime com base no novo scheduled_hours
        merged["overtime_hours"] = (
            merged["worked_hours"] - merged["scheduled_hours"]
        ).clip(lower=0)
        merged["overtime_minutes"] = (
            (merged["overtime_hours"] * 60).round().astype(int)
        )
        return merged
    except Exception:
        # Se der problema no parse, mantem como esta
        return df_daily


def save_overtime_report(df: pd.DataFrame, out_dir: Path) -> Path:
    """Salva o DataFrame em CSV com timestamp no diretório indicado."""
    out_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"horas_extras_diarias_{timestamp}.csv"
    df.to_csv(out_path, index=False, encoding="utf-8")
    return out_path


def parse_args(argv: Optional[list] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Calcula horas extras por dia a partir de shifts (presenca)"
        ),
    )

    parser.add_argument(
        "--entrada",
        dest="entrada",
        type=str,
        default=None,
        help=(
            "Caminho do arquivo de entrada (JSON) com shifts. "
            "Se omitido, usa o arquivo mais recente em "
            "'Dados_Coletados/Dados_Brutos/Dados da API/Presenca'."
        ),
    )

    parser.add_argument(
        "--horas-previstas",
        dest="horas_previstas",
        type=float,
        default=8.0,
        help="Horas previstas por dia (padrao: 8.0)",
    )

    parser.add_argument(
        "--saida",
        dest="saida",
        type=str,
        default=None,
        help=(
            "Caminho do CSV de saida. "
            "Se omitido, salva automaticamente em "
            "'Dados_Coletados/Dados_Processados'."
        ),
    )

    return parser.parse_args(argv)


def main(argv: Optional[list] = None) -> int:
    args = parse_args(argv)

    # Determinar arquivo de entrada
    if args.entrada:
        input_path = Path(args.entrada)
    else:
        input_path = find_latest_shifts_file(PRESENCA_DIR)

    if not input_path or not input_path.exists():
        print(
            "Nao encontrei arquivo de shifts. "
            "Garanta que existam arquivos JSON em:"
        )
        print(f"'{PRESENCA_DIR}' contendo 'shifts' no nome.")
        return 1

    print("Arquivo de entrada:", input_path)

    # Configuração de jornada prevista
    config = OvertimeConfig(
        scheduled_hours_per_day=float(args.horas_previstas)
    )
    print(
        f"Jornada prevista/dia: {config.scheduled_hours_per_day}h"
    )

    # Carregar e calcular
    try:
        df_shifts = load_shifts_to_dataframe(input_path)
    except Exception as exc:
        # Erro generico, mantido simples para console
        print(f"Erro ao carregar shifts: {exc}")
        return 1

    if df_shifts.empty:
        print("Nenhum registro de shifts encontrado no arquivo.")
        return 0

    df_overtime = compute_daily_overtime(df_shifts, config)

    # Enriquecer com estimated_times, se existir
    est_path = find_latest_estimated_times(PRESENCA_DIR)
    df_overtime = maybe_enrich_with_estimated_times(df_overtime, est_path)

    # Salvar CSV
    if args.saida:
        out_path = Path(args.saida)
        out_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        out_path = save_overtime_report(df_overtime, PROCESSADOS_DIR)

    if args.saida:
        df_overtime.to_csv(out_path, index=False, encoding="utf-8")

    print(f"Relatorio salvo em: {out_path}")

    # Prévia amigável
    preview = df_overtime.head(10)
    if not preview.empty:
        print("\nPrevia (10 primeiras linhas):")
        print(preview.to_string(index=False))

    # Totais por funcionário (resumo)
    resumo = (
        df_overtime.groupby("employee_id")["overtime_hours"]
        .sum()
        .reset_index()
        .sort_values("overtime_hours", ascending=False)
    )
    if not resumo.empty:
        print("\nTotal de horas extras por funcionario (periodo do arquivo):")
        for _, row in resumo.iterrows():
            print(f"  Emp {row['employee_id']}: {row['overtime_hours']:.2f} h")

    return 0


if __name__ == "__main__":
    sys.exit(main())
