# Guia Rápido - Obter Token OAuth2 Factorial

## 📋 Passo a Passo

### 1. Gerar URL de Autorização

Execute:
```bash
cd Ontop
python get_oauth2_token_simple.py
```

Isso vai mostrar a URL de autorização. **Copie a URL completa**.

### 2. Autorizar no Navegador

1. Cole a URL no navegador
2. Faça login como **ADMINISTRADOR** na Factorial
3. Autorize todas as permissões
4. Você será redirecionado para: `https://app.eu2.demo.factorial.dev/?code=XXXXX`
5. **Copie o código** (parte depois de `code=`)

### 3. Obter Access Token

**Opção A: Script Interativo**
```bash
python get_oauth2_token.py
```
- Cole o código quando solicitado
- O script vai obter o token automaticamente

**Opção B: Script com Código como Argumento**
```bash
python get_oauth2_token.py --code SEU_CODIGO_AQUI
```

### 4. Configurar o Token

O script vai mostrar o `access_token`. Adicione ao `config_unificado.env`:

```env
API_KEY=eyJraWQiOiJmYWN0b3JpYWwtaWQiLCJhbGciOiJFUzI1NiJ9...
AUTH_TYPE=bearer
```

### 5. Testar

```bash
python test_factorial_connection.py
```

---

## 🔑 Credenciais OAuth2

- **Client ID**: `NyFzeb2fUEvPKehzOyUh-SGKNy27uUR-KqxW1rhA4l4`
- **Client Secret**: (precisa ser fornecido - não está no .env por segurança)
- **Redirect URI**: `https://app.eu2.demo.factorial.dev/`
- **Base URL**: `https://api.eu2.demo.factorial.dev`

---

## ⚠️ Importante

1. **Login como ADMINISTRADOR** é obrigatório
2. O token expira em **1 hora** (3600 segundos)
3. Use `AUTH_TYPE=bearer` (não `x-api-key`)
4. O token deve ser usado como: `Authorization: Bearer {token}`

---

## 🔄 Renovar Token

Quando o token expirar, repita o processo acima para obter um novo token.
