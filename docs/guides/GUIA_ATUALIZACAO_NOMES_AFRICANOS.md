# Guia de Atualização de Nomes Africanos

## 📋 Descrição

Este script atualiza automaticamente os nomes dos colaboradores que **não têm nomes africanos**, gerando nomes africanos apropriados baseados no **gênero** de cada pessoa e fazendo **push na API Factorial**.

## 🎯 Funcionalidades

- ✅ Identifica colaboradores sem nomes africanos
- ✅ Gera nomes africanos baseados no gênero (masculino/feminino)
- ✅ Respeita o gênero de cada colaborador
- ✅ Faz push na API Factorial automaticamente
- ✅ Modo TESTE para verificar antes de atualizar
- ✅ Log completo de todas as atualizações

## 📝 Como Usar

### 1. Modo TESTE (Recomendado primeiro)

Execute em modo teste para ver o que será feito **sem atualizar na API**:

```bash
python atualizar_nomes_africanos.py --teste --sim
```

Isso vai:
- Mostrar preview dos novos nomes
- Processar todos os colaboradores
- **NÃO atualizar na API** (apenas simular)
- Gerar um log JSON com todas as mudanças

### 2. Modo REAL (Atualiza na API)

Depois de verificar no modo teste, execute em modo real:

```bash
python atualizar_nomes_africanos.py --sim
```

**⚠️ ATENÇÃO:** Isso vai **realmente atualizar** os nomes na API Factorial!

### 3. Modo Interativo

Se quiser escolher manualmente:

```bash
python atualizar_nomes_africanos.py
```

O script vai perguntar:
1. Modo TESTE (não atualiza na API)
2. Modo REAL (atualiza na API)
3. Cancelar

## 📊 O que o Script Faz

1. **Lê o arquivo CSV** com os colaboradores
2. **Identifica** quem não tem nome africano
3. **Filtra** apenas colaboradores ativos
4. **Gera nomes africanos** baseados no gênero:
   - **Feminino**: Amina, Fatou, Nia, Zola, Adanna, etc.
   - **Masculino**: Kwame, Taye, Ayo, Chike, Mandla, etc.
5. **Mostra preview** dos novos nomes
6. **Atualiza na API** (se não estiver em modo teste)
7. **Gera log** em `atualizacoes_nomes_africanos.json`

## 📁 Arquivos Gerados

- `atualizacoes_nomes_africanos.json` - Log completo de todas as atualizações com:
  - ID do colaborador
  - Nome antigo
  - Nome novo
  - Gênero

## 🔧 Requisitos

- Python 3.x
- Arquivo `config_unificado.env` configurado com:
  - `BASE_URL` - URL da API Factorial
  - `API_KEY` - Chave da API
  - `AUTH_TYPE` - Tipo de autenticação (x-api-key)

## ⚙️ Configuração da API

O script usa as configurações do arquivo `config_unificado.env`:

```env
BASE_URL=https://api.eu2.demo.factorial.dev
API_KEY=sua_chave_aqui
AUTH_TYPE=x-api-key
API_VERSION=2026-01-01
```

## 📋 Exemplo de Saída

```
================================================================================
PREVIEW - NOVOS NOMES AFRICANOS:
================================================================================
  ID 1785128  | Maria Lopez                    -> Ifeoma Nkosi (female)
  ID 1784609  | Samuel Sánchez                 -> Sekou Lumumba (male)
  ID 1784598  | Susana Stanley                 -> Patience Kabila (female)
  ...
```

## ⚠️ Importante

- O script **só atualiza colaboradores ATIVOS**
- Nomes africanos são gerados **aleatoriamente** mas respeitando o gênero
- Cada execução pode gerar nomes diferentes
- O log JSON salva todas as mudanças para referência

## 🐛 Troubleshooting

### Erro de conexão com API
- Verifique se `config_unificado.env` está configurado corretamente
- Teste a conexão com: `python -c "from core.api_client import APIClient; APIClient().test_connection()"`

### Arquivo CSV não encontrado
- Verifique se o arquivo está em: `data/raw/employees/employees_20260202_175128.csv`
- Ou ajuste o caminho no script

### Erro de autenticação
- Verifique se a `API_KEY` está correta e válida
- Verifique se o `AUTH_TYPE` está configurado como `x-api-key`

## 📞 Suporte

Se tiver problemas, verifique:
1. Logs em `logs/api.log`
2. Arquivo `atualizacoes_nomes_africanos.json` para ver o que foi processado
3. Mensagens de erro no terminal
