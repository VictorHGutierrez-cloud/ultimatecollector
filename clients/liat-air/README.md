# Demo LIAT AIR — Factorial (Antigua & Barbuda)

Personaliza a demo Factorial da **LIAT AIR / Liat (2020) Limited** (company `191947`, API `2026-07-01`).

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
COMPANY_ID=191947
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

## Documento de referência

`liat-airasset/LIAT HRIS Vendor Framework.pdf` — requisitos BSC, 9-box, 70/30 weighting.
