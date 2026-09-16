# Roteiro de demo — SIJ Vacation Leave (≈ 5–7 min)

**Cliente:** Statistical Institute of Jamaica (sandbox Factorial)  
**Objetivo:** Mostrar que as regras do PDF de férias foram traduzidas para Time Off na Factorial.

---

## Antes de começar (1 minuto)

1. Abra o Factorial no **tenant do statistic-institute**.
2. Tenha o PDF aberto ao lado (opcional):  
   `clients/statistic-institute/statistic-instituteasset/Statistical Institute of Jamaica Vacation Leave Requirements (1).docx`
3. Memorize estes 4 exemplos (um por faixa):

| Pessoa | Faixa | Dias/ano | Saldo demo |
|--------|-------|----------|------------|
| **Hellen Howard** | Base | 15 | ~9 dias (1º ano prorata) |
| **Charles Carter** | Intermediário | 20 | ~20 dias (ano cheio) |
| **Daisy Dawson** | 15–25 anos | 21 | ~40 dias (acúmulo) |
| **Laura Lewis** | Sênior | 25 | ~50 dias (acúmulo) |

---

## Passo 1 — Contexto (30 segundos)

**O que fazer:** Fale, sem clicar ainda.

**O que dizer:**
> “Recebemos o documento de Vacation Leave do Statistical Institute of Jamaica.  
> Configuramos na Factorial: 15, 20, 21 e 25 dias úteis por ano, com teto de 3 anos, prorata e feriados que não descontam do saldo.”

---

## Passo 2 — Políticas de Time Off (1–2 min)

**O que clicar:**
1. Menu → **Time Off** (ou **Absences** / **Ausências**, conforme o idioma da conta)
2. Entre em **Policies** / **Políticas**
3. Abra, uma a uma (ou mostre a lista):
   - **SIJ Vacation 15 days**
   - **SIJ Vacation 20 days**
   - **SIJ Vacation 21 days (15-25y)**
   - **SIJ Vacation 25 days**

**O que dizer (em cada policy):**
> “Cada política tem um allowance:  
> 15 → teto 45 · 20 → 60 · 21 → 63 · 25 → 75.  
> Isso espelha a regra de acumular no máximo 3 anos.”

**Detalhes técnicos para apontar se perguntarem:**
- Dias **úteis** (seg–sex)
- Feriados **não** contam como workable
- Prorata ligado
- Carry-over até 36 meses

---

## Passo 3 — Tipos de ausência (1 min)

**O que clicar:**
1. Ainda em Time Off → **Leave types** / **Tipos de ausência**
2. Mostre **SIJ Vacation Leave**
3. (Opcional) Mostre também: Sick, Maternity, Study, Compassionate, Special

**O que dizer:**
> “Vacation Leave é o tipo principal, com aprovação.  
> Os outros tipos existem porque o documento diz que leave of absence longo (Sick, Maternity, etc.) pode pausar o accrual — na demo explicamos a regra; a Factorial não pausa sozinha após 14 dias.”

---

## Passo 4 — Colaborador com saldo (2 min) — o momento forte

### 4a. Hellen Howard (15 dias / prorata)

**O que clicar:**
1. **Employees** / **Colaboradores** → busque **Hellen Howard**
2. Abra o perfil → aba **Time Off** / **Ausências**
3. Mostre a policy **SIJ Vacation 15 days** e o saldo (~9)

**O que dizer:**
> “Hellen está na faixa de 15 dias.  
> O saldo de ~9 dias é o exemplo do documento: primeiro ano incompleto, com arredondamento.”

### 4b. Charles Carter (20 dias)

**O que clicar:** Mesmo caminho → **Charles Carter**

**O que dizer:**
> “Charles tem entitlement cheio de 20 dias — ano completo na faixa intermediária.”

### 4c. Daisy Dawson ou Laura Lewis (acúmulo)

**O que clicar:** **Daisy Dawson** (21 / ~40) ou **Laura Lewis** (25 / ~50)

**O que dizer:**
> “Aqui vemos o acúmulo multi-ano, ainda abaixo do teto de 3 anos (63 ou 75).  
> Quando chega no máximo, a empresa para de acumular até o saldo baixar — regra do documento.”

---

## Passo 5 — Pedido de férias já criado (1 min)

**O que clicar:**
1. Em qualquer um deles, ou na visão de **Time Off → Leaves / Requests**
2. Mostre uma destas absences aprovadas:

| Quem | Datas | Descrição |
|------|-------|-----------|
| Hellen Howard | 14–18 set 2026 | family holiday |
| Charles Carter | 28–30 set 2026 | short break |
| Daisy Dawson | 12–21 out 2026 | extended leave |

**O que dizer:**
> “Já existem pedidos de SIJ Vacation Leave aprovados.  
> A contagem é em dias úteis: fins de semana e feriados públicos não entram no desconto.”

---

## Passo 6 — Fechamento (30 segundos)

**O que dizer:**
> “Resumo: o PDF virou configuração real — 4 faixas, tetos de 3 anos, dias úteis, prorata e exemplos vivos nos colaboradores.  
> Duas regras ficam como processo/manual na Factorial: pausa de accrual após 14 dias de leave of absence, e credit de recall se a pessoa for chamada de volta.”

---

## Se perguntarem “e se…”

| Pergunta | Resposta curta |
|----------|----------------|
| E quem tem 15–25 anos de casa? | Policy **21 days** (Daisy) |
| E o teto de 3 anos? | 15→45, 20→60, 21→63, 25→75 no allowance |
| Feriado no meio das férias? | Não desconta — `working days` + holiday not workable |
| Recall? | Devolve os dias não usados (ajuste manual / incidence) |
| Pausa após 14 dias off? | Regra de negócio; leave types SIJ existem para a conversa |

---

## Checklist rápido (imprimir / colar no Notion)

- [ ] Login no tenant SIJ  
- [ ] Mostrar 4 policies SIJ Vacation  
- [ ] Mostrar leave type SIJ Vacation Leave  
- [ ] Abrir Hellen (15 / ~9)  
- [ ] Abrir Charles (20 / ~20)  
- [ ] Abrir Daisy ou Laura (acúmulo)  
- [ ] Mostrar 1 leave aprovado  
- [ ] Fechar com 2 limitações honestas (14 dias + recall)
