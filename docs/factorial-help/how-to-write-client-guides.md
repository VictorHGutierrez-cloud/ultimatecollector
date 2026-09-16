# Como escrever guias / demo scripts para cliente

Use este roteiro sempre que o usuário pedir um **guia**, **demo script**, **setup summary** ou **passo a passo** de produto Factorial para um cliente.

## Passo a passo (para o Cursor)

1. **Identificar o cliente**  
   - Pasta típica: `clients/{id}/`  
   - Ler `profile.json` (sem expor secrets), `catalog.json` se existir, e docs em `*asset/` ou `run_log/`.

2. **Identificar o módulo do produto**  
   - Abrir o arquivo certo em `docs/factorial-help/modules/`.  
   - Confirmar títulos/links em `INDEX.md` ou `catalog.json`.

3. **Separar três camadas no texto**  
   - **Produto (Factorial):** o que a feature faz, nomes oficiais, onde clicar.  
   - **Cliente:** nomes, políticas, IDs, narrativa da demo.  
   - **Operação técnica (API/seed):** só se o usuário pedir; senão manter linguagem de negócio.

4. **Estrutura recomendada do guia**  
   1. Objetivo (1 parágrafo)  
   2. Pré-requisitos (apps, permissões, dados)  
   3. Configuração (admin) — passos numerados  
   4. Experiência do colaborador / gestor  
   5. Roteiro de demo (o que mostrar na tela)  
   6. Checklist de validação  
   7. Links oficiais do Help Center  
   8. (Opcional) troubleshooting

5. **Linguagem**  
   - Português claro, sem jargão de TI desnecessário.  
   - Manter termos oficiais em inglês (`Time off allowance`, `Permission group`) e explicar em PT.  
   - Passos do tipo: “No menu à esquerda, clique em **Settings** → **Time** → **Time off**”.

6. **Não fazer**  
   - Não copiar artigo oficial inteiro.  
   - Não inventar botões: se duvidar, abrir o link do Help Center.  
   - Não colocar tokens/API keys no guia.  
   - Não misturar setup de um cliente com dados de outro.

## Modelo curto (copiar e adaptar)

```markdown
# [Cliente] — Guia de [Módulo]

## Objetivo
...

## Pré-requisitos
- App/feature habilitada
- Grupo de permissões adequado
- Dados de exemplo prontos

## Configuração (Admin)
1. ...
2. ...

## O que o colaborador vê
1. ...

## Roteiro de demo (5–10 min)
1. Abrir ...
2. Mostrar ...
3. Contar a história de ...

## Checklist
- [ ] ...
- [ ] ...

## Artigos oficiais
- [Título](url)
```

## Onde salvar

- Guia do cliente → `clients/{id}/...` (ex.: `*asset/DEMO_SCRIPT_....md`)
- Conhecimento genérico do produto → `docs/factorial-help/` (esta pasta)
