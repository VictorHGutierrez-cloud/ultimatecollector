# 🔧 Guia de Debug - Attendance Sender

## 📋 Problemas Identificados e Soluções

### ❌ Problema 1: Token Expirado
**Status**: ✅ **CORRIGIDO**

**O que estava errado:**
- O token JWT na configuração havia expirado
- Data de expiração no token: `exp: 2076659956` (válido até 2025-10-27)
- Token atual expirou e não é mais válido

**Solução:**
1. Gerar um novo token JWT para a API Factorial
2. Usar OAuth2 com Client Credentials Flow (recomendado)
3. Atualizar o arquivo `config_unificado.env` com as novas credenciais

---

### ❌ Problema 2: Import Incorreto
**Status**: ✅ **CORRIGIDO**

**O que estava errado:**
```python
from ultimate_collector.core.api_client import APIClient  # ❌ ERRADO
```

**Corrigido para:**
```python
from core.api_client import APIClient  # ✅ CORRETO
```

---

### ✅ Problema 3: Arquivo de Configuração Ausente
**Status**: ✅ **CORRIGIDO**

**Solução implementada:**
- Arquivo `config_unificado.env` criado automaticamente
- Dependências de configuração verificadas

---

## 🎯 Como Usar o Attendance Sender

### 1. Configurar Credenciais

**Opção A: Usar Token JWT (Manual)**

1. Obtenha um token JWT válido da API Factorial
2. Edite o arquivo `config_unificado.env`:
```env
API_KEY=seu_token_jwt_aqui
AUTH_TYPE=bearer
```

**Opção B: Usar OAuth2 (Recomendado)**

1. Você já tem as credenciais OAuth2 configuradas:
```env
CLIENT_ID=OrfZ4a1ghePikdXTBzveMLVShNAqxIQtQIlqGVM2TGU
CLIENT_SECRET=w8FPABgXQy3RtRC1ngXFksR1nvXsV0SWnafL7-CUL8E
TOKEN_URL=https://api.eu2.demo.factorial.dev/oauth/token
```

2. O sistema automaticamente obterá um novo token quando necessário

---

### 2. Executar Teste de Debug

```bash
python senders/debug_attendance.py
```

**O que esta ferramenta faz:**
- ✅ Verifica configurações de ambiente
- ✅ Testa imports de módulos
- ✅ Testa conexão com a API
- ✅ Valida employee IDs
- ✅ Identifica e corrige problemas comuns

---

### 3. Usar o Clock Interface

#### Exemplo 1: Clock In Simples
```python
from senders.clock_interface import ClockInterface

interface = ClockInterface()
success = interface.clock_in(
    employee_id=270105,
    observations="Entrada via sistema"
)

if success:
    print("✅ Clock in registrado com sucesso!")
```

#### Exemplo 2: Clock Out Simples
```python
success = interface.clock_out(
    employee_id=270105,
    observations="Saída via sistema"
)
```

#### Exemplo 3: Turno Completo
```python
success = interface.register_shift(
    employee_id=270105,
    clock_in_time="2024-01-15 08:00:00",
    clock_out_time="2024-01-15 17:00:00",
    observations="Turno completo"
)
```

#### Exemplo 4: Ver Turnos
```python
interface.show_employee_shifts(
    employee_id=270105,
    date="2024-01-15"  # Opcional
)
```

---

## 🛠️ Ferramentas de Debug Disponíveis

### 1. `senders/debug_attendance.py`
Ferramenta completa de debug e diagnóstico
```bash
python senders/debug_attendance.py
```

### 2. `senders/test_connection_simple.py`
Teste direto de conexão com a API
```bash
python senders/test_connection_simple.py
```

---

## 📝 Endpoints da API Factorial

### Clock In
```
POST /api/2025-07-01/resources/attendance/shifts/clock_in
```

**Parâmetros:**
- `employee_id` (int): ID do funcionário
- `now` (ISO datetime): Data/hora do clock in
- `latitude` (float, opcional): Latitude
- `longitude` (float, opcional): Longitude
- `observations` (string, opcional): Observações

### Clock Out
```
POST /api/2025-07-01/resources/attendance/shifts/clock_out
```

**Parâmetros:** Mesmos do clock in

### Registrar Turno Completo
```
POST /api/2025-07-01/resources/attendance/shifts
```

**Parâmetros:**
- `employee_id` (int): ID do funcionário
- `date` (YYYY-MM-DD): Data do turno
- `clock_in` (HH:MM): Horário de entrada
- `clock_out` (HH:MM): Horário de saída
- `latitude` (float, opcional): Latitude
- `longitude` (float, opcional): Longitude
- `observations` (string, opcional): Observações

### Buscar Turnos
```
GET /api/2025-07-01/resources/attendance/shifts
```

**Parâmetros:**
- `employee_id` (int): ID do funcionário
- `date` (YYYY-MM-DD, opcional): Data específica

---

## 🔍 Troubleshooting

### Erro 401: Unauthorized
**Causa:** Token expirado ou inválido

**Solução:**
1. Verifique se o token está válido
2. Gere um novo token usando OAuth2
3. Atualize `config_unificado.env`

### Erro 404: Not Found
**Causa:** Employee ID não encontrado

**Solução:**
1. Liste os funcionários disponíveis
2. Use um ID válido
3. Verifique permissões da API

### Erro de Import
**Causa:** Paths de import incorretos

**Solução:**
1. Execute `python senders/debug_attendance.py`
2. Verifique se todos os imports estão OK
3. Certifique-se de que está na raiz do projeto

---

## 📞 Próximos Passos

1. ✅ **O que foi feito:**
   - Corrigido import path em `attendance_sender.py`
   - Criado arquivo `config_unificado.env`
   - Criada ferramenta de debug
   - Configuradas credenciais OAuth2

2. ⚠️ **O que você precisa fazer:**
   - Obter um novo token JWT válido OU
   - Configurar OAuth2 para renovação automática de tokens

3. 🧪 **Para testar:**
   ```bash
   python senders/debug_attendance.py
   ```

---

## 📚 Referências

- Documentação API Factorial: https://factorialhr.com/api/docs
- Arquivo de configuração: `config_unificado.env`
- Logs: `logs/factorial_api.log`
- Credenciais: `apitenantpresales.txt` (MANTER CONFIDENCIAL)

---

## ⚠️ Importante

**Segurança:**
- ❌ NUNCA commite o arquivo `config_unificado.env` com credenciais
- ✅ Use `.gitignore` para proteger credenciais
- ✅ Mantenha `apitenantpresales.txt` fora do controle de versão

**Tokens:**
- Os tokens JWT expiram após um período (geralmente 24 horas)
- Use OAuth2 para renovação automática
- Monitore expiração de tokens nos logs

