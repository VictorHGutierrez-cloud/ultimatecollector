# Time off — ausências, férias e saldos

**Help Center (pai):** [Time tracking & Absences](https://help.factorialhr.com/en_US/time-tracking-absences)

## Subcategorias principais

| Área | URL | Para que serve |
|------|-----|----------------|
| Absences & approvals | https://help.factorialhr.com/en_US/absences-approvals | Pedir, atribuir, aprovar, calendário, feriados |
| Time off settings | https://help.factorialhr.com/en_US/time-off-settings | Policies, allowances, carryover, tenure |
| Time off deductions | https://help.factorialhr.com/en_US/time-off-deductions | Como as ausências descontam saldo / impacto |

## O que é

Tudo que envolve **pedir e controlar dias/horas fora do trabalho**: férias, doença, licenças, feriados, bloqueios de calendário e **saldos** (allowances).

## Conceitos-chave

| Termo | Explicação simples |
|-------|--------------------|
| Absence type | “Tipo” do pedido (Vacation, Sick leave…) |
| Time off policy | Conjunto de regras atribuído a pessoas |
| Time off allowance | Contador/bolsa (ex.: 20 dias de férias) |
| Fixed balance | Saldo fixo no ciclo |
| Based on time worked | Saldo que acumula conforme tempo trabalhado |
| Approver / approval system | Quem aprova e em que ordem |
| Global approver | Pode aprovar qualquer pedido (atalho de poder) |
| Blocked period | Janela em que não se pode pedir |
| Carryover | O que sobra passa para o próximo ciclo |
| Allowance adjustment | Ajuste manual no saldo de uma pessoa |
| Bank holidays | Feriados públicos |

## Onde clicar

**Colaborador**

1. Sidebar → **Time off** → Add time off  
2. Escolher tipo, datas, anexar documento se a policy exigir  

**Gestor / Admin**

1. **Inbox → Requests** para aprovar  
2. Calendário / perfil do employee → Time off  
3. **Settings → Time → Time off** para policies, allowances, absence types  

## Fluxo típico de setup (demo / cliente)

```text
Criar absence types
  → Criar allowances (regras de saldo)
  → Montar time off policy e atribuir às pessoas
  → Definir approvers / approval system
  → Carregar bank holidays
  → (Opcional) blocked periods, carryover, document upload
  → Testar: request → approve → ver saldo
```

## Dicas para guia de cliente

- Sempre mostre o **saldo antes e depois** de um pedido aprovado.
- Explique: pedido pendente **pode não descontar** até aprovar (depende da configuração).
- Separar história **employee** vs **HR admin** vs **manager**.
- Em sandboxes deste repo (ex. STATIN), amarre o guia aos tipos/policies reais já seedados.

## Artigos âncora

Absences:

- About absences and approvals
- About time off allowances
- How to request and assign time off
- How to create time off approval systems
- How to approve and reject time off requests
- How to set up blocked periods for time off

Settings:

- About time off settings: overview
- How to create and assign time off policies
- How to configure time off allowances
- How Carryover works at the end of the year
- FAQ about Time off settings

Listas completas: `absences-approvals`, `time-off-settings`, `time-off-deductions` em `INDEX.md`.
