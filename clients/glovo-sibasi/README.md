# Demo Kibanda (Brenda) — Factorial East Africa

Personaliza o sandbox Factorial **company `191232`** (perfil local `glovo-sibasi`) com a história **Kibanda × Factorial — Brenda's story**.

Foco desta wave: **frente visual** (Directory, Locations, Teams, Announcements, Documents). Sem ciclo de avaliação de desempenho.

## Termos simples

| Termo | O que é | Onde está |
|-------|---------|-----------|
| **catalog.json** | Receita da demo: pessoas, branches, posts | `clients/glovo-sibasi/catalog.json` |
| **Inventário** | Foto do que já existe na conta hoje | `inventory_report.md` + `run_log/inventory.json` |
| **Seed** | Grava a receita na Factorial | `scripts/clients/glovo-sibasi/kibanda_seed_front.py` |
| **Dry-run** | Simula sem gravar | `--dry-run` |
| **Apply** | Grava de verdade | `--apply` |
| **Front-facing** | O que se vê em 10 segundos | People, Locations, Announcements, Documents |

## História (resumo)

- Empresa fictícia: **Kibanda** — 4 restaurantes em Nairobi + head office
- Protagonista: **Brenda Wanjiru**
- Branches: CBD (Faith), Westlands (Grace), Kilimani (Daniel), Karen (Peter)
- Story pack: `glovo-sibasiasset/Kibanda_Factorial_Brendas_Story.pdf`
- Workbook Excel do PDF: **ignorado de propósito** nesta demo

## Passo a passo

### 1) Credenciais

API key em `clients/glovo-sibasi/secrets/seutoken.txt` (não commitar).

### 2) Inventário

```bash
python scripts/clients/glovo-sibasi/kibanda_inventory.py
```

Abra: `clients/glovo-sibasi/inventory_report.md`

### 3) Seed (simulação)

```bash
python scripts/clients/glovo-sibasi/kibanda_seed_front.py --dry-run
```

### 4) Seed (aplicar)

```bash
python scripts/clients/glovo-sibasi/kibanda_seed_front.py --apply
```

### 5) Documentos (PDFs demo)

```bash
python scripts/clients/glovo-sibasi/kibanda_upload_documents.py --apply
```

### 6) Roteiro

Abra `DEMO_SCRIPT.md` (~10–12 min, frente visual).

## O que esta wave prepara

- Legal entity Kibanda (Kenya / KES)
- 4 locations (branches) + HQ Kilimani
- Times por branch + Head Office
- Cast Kenyan (Brenda + managers + staff da story)
- 5 announcements com capa (API multipart `cover_image`; arquivos em `glovo-sibasiasset/announcements/`)
- PDFs demo: handbook, onboarding Tom, contract sample

## Fora do escopo (agora)

Performance/goals, shifts/rotas, payroll Kenya, ATS completo, workbook Excel.
