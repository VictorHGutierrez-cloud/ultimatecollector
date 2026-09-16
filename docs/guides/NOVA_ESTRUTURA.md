# 🏗️ NOVA ESTRUTURA DO ULTIMATE COLLECTOR

## 📋 VISÃO GERAL
Reestruturação completa do projeto para máxima organização e facilidade de uso.

## 📁 ESTRUTURA FINAL ORGANIZADA

```
Ultimate_Collector_Limpo/
├── 📁 src/                              # CÓDIGO FONTE
│   ├── 📁 core/                         # Sistema core
│   │   ├── api_client.py
│   │   ├── config.py
│   │   └── __init__.py
│   ├── 📁 collectors/                   # Coletores de dados
│   │   ├── hr_collector.py
│   │   ├── finance_collector.py
│   │   └── __init__.py
│   ├── 📁 senders/                      # Enviadores de dados
│   │   ├── attendance_sender.py
│   │   ├── finance_sender.py
│   │   └── __init__.py
│   └── 📁 utils/                        # Utilitários
│       ├── data_analyzer.py
│       ├── file_manager.py
│       └── __init__.py
├── 📁 scripts/                          # SCRIPTS DE EXECUÇÃO
│   ├── collect_data.py                  # Coleta única
│   ├── send_data.py                     # Envio único
│   ├── auto_collect.py                  # Coleta automática
│   ├── auto_send.py                     # Envio automático
│   └── main.py                          # Menu principal
├── 📁 config/                           # CONFIGURAÇÕES
│   ├── .env                             # Configuração principal
│   ├── config.example.env               # Exemplo de configuração
│   └── settings.json                    # Configurações avançadas
├── 📁 data/                             # DADOS ORGANIZADOS
│   ├── 📁 raw/                          # Dados brutos
│   │   ├── 📁 employees/                # Dados de funcionários
│   │   ├── 📁 finance/                  # Dados financeiros
│   │   ├── 📁 expenses/                 # Dados de despesas
│   │   └── 📁 attendance/               # Dados de presença
│   ├── 📁 processed/                    # Dados processados
│   └── 📁 reports/                      # Relatórios gerados
├── 📁 logs/                             # LOGS DO SISTEMA
│   ├── system.log
│   ├── api.log
│   └── errors.log
├── 📁 docs/                             # DOCUMENTAÇÃO
│   ├── README.md
│   ├── SETUP.md
│   ├── API_REFERENCE.md
│   └── EXAMPLES.md
├── 📁 tests/                            # TESTES
│   ├── test_collectors.py
│   ├── test_senders.py
│   └── test_api.py
├── 📁 tools/                            # FERRAMENTAS AUXILIARES
│   ├── cleanup.py                       # Limpeza de dados
│   ├── backup.py                        # Backup de dados
│   └── migrate.py                       # Migração de dados
├── requirements.txt                     # Dependências
├── setup.py                            # Instalação
└── README.md                           # Documentação principal
```

## 🎯 VANTAGENS DA NOVA ESTRUTURA

### ✅ ORGANIZAÇÃO:
- **Código fonte** separado em `src/`
- **Scripts** organizados em `scripts/`
- **Dados** organizados por categoria
- **Configurações** centralizadas

### ✅ FACILIDADE DE USO:
- **Um comando** para cada função
- **Configuração única** em `.env`
- **Documentação clara**
- **Estrutura intuitiva**

### ✅ MANUTENIBILIDADE:
- **Separação clara** de responsabilidades
- **Imports organizados**
- **Testes separados**
- **Logs organizados**

## 🚀 COMANDOS SIMPLIFICADOS

### 📥 COLETA DE DADOS:
```bash
python scripts/collect_data.py          # Coleta única
python scripts/auto_collect.py          # Coleta automática
```

### 📤 ENVIO DE DADOS:
```bash
python scripts/send_data.py             # Envio único
python scripts/auto_send.py             # Envio automático
```

### 🎯 MENU PRINCIPAL:
```bash
python scripts/main.py                  # Menu interativo
```

### 🛠️ FERRAMENTAS:
```bash
python tools/cleanup.py                 # Limpeza
python tools/backup.py                  # Backup
```

## 📊 ORGANIZAÇÃO DOS DADOS

### 📁 ESTRUTURA DE DADOS:
```
data/
├── raw/                                # Dados brutos da API
│   ├── employees/                      # Funcionários
│   │   ├── employees_20251021.csv
│   │   └── employees_20251021.json
│   ├── finance/                        # Dados financeiros
│   │   ├── accounts_20251021.csv
│   │   ├── categories_20251021.csv
│   │   └── journal_entries_20251021.csv
│   ├── expenses/                       # Despesas
│   │   ├── expenses_20251021.csv
│   │   └── expensables_20251021.csv
│   └── attendance/                     # Presença
│       └── shifts_20251021.csv
├── processed/                          # Dados processados
│   ├── reports/                        # Relatórios
│   └── analytics/                      # Análises
└── reports/                            # Relatórios finais
    ├── monthly/                        # Relatórios mensais
    └── custom/                         # Relatórios customizados
```

## ⚙️ CONFIGURAÇÃO SIMPLIFICADA

### 📄 ARQUIVO .env ÚNICO:
```env
# API Configuration
BASE_URL=https://api.eu2.demo.factorial.dev
API_KEY=seu_token_aqui
AUTH_TYPE=bearer

# Data Collection
AUTO_COLLECT_EMPLOYEES=true
AUTO_COLLECT_FINANCE=true
AUTO_COLLECT_EXPENSES=true

# Data Sending
AUTO_SEND_ATTENDANCE=false
AUTO_SEND_FINANCE=false

# Automation
COLLECT_INTERVAL=60
SEND_INTERVAL=30
```

## 🔄 MIGRAÇÃO

### 📋 PASSOS PARA MIGRAÇÃO:
1. ✅ Criar nova estrutura de pastas
2. ✅ Mover arquivos para locais corretos
3. ✅ Atualizar imports e caminhos
4. ✅ Consolidar configurações
5. ✅ Testar nova estrutura
6. ✅ Atualizar documentação

## 🎉 RESULTADO FINAL

### ✅ ANTES (Confuso):
- Arquivos espalhados
- Múltiplas configurações
- Estrutura confusa
- Difícil de manter

### ✅ DEPOIS (Organizado):
- Estrutura profissional
- Configuração única
- Fácil de usar
- Fácil de manter
- Documentação clara
- Testes organizados
