# Fonte do conteúdo

## Origem oficial

- Help Center (EN): https://help.factorialhr.com/en_US
- Plataforma do knowledge base: Helpjuice (feeds Atom por categoria)

## Como o índice é montado

1. Lê a homepage e descobre as **categorias de topo**.
2. Em cada categoria-pai, encontra **subcategorias** (links “see more”).
3. Para cada categoria-folha, baixa o feed Atom:
   - `https://factorial.helpjuice.com/en_US/{slug}.atom`
4. Grava título, URL pública, slug e snippet curto em:
   - `catalog.json`
   - `INDEX.md`

Os arquivos em `modules/` são **resumos escritos por nós** (não são cópia literal dos artigos).

## Atualizar

```text
python scripts/refresh_factorial_help_index.py
```

Rode isso quando:

- a Factorial publicar muitos artigos novos;
- um link do INDEX estiver quebrado;
- você quiser conferir o que mudou no Help Center.

## Política de uso

- Preferir sempre o **link oficial** ao citar um passo detalhado.
- Se o resumo local e o artigo ao vivo divergirem, **o artigo oficial vence**.
- Não versionar HTML bruto de debug na pasta (apague `_debug_*` se aparecer).
