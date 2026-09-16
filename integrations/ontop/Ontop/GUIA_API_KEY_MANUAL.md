# Guia: Gerar API Key Manualmente no Factorial

## Para Uso Interno - Opção Mais Simples

Segundo a documentação do Factorial, para uso interno você pode **gerar a API Key manualmente no frontend** sem precisar do OAuth2 completo.

## Passos

### 1. Acesse o Frontend do Factorial

1. Faça login como **ADMINISTRADOR** no Factorial
2. Acesse: `https://app.eu2.demo.factorial.dev` (ou sua URL de produção)

### 2. Navegue até as Configurações de API

1. Vá em **Settings** (Configurações)
2. Procure por **API** ou **API Keys**
3. Ou vá diretamente em: **Settings > Integrations > API**

### 3. Gere uma Nova API Key

1. Clique em **"Generate API Key"** ou **"Create API Key"**
2. Dê um nome para a API Key (ex: "Coletor RH - Uso Interno")
3. Selecione as permissões necessárias (scopes)
4. Clique em **"Generate"** ou **"Create"**

### 4. Copie a API Key

1. **IMPORTANTE**: A API Key será mostrada apenas uma vez!
2. Copie a API Key completa
3. Guarde em local seguro

### 5. Configure no Projeto

Adicione ao `config_unificado.env`:

```env
# API Key gerada manualmente
FACTORIAL_API_KEY=sua_api_key_aqui
FACTORIAL_AUTH_TYPE=x-api-key
BASE_URL=https://api.eu2.demo.factorial.dev
API_VERSION=2026-01-01
```

### 6. Teste

```bash
cd Ontop
python test_factorial_connection.py
```

## Vantagens da API Key Manual

- ✅ Mais simples para uso interno
- ✅ Não precisa do CLIENT_SECRET
- ✅ Não precisa criar endpoint para OAuth
- ✅ Funciona imediatamente
- ✅ Não expira (ou expira em muito tempo)

## Desvantagens

- ❌ Precisa ser gerada manualmente
- ❌ Se perder, precisa gerar nova
- ❌ Menos seguro para múltiplos usuários/empresas

## Quando Usar OAuth2 vs API Key Manual

- **API Key Manual**: Uso interno, desenvolvimento, testes, integração única
- **OAuth2**: Integração pública, múltiplos clientes, maior segurança

## Referência

Baseado na conversa do suporte Factorial:
> "if they will use this only in an internal way, they can avoid the development of the endpoint, as will use it once, and they can generate the API Key manually in the frontend with a couple of clicks"
