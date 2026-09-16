# Factorial Help Pack (caderno de consulta)

Pasta local com o mapa do [Factorial Help Center](https://help.factorialhr.com/en_US) para o Cursor te ajudar a **entender o produto** e a **escrever guias para clientes**.

## O que tem aqui (em linguagem simples)

| Arquivo / pasta | Para que serve |
|-----------------|----------------|
| [INDEX.md](INDEX.md) | Lista de **todas** as categorias e artigos oficiais (título + link) |
| [catalog.json](catalog.json) | O mesmo índice em JSON (fácil para scripts e para o Cursor) |
| [glossary.md](glossary.md) | Termos Factorial em inglês ↔ português |
| [modules/](modules/) | Resumos por área do produto (o que é, onde clicar, o que mostrar na demo) |
| [how-to-write-client-guides.md](how-to-write-client-guides.md) | Como montar um guia / demo script para cliente |
| [SOURCE.md](SOURCE.md) | De onde veio o conteúdo e como atualizar |

**Importante:** não copiamos os artigos da Factorial palavra por palavra. Guardamos o **mapa + resumos nossos + links oficiais**. Quando precisar do detalhe atualizado, abra o link do artigo.

## Como você usa (passo a passo)

### 1) Perguntar sobre o produto

1. Abra um chat neste projeto no Cursor.
2. Pergunte em português, por exemplo:
   - “Como funciona *time off allowance*?”
   - “O que é Job Catalog na Factorial?”
   - “Diferença entre Performance review e Goals”
3. O Cursor deve consultar esta pasta, explicar em linguagem simples e apontar o artigo oficial.

### 2) Pedir um guia para cliente

1. Digite algo como: “Escreve um guia de Time Off para o STATIN” ou “Monta um demo script de Performance”.
2. Se o cliente já tiver pasta em `clients/...`, diga o nome do cliente.
3. O Cursor usa os módulos desta pasta + os arquivos do cliente (sem misturar secrets).

### 3) Atualizar a lista de artigos (quando a Factorial mudar o site)

1. Abra o terminal na raiz do projeto.
2. Rode:

```text
python scripts/refresh_factorial_help_index.py
```

3. Isso atualiza só `catalog.json` e `INDEX.md`.
4. Se quiser atualizar os textos dos módulos, peça no chat: “Atualiza os resumos em docs/factorial-help/modules”.

## Mapa rápido dos módulos

| Módulo | Arquivo | Prioridade neste projeto |
|--------|---------|-------------------------|
| Primeiros passos | [modules/getting-started.md](modules/getting-started.md) | Alta |
| ONE (assistente) | [modules/one.md](modules/one.md) | Média |
| Time tracking | [modules/time-tracking.md](modules/time-tracking.md) | Alta |
| Time off / Absences | [modules/time-off.md](modules/time-off.md) | Alta |
| Shift management | [modules/shift-management.md](modules/shift-management.md) | Média |
| Organization / Job catalog | [modules/organization-job-catalog.md](modules/organization-job-catalog.md) | Alta |
| Permissions & workflows | [modules/permissions-workflows.md](modules/permissions-workflows.md) | Alta |
| Performance | [modules/performance.md](modules/performance.md) | Alta |
| Competencies & goals | [modules/competencies-goals.md](modules/competencies-goals.md) | Alta |
| Surveys & eNPS | [modules/surveys-enps.md](modules/surveys-enps.md) | Média |
| Training | [modules/training.md](modules/training.md) | Alta |
| Apps / API / Integrations | [modules/apps-integrations-api.md](modules/apps-integrations-api.md) | Alta |
| Projects | [modules/projects.md](modules/projects.md) | Curta |
| Compensation & benefits | [modules/compensation-benefits.md](modules/compensation-benefits.md) | Curta |
| Finance | [modules/finance.md](modules/finance.md) | Curta |
| Documents & e-signature | [modules/documents.md](modules/documents.md) | Curta |
| Recruitment / ATS | [modules/recruitment-ats.md](modules/recruitment-ats.md) | Curta |
| IT Management | [modules/it-management.md](modules/it-management.md) | Curta |
| Notifications | [modules/notifications.md](modules/notifications.md) | Curta |
| Ticketing & policies | [modules/ticketing-policies.md](modules/ticketing-policies.md) | Curta |
| Billing | [modules/billing.md](modules/billing.md) | Curta |
| Contact Support | [modules/support.md](modules/support.md) | Curta |

## O que NÃO fica aqui

- Tokens, senhas, `profile.json` com secrets
- Texto longo copiado dos artigos oficiais
- Documentos internos do cliente (continuam em `clients/{cliente}/...`)

## Termos rápidos

- **Help Center** = site de ajuda oficial da Factorial
- **Categoria** = pasta de assunto (ex.: Time tracking)
- **Artigo** = página de ajuda com um título e um link
- **Módulo (neste pack)** = nosso resumo em português de uma área do produto
