# Demo LIAT AIR — Factorial (Antigua & Barbuda)

Personaliza a demo Factorial da **LIAT AIR / Liat (2020) Limited** (company `195679`, API `2026-07-01`).

Foco: **Performance Management** com Balanced Scorecard (BSC) + 9-Box, conforme o framework HRIS da LIAT.

## O que o seed prepara via API

- Legal entity: `Liat (2020) Limited` (Antigua / USD)
- Location: `LIAT VC Bird International Airport` — St. John's
- 6 times: Executive, Flight Ops, Ground/MRO, Commercial, Finance, People & Culture
- Cast de 12 pessoas (nomes caribenhos), managers e memberships
- Processos de performance:
  - `LIAT Q1 Goal Setting & BSC Planning 2026` (ativo)
  - `LIAT Q2-Q3 Mid-Year Review 2026` (ativo, com peer/360°)
  - `LIAT Q4 Year-End & 9-Box Review 2026` (draft, com potencial)
- Questionários: BSC Objectives (70%), Competencies (30%), 360° Feedback, Coaching & IDP
- Escala DNM / PMS / MET / EXC / SIG
- 4 treinamentos BSC / 9-box / coaching / safety
- 2 posts em Company announcements
- Metas SMART em `run_log/goals_pack.md`

**Fora do escopo desta demo:** Staff Travel, Leave, Payroll, ATS, Time tracking.

## Passo a passo

### 1) Credenciais

A API key fica em `clients/liat-air/secrets/seutoken.txt` (não commitar).

Ou configure em `clients/liat-air/secrets/secrets.env`:

```
BASE_URL=https://api.eu2.demo.factorial.dev
API_KEY=sua_chave_aqui
API_VERSION=2026-07-01
AUTH_TYPE=x-api-key
COMPANY_ID=195679
```

### 2) Inventário

```bash
python scripts/clients/liat-air/liat_inventory.py
```

### 3) Seed (simulação)

```bash
python scripts/clients/liat-air/liat_seed_performance.py --dry-run
```

### 4) Seed (aplicar na Factorial)

```bash
python scripts/clients/liat-air/liat_seed_performance.py --apply
```

### 5) Verificar

```bash
python scripts/clients/liat-air/liat_verify_performance.py
```

### 6) Checklist manual no painel Factorial

1. Configurar pesos **70% objetivos / 30% competências**
2. Ativar **9-box** no processo Q4 Year-End
3. Configurar **peer evaluator groups** (360°)
4. Ligar metas individuais a **parent goals** (cascata BSC)
5. Ativar **e-signature** nos appraisals
6. Iniciar agreements no UI se a API retornar 403

## Documento de referência (para a LIAT usar no dia a dia)

**Guia operacional de AVDs (SOW):**  
`liat-airasset/LIAT Factorial AVD Operating Guide.pdf`  
(fonte Markdown: `FACTORIAL_AVD_SOW_LIAT.md`)

Como gerar de novo:

```bash
python scripts/clients/liat-air/build_avd_sow_pdf.py
python scripts/clients/liat-air/liat_upload_documents.py --apply
```

Isso sobe o PDF do **guia de uso da Factorial** (não o framework de vendor da LIAT).

O PDF de requisitos do cliente continua em:  
`liat-airasset/LIAT HRIS Vendor Framework.pdf` — BSC, 9-box, 70/30 (referência interna).

## Cascata de metas (UI)

A API não cria parent/sub-goals. Na demo use os **Assign to** corretos:

**Whole company** → **Team (LIAT Flight Operations)** → **Employees (Tamara Joseph)**

Abra **[Corporate BSC / Customer] Network OTP and Safety 2026 (WCTE)** → **Sub-goals** → meta do time → sub-meta individual.
