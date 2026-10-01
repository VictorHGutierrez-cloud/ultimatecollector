# Demo CDH Malawi — Factorial (Investment Bank)

Personaliza a demo Factorial da **CDH Investment Bank Ltd** (company `188450`, API `2026-07-01`).

Foco: **Full Balanced Scorecard (BSC)** com 4 perspectivas + valores, baseado no Excel do cliente (`N MEDI - SCORECARD`).

## Termos simples (o que criamos agora)

| Termo | O que é | Onde está |
|-------|---------|-----------|
| **catalog.json** | A “receita” da demo: quem são as pessoas, times, metas, processos BSC | `clients/cdh-malawi/catalog.json` |
| **Inventário** | Foto do que **já existe** na conta Factorial hoje | `inventory_report.md` + `run_log/inventory.json` |
| **Seed** | Passo seguinte: **aplicar** a receita na conta (ainda não fizemos) | scripts (próxima fase) |
| **Dry-run** | Simular o seed **sem gravar** | — |
| **Apply** | Gravar de verdade na Factorial | — |

## Decisões alinhadas

- Modelo: **Full BSC** (Financial 30% + Customer 15% + Internal 25% + Learning & Growth 30%)
- Ano: **2026**
- Peso final: **90% objectives / 10% core values** (Integrity, Respect & Trust, Teamwork, Equity, Innovation)
- Personagem estrela: **Nqabile Medi** (Administration Manager, HCD) — scorecard do Excel
- Appraiser: **Chisomo Banda** (Chief Human Capital Development Officer)

## Passo a passo

### 1) Credenciais

A API key fica em `clients/cdh-malawi/secrets/seutoken.txt` (não commitar).

### 2) Inventário (já pode rodar)

```bash
python scripts/clients/cdh-malawi/cdh_inventory.py
```

Abra depois: `clients/cdh-malawi/inventory_report.md`

### 3) Seed (simulação — não grava)

```bash
python scripts/clients/cdh-malawi/cdh_seed_performance.py --dry-run
```

### 4) Seed (aplicar na Factorial)

```bash
python scripts/clients/cdh-malawi/cdh_seed_performance.py --apply
```

### 5) Verificar

```bash
python scripts/clients/cdh-malawi/cdh_verify_performance.py
```

Metas prontas para a demo: `clients/cdh-malawi/run_log/goals_pack.md`

## O que o catalog planeja (ainda não está na conta)

- Legal entity: CDH Investment Bank Ltd (Lilongwe)
- Location: CDH House — Lilongwe Head Office
- 6 times CDH (Executive, HCD, Finance, Operations, Commercial, Risk & Compliance)
- Cast de 10 pessoas (nomes malawianos), com rename a partir dos employees atuais
- 4 processos: Q1 Goal Setting, Q2 Progress, Q3 Progress, Q4 Year-End Appraisal
- Escala: Needs Help / Caution / On Target / Exceeded / Significantly Exceeded
- Trainings + announcements do ciclo BSC

## Fora do escopo (por enquanto)

Payroll, Time tracking, ATS completo, 9-box (não aparece no Excel do cliente).
