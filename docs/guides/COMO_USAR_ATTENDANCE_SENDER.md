# 🕐 Como Usar o Attendance Sender - Guia Completo

## 📌 O QUE FOI FEITO

### ✅ Problemas Corrigidos

1. **Caminho de Import Incorreto**
   - **Antes:** O código tentava importar de um caminho que não existia
   - **Agora:** Corrigido para usar o caminho correto

2. **Arquivo de Configuração**
   - **Antes:** Arquivo de configuração não existia
   - **Agora:** Criado `config_unificado.env` com suas credenciais

3. **Token Expirado**
   - **Problema:** O token na configuração expirou em 27/10/2025
   - **Solução:** Você precisa obter um novo token

---

## 🎯 O QUE É O ATTENDANCE SENDER?

O Attendance Sender é um sistema que **envia dados de presença** (entrada/saída) para o Factorial.

**O que ele faz:**
- Registra quando funcionários entram (CLOCK IN)
- Registra quando funcionários saem (CLOCK OUT)
- Registra turnos completos de uma vez
- Consulta histórico de presença

---

## 📋 PASSO A PASSO PARA USAR

### 1️⃣ PRIMEIRO: Obtenha um Token Válido

O token atual expirou. Você tem 2 opções:

#### OPÇÃO A: Token JWT Manual (Mais Simples)

1. Acesse o Factorial
2. Vá em **Configurações** > **API**
3. Gere um novo token
4. Copie o token
5. Abra o arquivo `config_unificado.env`
6. Cole o token na linha `API_KEY=`
7. Salve o arquivo

#### OPÇÃO B: OAuth2 (Automático - Recomendado)

Já está configurado! As credenciais OAuth2 estão no arquivo. Você só precisa garantir que o sistema use OAuth2 em vez do token JWT.

Para usar OAuth2:
1. Altere `AUTH_TYPE=bearer` para `AUTH_TYPE=oauth2` no arquivo `config_unificado.env`
2. O sistema vai gerar tokens automaticamente quando necessário

---

### 2️⃣ TESTAR A CONEXÃO

Execute este comando para verificar se está funcionando:

```bash
python senders/debug_attendance.py
```

**O que você vai ver:**

✅ **Se estiver tudo OK:**
```
✅ Conexão com API estabelecida
✅ AttendanceSender inicializado com sucesso
```

❌ **Se houver problemas:**
```
❌ Erro 401: Token expirado
❌ Variáveis não configuradas
```

---

### 3️⃣ USAR O SISTEMA

#### Opção 1: Interface Simples (Recomendado para Iniciantes)

Crie um arquivo chamado `teste_clock.py` na raiz do projeto:

```python
from senders.clock_interface import ClockInterface

# Criar interface
interface = ClockInterface()

# Registrar entrada
print("🕐 Registrando entrada...")
sucesso = interface.clock_in(
    employee_id=270105,  # ID do funcionário
    observations="Entrada automática"
)

if sucesso:
    print("✅ Entrada registrada!")
else:
    print("❌ Erro ao registrar entrada")

# Registrar saída
print("\n🕐 Registrando saída...")
sucesso = interface.clock_out(
    employee_id=270105,
    observations="Saída automática"
)

if sucesso:
    print("✅ Saída registrada!")
else:
    print("❌ Erro ao registrar saída")
```

Execute:
```bash
python teste_clock.py
```

#### Opção 2: Uso Avançado (Programático)

```python
from senders.attendance_sender import AttendanceSender
from datetime import datetime, timezone

# Criar sender
sender = AttendanceSender()

# Clock in
resultado = sender.clock_in(
    employee_id=270105,
    latitude=-23.5505,
    longitude=-46.6333,
    observations="Chegada no trabalho"
)

print(f"✅ Clock in: {resultado}")

# Clock out
resultado = sender.clock_out(
    employee_id=270105,
    observations="Saída do trabalho"
)

print(f"✅ Clock out: {resultado}")
```

---

## 🛠️ FUNÇÕES DISPONÍVEIS

### 1. Clock In (Entrada)
Registra a entrada de um funcionário.

**Parâmetros:**
- `employee_id` (obrigatório): ID do funcionário
- `latitude` (opcional): Latitude do local
- `longitude` (opcional): Longitude do local  
- `observations` (opcional): Observações sobre a batida

**Exemplo:**
```python
interface.clock_in(
    employee_id=270105,
    latitude=-23.5505,
    longitude=-46.6333,
    observations="Entrada manual"
)
```

### 2. Clock Out (Saída)
Registra a saída de um funcionário.

**Mesmos parâmetros do Clock In**

**Exemplo:**
```python
interface.clock_out(
    employee_id=270105,
    observations="Saída manual"
)
```

### 3. Registrar Turno Completo
Registra entrada e saída de uma vez.

