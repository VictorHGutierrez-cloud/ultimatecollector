# 🔐 PASSO A PASSO COMPLETO - OAuth2 Factorial

## 📋 RESUMO DO QUE FUNCIONOU

Conseguimos conectar com sucesso na API da Factorial usando OAuth2 e coletar dados dos colaboradores! Aqui está o processo completo:

---

## 🚀 PASSO 1: CONFIGURAÇÃO INICIAL

### 1.1 - Credenciais OAuth2
Você tinha as credenciais OAuth2 da Factorial:
- **Client ID**: `OrfZ4a1ghePikdXTBzveMLVShNAqxIQtQIlqGVM2TGU`
- **Client Secret**: `w8FPABgXQy3RtRC1ngXFksR1nvXsV0SWnafL7-CUL8E`
- **Ambiente**: Demo (`https://app.eu2.demo.factorial.dev`)

### 1.2 - Configuração do Ambiente
Arquivo `config_factorial.env` configurado com:
```env
BASE_URL=https://api.eu2.demo.factorial.dev
AUTH_TYPE=bearer
```

---

## 🔑 PASSO 2: FLUXO OAUTH2 - AUTHORIZATION CODE

### 2.1 - Gerar URL de Autorização
Criamos a URL de autorização OAuth2:
```
https://api.eu2.demo.factorial.dev/oauth/authorize?client_id=OrfZ4a1ghePikdXTBzveMLVShNAqxIQtQIlqGVM2TGU&redirect_uri=https://app.eu2.demo.factorial.dev/&response_type=code&scope=banking+company_holidays+company_legal_entities+company_locations+contracts+custom_fields+documents+employees+employee_updates+expenses+finance+job_catalog+marketplace+payroll+payroll_supplements+performance+posts+project_management_expenses+project_management_projects+project_management_time+recruitment+shift_management+tasks+time_off+time_tracking+trainings
```

### 2.2 - Autorização Manual (VOCÊ FEZ)
1. ✅ Acessou a URL no navegador
2. ✅ Fez login como **ADMINISTRADOR** na Factorial
3. ✅ Autorizou as permissões da aplicação
4. ✅ Copiou o código da URL de redirecionamento: `2xFs_ubtijckHcC1-eLW1IwtgYrfWVoa-T0nP8-t8qQ`

---

## 🔄 PASSO 3: TROCA DO CÓDIGO POR ACCESS TOKEN

### 3.1 - Comando cURL que Funcionou
```bash
curl -X POST "https://api.eu2.demo.factorial.dev/oauth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=OrfZ4a1ghePikdXTBzveMLVShNAqxIQtQIlqGVM2TGU&client_secret=w8FPABgXQy3RtRC1ngXFksR1nvXsV0SWnafL7-CUL8E&code=2xFs_ubtijckHcC1-eLW1IwtgYrfWVoa-T0nP8-t8qQ&redirect_uri=https://app.eu2.demo.factorial.dev/&grant_type=authorization_code"
```

### 3.2 - Resposta de Sucesso
```json
{
  "access_token": "eyJraWQiOiJmYWN0b3JpYWwtaWQiLCJhbGciOiJFUzI1NiJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "02oi_vBCLsIRclER37BpGsJfRdxPa1mWFEdpAhnXOq4",
  "scope": "banking company_holidays company_legal_entities..."
}
```

---

## ⚙️ PASSO 4: CONFIGURAÇÃO DO SISTEMA

### 4.1 - Atualização do config_factorial.env
```env
BASE_URL=https://api.eu2.demo.factorial.dev
API_KEY=eyJraWQiOiJmYWN0b3JpYWwtaWQiLCJhbGciOiJFUzI1NiJ9...
AUTH_TYPE=bearer
```

### 4.2 - Teste de Conexão
```python
from core.api_client import APIClient
client = APIClient()
result = client.test_connection()  # ✅ Sucesso!
```

---

## 📊 PASSO 5: COLETA DE DADOS

### 5.1 - Coleta dos Colaboradores
```python
from ultimate_collector.collectors.hr_data_masterultimate import HRDataMasterUltimate
collector = HRDataMasterUltimate()
result = collector.collect_category('employees')
```

### 5.2 - Resultado
- ✅ **37 colaboradores** coletados com sucesso
- 💾 Dados salvos em JSON e CSV
- 📁 Localização: `Dados_Coletados/Dados_Brutos/Dados da API/Funcionários/`

---

## 🔍 PONTOS CHAVE QUE FIZERAM DAR CERTO

### ✅ 1. URL Correta do Ambiente
- **Demo**: `https://api.eu2.demo.factorial.dev` (não `api.factorialhr.com`)
- **Frontend**: `https://app.eu2.demo.factorial.dev`

### ✅ 2. Fluxo OAuth2 Correto
- **Authorization Code Flow** (não Client Credentials)
- **resource_owner_type=company** (para token da empresa)
- **Login como ADMINISTRADOR** obrigatório

### ✅ 3. Configuração do Sistema
- **AUTH_TYPE=bearer** (não oauth2)
- **API_KEY** com o access_token
- **BASE_URL** do ambiente correto

### ✅ 4. Permissões Amplas
- Scope completo com todas as permissões necessárias
- Incluindo: `employees`, `expenses`, `time_tracking`, etc.

---

## 🚨 PROBLEMAS QUE ENFRENTAMOS E COMO RESOLVEMOS

### ❌ Problema 1: Cliente não reconhecido
- **Erro**: `invalid_client`
- **Causa**: URL errada (`api.factorialhr.com` em vez de `api.eu2.demo.factorial.dev`)
- **Solução**: Usar URL do ambiente demo

### ❌ Problema 2: Token não funcionava
- **Erro**: 401 Unauthorized
- **Causa**: Token expirado ou ambiente errado
- **Solução**: Gerar novo token com OAuth2

### ❌ Problema 3: Configuração hardcoded
- **Erro**: Sistema não lia o .env
- **Causa**: Credenciais hardcoded no código
- **Solução**: Remover hardcode e usar `load_dotenv()`

---

## 📝 COMANDOS FINAIS QUE FUNCIONARAM

### 1. Teste de Conexão
```bash
python -c "from core.api_client import APIClient; client = APIClient(); print('✅ Sucesso!' if client.test_connection() else '❌ Falhou')"
```

### 2. Coleta de Dados
```bash
python -c "from ultimate_collector.collectors.hr_data_masterultimate import HRDataMasterUltimate; collector = HRDataMasterUltimate(); collector.collect_category('employees')"
```

---

## 🎯 RESULTADO FINAL

- ✅ **37 colaboradores** coletados
- ✅ **Token OAuth2** funcionando
- ✅ **Sistema configurado** corretamente
- ✅ **Dados salvos** em JSON e CSV
- ✅ **Pronto para** coletar outros dados (expenses, time_tracking, etc.)

---

## 🔄 PRÓXIMOS PASSOS

1. **Coletar mais dados**: expenses, time_tracking, etc.
2. **Configurar refresh token**: para renovar automaticamente
3. **Implementar monitoramento**: verificar expiração do token
4. **Expandir coleta**: outras categorias da API

---

## 💡 LIÇÕES APRENDIDAS

1. **Ambiente correto é crucial**: Demo vs Production
2. **OAuth2 requer interação manual**: Authorization Code Flow
3. **Admin login obrigatório**: para company tokens
4. **URLs específicas por ambiente**: não usar URLs genéricas
5. **Configuração via .env**: evitar hardcode

---

**🎉 MISSÃO CUMPRIDA! Sistema OAuth2 funcionando perfeitamente!**
