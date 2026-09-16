# Demo SZV — Factorial (Sint Maarten)

Personaliza a demo Factorial da **SZV Social & Health Insurances** (company `167952`, API `2026-07-01`).

Referência da empresa: [https://www.szv.sx/](https://www.szv.sx/)

## O que já foi preparado por API

- Legal entity: `SZV Social & Health Insurances` (Sint Maarten / USD)
- Location: `SZV Philipsburg Office` — Harbour View Building, Sparrow Road #4
- 5 times: People & Culture, Customer Care, Medical Insurance Ops, Finance & Levy, Leadership
- Cast de 9 pessoas com nomes locais (Sint Maarten), managers e memberships
- Processos de performance:
  - `SZV P1 Planning Cycle 2026` (ativo)
  - `SZV P2 Mid-Year Cycle 2026` (ativo)
  - `SZV P3 Year-End Review 2026` (draft, com potencial/9-box na criação)
- Questionários: Objetivos, Core Values, Competências, Coaching
- Escala NM / MS / ME / EE / SE
- Treinamentos: Coaching Essentials + Core Values
- 4 job postings ATS (Customer Care, Control Doctor, HR, Finance)
- 3 candidatos com applications nas vagas abertas
- Checklist de **onboarding** (13 tasks) para new hire **Keisha Peterson** (pré-boarding → 1ª semana → 30/60/90 / probation)
- 2 posts em Company announcements (Performance Cycle + Core Values / welcome)
- Metas SMART em `run_log/goals_pack.md`

**Não personalizado (de propósito):** time tracking / attendance / clock-in / shifts.

**Nota sobre onboarding:** a API pública não cria o workflow nativo de Onboarding da Factorial. Simulamos com **Tasks** nomeadas `SZV Onboarding: ...` (donos P&C, Manager, ICT/Facilities, Payroll).

## Cast da demo

| Grupo | Pessoa | Cargo | Manager |
|-------|--------|-------|---------|
| Staff | Keisha Peterson | Customer Care Specialist | Ricardo Vlaun |
| Staff | Marlon Williams | HR Coordinator | Nadia Lejuez |
| Staff | Tanya Carty | Medical Claims Officer | Fiona Halley |
| Manager | Jamal Voges | Finance & Levy Manager | Carlos Richardson |
| Manager | Ricardo Vlaun | Customer Care Manager | Carlos Richardson |
| Manager | Nadia Lejuez | People Manager | Margarita De Weever |
| Manager | Fiona Halley | Medical Operations Manager | Carlos Richardson |
| Leadership | Margarita De Weever | Chief People Officer | Carlos Richardson |
| Leadership | Carlos Richardson | Head of Operations | (topo) |

## Passo a passo (simples)

### 1) Credenciais

No arquivo `config_unificado.env` (ou `config/.env`):

- `BASE_URL=https://api.eu2.demo.factorial.dev`
- `API_KEY=` (chave **SZV Social & Health Insurances**)
- `API_VERSION=2026-07-01`
- `AUTH_TYPE=x-api-key`
- `COMPANY_ID=167952`

### 2) Inventário

No terminal, na pasta do projeto:

```bash
python scripts/szv_inventory.py
```

### 3) Seed

Simulação (não grava):

```bash
python scripts/szv_seed_performance.py --dry-run
```

Gravar na Factorial:

```bash
python scripts/szv_seed_performance.py --apply
```

### 4) Verificar

```bash
python scripts/szv_verify_performance.py
```

### 5) Checklist no painel Factorial (manual)

1. **Employees** — nomes Sint Maarten e organograma
2. **Locations** — SZV Philipsburg Office
3. **ATS / Jobs** — 4 vagas SZV + candidatos (Ashley, Desmond, Soraya)
4. **Tasks** — filtrar por `SZV Onboarding` (checklist da Keisha)
5. **Posts / Announcements** — 2 comunicados SZV
6. **Performance** — processos P1 / P2 / P3
7. Questionários com Core Values e Competencies
8. Escala NM–SE visível
9. Pesos (UI): Staff 50/30/20, Managers 40/35/25, Leadership 40/40/20
10. Iniciar agreements / action plans no UI se necessário
11. Colar 1–2 metas de `run_log/goals_pack.md` (ex.: Keisha + Ricardo)
12. Validar 9-box no P3 após iniciar o processo

## Arquivos importantes

| Arquivo | Função |
|---------|--------|
| `demo_szv/catalog.json` | Conteúdo SZV (cast, valores, metas, vagas, localização) |
| `scripts/szv_inventory.py` | Inventário da conta |
| `scripts/szv_seed_performance.py` | Seed dry-run/apply |
| `scripts/szv_verify_performance.py` | Verificação |
| `demo_szv/DEMO_SCRIPT.md` | Roteiro de apresentação |
| `demo_szv/inventory_report.md` | Último inventário |
| `demo_szv/run_log/` | Logs e IDs criados |

## O que NÃO foi seedado por API

- Time tracking / attendance
- App mobile
- Service desk completo com SLA
- Cascata org→dept→individual 100% nativa (simulamos via times + metas alinhadas)
- Preenchimento completo de respostas de avaliação
- Iniciação confiável de agreements (fazer no UI)
