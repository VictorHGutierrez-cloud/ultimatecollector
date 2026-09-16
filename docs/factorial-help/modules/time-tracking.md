# Time tracking — ponto e horas

**Help Center:** [Time tracking](https://help.factorialhr.com/en_US/time-tracking) (~53 artigos)  
**Pai:** [Time tracking & Absences](https://help.factorialhr.com/en_US/time-tracking-absences)

## O que é

Módulo para **bater ponto** (clock in/out), gerir **pausas**, **folhas de horas** (timesheets), **horas extras**, **horas especiais** e **aprovação**. A regra de ouro: quase tudo importante vive numa **Time tracking policy**.

## Conceitos-chave

| Termo | Significado prático |
|-------|---------------------|
| Time tracking policy | Pacote de regras: como bater ponto, tolerância, breaks, overtime, special hours |
| Time tracking systems | Canais: desktop, mobile, QR, Employee ID, etc. |
| Work schedule | Jornada esperada (base do balance / estimated hours) |
| Breaks / break types | Pausas pagas ou não; criadas em Time Categories e ligadas à policy |
| Extra hours / overtime | Acima do previsto; pode ter aprovação e compensação |
| Special hours | Faixas especiais (noite, weekend, holiday) |
| Bank of hours | Banco de horas acumulado |
| Timesheet approval | Trava/valida o período depois da revisão |
| Work location tracking | Home / office / trip no clock-in |
| Geolocation | Coordenadas no clock-in (com aceite de política) |

## Onde clicar (admin)

1. **Settings → Time → Time tracking** (policies)  
2. **Settings → Time → Work schedules**  
3. **Settings → Time → Time Categories** (breaks)  
4. Sidebar → **Time tracking** (visão operacional / aprovação)  
5. Perfil do employee → timesheet

## Fluxo típico de setup

```text
Criar work schedule
  → Criar break types (se precisar)
  → Criar Time tracking policy
  → Ativar sistemas de clock-in
  → Configurar overtime / special hours / approvals
  → Atribuir policy aos employees
  → Testar clock-in + aprovação de timesheet
```

## Dicas para guia / demo

- Mostre **um dia completo**: clock-in → break → clock-out → observação → aprovação do manager.
- Deixe claro a diferença **planned/estimated hours** vs **horas batidas** vs **extra hours**.
- Se o cliente usa turnos, combine com o módulo [shift-management.md](shift-management.md).
- Face Recognition: artigo oficial diz que a feature foi descontinuada em alguns mercados — confirme no artigo antes de prometer.

## Artigos âncora

- About time tracking policies
- About time tracking systems
- About breaks
- How to review and approve timesheets
- How to create and assign work schedules
- Extra time compensation / Special hours
- FAQ about Time tracking

Lista completa: `time-tracking` em `INDEX.md`.
