# Como Abrir um Período de Payroll no Factorial

## Problema
O erro "Invalid parameters" ao criar supplements acontece porque o **período de payroll está FECHADO**.

## Solução

### 1. Abrir um Período Existente

1. Acesse o frontend do Factorial
2. Vá em **Payroll** ou **Compensation**
3. Selecione um período (ex: "February 2026" ou próximo período)
4. Verifique se o período está com status:
   - ✅ **"Preparation"** ou **"Open"** - Pode criar supplements
   - ❌ **"Closed"** - NÃO pode criar supplements

5. Se estiver fechado, procure por um botão para:
   - **"Open Period"**
   - **"Reopen Period"**
   - **"Change Status"**

### 2. Criar um Novo Período

1. No frontend, vá em **Payroll** > **Create New Period**
2. Configure o novo período
3. Deixe-o em status **"Preparation"** ou **"Open"**

### 3. Descobrir o ID do Período Aberto

Depois de abrir um período, você pode:

**Opção A: Usar o script de descoberta**
```bash
cd Ontop
python descobrir_policy_period_ids.py
```

**Opção B: Me passar o ID**
- Se você souber o ID do período aberto, me passe e eu atualizo o script

**Opção C: Adicionar ao config**
```env
POLICY_PERIOD_ID=123
```

### 4. Executar o Script

Depois de ter um período aberto:

```bash
cd Ontop
# Usar ID do config
python test_factorial_data_insert.py

# Ou passar como argumento
python test_factorial_data_insert.py 123
```

## Verificação

Para verificar se um período está aberto, tente criar um supplement manualmente no frontend. Se funcionar, o período está aberto!
