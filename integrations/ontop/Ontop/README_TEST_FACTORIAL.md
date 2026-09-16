# Guia de Teste - Inserção de Dados Factorial

Este guia explica como usar o script `test_factorial_data_insert.py` para inserir dados de teste na API Factorial e validar o relatório SQL.

## 📋 Pré-requisitos

1. **API Key do Factorial**
   - Obtenha sua API key no painel do Factorial
   - Configure como variável de ambiente ou no código

2. **Dados Existentes no Factorial**
   - Pelo menos 1 funcionário ativo
   - Pelo menos 1 Policy Period configurado
   - Pelo menos 1 Taxonomy (tipo de compensação) disponível

3. **Bibliotecas Python**
   ```bash
   pip install requests
   ```

## 🚀 Como Usar

### Passo 1: Configurar API Key

**Opção A: Variável de Ambiente (Recomendado)**
```bash
# Windows PowerShell
$env:FACTORIAL_API_KEY = "sua_api_key_aqui"

# Windows CMD
set FACTORIAL_API_KEY=sua_api_key_aqui

# Linux/Mac
export FACTORIAL_API_KEY="sua_api_key_aqui"
```

**Opção B: Editar o Código**
Abra `test_factorial_data_insert.py` e altere:
```python
FACTORIAL_API_KEY = 'sua_api_key_aqui'
```

### Passo 2: Executar o Script

```bash
python test_factorial_data_insert.py
```

### Passo 3: Verificar os Dados Criados

O script irá:
- ✅ Criar 3 Supplements com datas diferentes (últimos 6 meses)
- ✅ Criar 2 Additional Compensations (se houver contrato)
- ✅ Salvar um resumo em `factorial_test_data_created.json`

## 📊 O que o Script Cria

### Supplements (Suplementos)
- **Quantidade**: 3 registros
- **Valores**: $100, $200, $300
- **Datas**: Distribuídas nos últimos 6 meses
- **Unidade**: "money" (fixo)

### Additional Compensations (Compensações Adicionais)
- **Quantidade**: 2 registros (apenas se houver contrato)
- **Valores**: $150, $250
- **Datas**: Distribuídas nos últimos 6 meses
- **Unidade**: "money" (fixo)

## 🔍 Estrutura dos Dados Criados

### Supplements
```json
{
  "employee_id": 123,
  "amount_in_cents": 10000,  // $100.00
  "effective_on": "2024-12-01",
  "contracts_taxonomy_id": 1,
  "payroll_policy_period_id": 1,
  "unit": "money"
}
```

### Additional Compensations
```json
{
  "contract_version_id": 456,
  "contracts_taxonomy_id": 1,
  "amount": 15000,  // $150.00
  "unit": "money",
  "description": "Test Additional Compensation 1",
  "first_payment_on": "2024-12-01"
}
```

## 📝 Campos Importantes para o SQL

O SQL que você está testando busca:

### Da tabela `supplements`:
- `id` → Usado para gerar "Reference" (CA00001, CA00002, etc.)
- `employee_id` → Usado para buscar dados do funcionário
- `amount` → "Price per Unit" e "Price"
- `effective_on` → "Payment date"
- `name` → "Tag(optional)"
- `unit` → "Unit"
- `employee_observations` ou `supplement_observations` → "Comments"

### Da tabela `additional_compensations`:
- `id` → Usado para gerar "Reference" (CA00001, CA00002, etc.)
- `employee_id` → Usado para buscar dados do funcionário
- `amount` → "Price per Unit" e "Price"
- `first_payment` → "Payment date"
- `title` → "Tag(optional)"
- `type` → Usado para determinar "Unit" (hourly → "Per hour", fixed → "Per task")
- `description` → "Comments"

## ⚠️ Observações Importantes

1. **Policy Periods**: O script usa o primeiro policy period encontrado. Certifique-se de que há pelo menos um ativo.

2. **Taxonomies**: O script usa a primeira taxonomy encontrada. Certifique-se de que há pelo menos uma disponível.

3. **Contratos**: Additional Compensations só são criadas se o funcionário tiver um contrato ativo.

4. **Datas**: Os dados são criados com datas nos últimos 6 meses para aparecer no SQL (que filtra `>= CURRENT_DATE - INTERVAL '6 months'`).

5. **Valores em Centavos**: A API Factorial trabalha com valores em centavos:
   - $100.00 = 10000 centavos
   - $150.50 = 15050 centavos

## 🧪 Testando o SQL

Após executar o script:

1. **Verificar no Factorial**: Acesse o painel e confirme que os dados foram criados

2. **Executar o SQL**: Use o SQL fornecido para gerar o relatório

3. **Validar os Dados**: Verifique se:
   - Os funcionários aparecem corretamente
   - As referências estão no formato correto (CA00001, etc.)
   - Os valores estão corretos
   - As datas estão corretas
   - Os campos editáveis estão preenchidos

## 🔧 Personalização

Você pode personalizar o script editando:

### Quantidade de Registros
```python
# Na função main(), altere:
for i in range(3):  # Altere 3 para o número desejado
```

### Valores
```python
# Para Supplements:
amount_in_cents = (i + 1) * 10000  # Altere o multiplicador

# Para Additional Compensations:
amount = (i + 1.5) * 10000  # Altere o multiplicador
```

### Datas
```python
# Altere o intervalo de dias:
date = base_date - timedelta(days=60 * i)  # Altere 60 para outro valor
```

### Unidades
```python
# Para Supplements:
unit='money'  # Pode ser 'money', 'hours', etc.

# Para Additional Compensations:
unit='money'  # Pode ser 'money', 'hours', etc.
```

## 🐛 Troubleshooting

### Erro: "401 Unauthorized"
- Verifique se a API key está correta
- Verifique se a API key tem permissões necessárias

### Erro: "404 Not Found"
- Verifique se há funcionários ativos
- Verifique se há policy periods configurados
- Verifique se há taxonomies disponíveis

### Erro: "422 Unprocessable Entity"
- Verifique se os IDs fornecidos existem
- Verifique se as datas estão no formato correto (YYYY-MM-DD)
- Verifique se os valores estão em centavos

### Nenhum dado criado
- Verifique os logs do script
- Verifique se há funcionários ativos
- Verifique se há policy periods ativos

## 📚 Referências

- [Documentação da API Factorial](https://factorialhr.com/api-documentation)
- Endpoint Supplements: `POST /api/2026-01-01/resources/payroll/supplements`
- Endpoint Compensations: `POST /api/2026-01-01/resources/contracts/compensations`

## 📄 Arquivos Gerados

Após executar o script, será criado:
- `factorial_test_data_created.json`: Resumo dos IDs criados para referência

## ✅ Checklist de Validação

Após executar o script e rodar o SQL, verifique:

- [ ] Supplements aparecem no relatório
- [ ] Additional Compensations aparecem no relatório
- [ ] Referências estão no formato correto (CA00001, etc.)
- [ ] Worker IDs estão corretos
- [ ] Nomes e emails dos funcionários estão corretos
- [ ] Valores estão corretos
- [ ] Datas estão corretas
- [ ] Campos editáveis estão preenchidos
- [ ] Campos NOT EDITABLE estão corretos