**Parâmetros:**
- `employee_id`: ID do funcionário
- `clock_in_time`: Horário de entrada (formato: "YYYY-MM-DD HH:MM:SS")
- `clock_out_time`: Horário de saída (formato: "YYYY-MM-DD HH:MM:SS")

**Exemplo:**
```python
interface.register_shift(
    employee_id=270105,
    clock_in_time="2024-01-15 08:00:00",
    clock_out_time="2024-01-15 17:00:00",
    observations="Turno normal"
)
```

### 4. Ver Turnos de um Funcionário
Consulta os turnos registrados.

**Parâmetros:**
- `employee_id`: ID do funcionário
- `date` (opcional): Data específica (formato: "YYYY-MM-DD")

**Exemplo:**
```python
interface.show_employee_shifts(employee_id=270105)
```

---

## 🔍 TROUBLESHOOTING (Resolução de Problemas)

### Erro: "Token expirado" ou "401 Unauthorized"

**O que fazer:**
1. Obtenha um novo token do Factorial
2. Atualize o arquivo `config_unificado.env`
3. Execute `python senders/debug_attendance.py` para testar

### Erro: "Funcionário não encontrado"

**O que fazer:**
1. Verifique se o `employee_id` está correto
2. Liste os funcionários disponíveis na API
3. Use um ID válido

### Erro: "Import error"

**O que fazer:**
1. Certifique-se de estar na raiz do projeto
2. Execute: `python senders/debug_attendance.py`
3. Veja se todos os imports estão OK

---

## 📁 ARQUIVOS IMPORTANTES

- **Configuração:** `config_unificado.env` (edite aqui para suas credenciais)
- **Debug:** `senders/debug_attendance.py` (execute para diagnosticar problemas)
- **Teste de Conexão:** `senders/test_connection_simple.py`
- **Logs:** `logs/factorial_api.log` (veja erros aqui)

---

## 💡 DICAS

1. **Sempre teste primeiro** com `python senders/debug_attendance.py`
2. **Mantenha tokens atualizados** - eles expiram em 24h
3. **Use logs** para identificar problemas
4. **Start simples** - use o `ClockInterface` primeiro
5. **Teste com um funcionário** antes de usar em produção

---

## 📞 PRÓXIMOS PASSOS

1. ✅ Configure o arquivo `config_unificado.env` com um token válido
2. ✅ Execute `python senders/debug_attendance.py` para verificar
3. ✅ Teste com um funcionário usando o exemplo acima
4. ✅ Se funcionar, integre no seu fluxo de trabalho

---

## ⚠️ IMPORTANTE

- Nunca compartilhe o arquivo `apitenantpresales.txt`
- Mantenha suas credenciais seguras
- Não commite arquivos `.env` com credenciais no GitHub

---

## 📚 EXEMPLO COMPLETO

Aqui está um exemplo completo funcionando:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Exemplo completo de uso do Attendance Sender"""

from senders.clock_interface import ClockInterface

def main():
    # Criar interface
    interface = ClockInterface()
    
    # ID do funcionário (da sua configuração)
    employee_id = 270105
    
    print("="*70)
    print("🕐 TESTE DE ATTENDANCE SENDER")
    print("="*70)
    
    # 1. Clock In
    print("\n1️⃣ Registrando entrada...")
    if interface.clock_in(employee_id, observations="Teste de sistema"):
        print("✅ Entrada OK!")
    else:
        print("❌ Erro na entrada")
        return
    
    # 2. Clock Out
    print("\n2️⃣ Registrando saída...")
    if interface.clock_out(employee_id, observations="Teste de sistema"):
        print("✅ Saída OK!")
    else:
        print("❌ Erro na saída")
        return
    
    # 3. Ver turnos
    print("\n3️⃣ Buscando turnos...")
    interface.show_employee_shifts(employee_id)
    
    print("\n" + "="*70)
    print("✅ TESTE CONCLUÍDO!")
    print("="*70)

if __name__ == "__main__":
    main()
```

Salve como `teste_completo.py` e execute:
```bash
python teste_completo.py
```

---

## ❓ Perguntas Frequentes

**P: Como sei qual employee_id usar?**
R: Execute `python senders/debug_attendance.py` e ele vai listar os IDs disponíveis.

**P: Os dados são enviados imediatamente?**
R: Sim! Cada chamada envia os dados na hora para a API.

**P: Posso registrar turnos de dias anteriores?**
R: Sim! Use a função `register_shift` com datas passadas.

**P: O que fazer se o token expirar?**
R: Obtenha um novo token e atualize `config_unificado.env`.

**P: Posso usar em produção?**
R: Sim, mas teste muito antes! Use logs e monitoramento.

---

**Boa sorte! 🚀**

