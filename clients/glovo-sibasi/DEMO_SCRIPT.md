# DEMO SCRIPT — Kibanda (Brenda) · Front-facing

**Sandbox:** company `191232` (perfil `glovo-sibasi`)  
**Duração:** ~10–12 minutos  
**Foco:** Directory, Locations, Teams, Announcements (+ capas), Documents  
**Fora desta wave:** shifts, payroll, ATS, performance

Story pack: `glovo-sibasiasset/Kibanda_Factorial_Brendas_Story.pdf`

---

## Antes da demo (2 minutos)

1. Abra Factorial no sandbox Kibanda.
2. Confirme People: **Brenda Wanjiru** no topo.
3. Abra **Company announcements** — 5 posts Kibanda **já com capa** (multipart `cover_image` no seed).
4. Abra **Documents** e confira os 3 PDFs Kibanda.

---

## Click-path (frente visual)

### 1) Org / Locations (~2 min)

- Abra **Locations**.
- Mostre as 4 branches + HQ:
  - Kibanda CBD
  - Kibanda Westlands
  - Kibanda Kilimani Branch
  - Kibanda Karen
  - Kibanda Kilimani — Head Office
- Frase: *“Quatro restaurantes em Nairobi + head office acima do Kilimani.”*

### 2) People / Directory (~3 min)

- Abra **Employees / People**.
- Destaque:
  - **Brenda Wanjiru** — Founder & MD
  - **Esther Nyambura** — HR & Admin
  - Branch managers: **Faith** (CBD), **Grace** (Westlands), **Daniel** (Kilimani), **Peter** (Karen)
  - Staff da story: Tom Sang, Brian Wekesa, Mary Odhiambo, Paul Kipchumba…
- Frase: *“Em 10 segundos o cliente sente East Africa — não um sandbox genérico.”*

### 3) Teams (~1 min)

- Abra **Teams**.
- Mostre Head Office + um time por branch, com o manager como lead.

### 4) Announcements (~3 min)

- Abra **Company announcements**.
- Percorra os 5 posts (já com capa).
- Conte a história em ordem:
  1. Welcome / um só lugar para as pessoas
  2. Rotas no app (fim do WhatsApp)
  3. Mashujaa Day double pay
  4. Hiring December
  5. Minimum wage check May 2026
- Frase: *“Isto é o que Brenda vê no domingo à noite em vez de quatro grupos de WhatsApp.”*

### 5) Documents (~2 min)

- Abra **Documents** (company).
- Mostre:
  - `Kibanda_Employee_Handbook_Demo.pdf`
  - `Kibanda_Onboarding_Checklist_Tom_Sang.pdf`
  - `Kibanda_Employment_Contract_Sample_Brian_Wafula.pdf`
- Frase: *“No caminho completo do PDF, Esther manda o contrato por e-signature; aqui já deixamos o sample visível.”*

### 6) Fecho verbal (~1 min)

- “Depois vêm shifts, leave Kenya, pre-payroll e recruitment — está no story PDF completo.”
- Não abra performance nesta wave.

---

## Como re-seedar (se precisar)

```bash
python scripts/clients/glovo-sibasi/kibanda_inventory.py
python scripts/clients/glovo-sibasi/kibanda_seed_front.py --dry-run
python scripts/clients/glovo-sibasi/kibanda_seed_front.py --apply
python scripts/clients/glovo-sibasi/build_kibanda_demo_pdfs.py
python scripts/clients/glovo-sibasi/kibanda_upload_documents.py --apply
```

---

## Termos rápidos

| Termo | Significado |
|-------|-------------|
| Sandbox | Conta de teste Factorial |
| Cast | Pessoas renomeadas para a história |
| Announcement / Post | Aviso interno da empresa |
| Cover | Imagem de capa do post (subida no seed via multipart) |
| Seed | Script que grava a receita na conta |
