# 🚀 GUIA COMPLETO - AUTOMATIZAÇÃO TOTAL DOS COLETORES

## 📋 SITUAÇÃO ATUAL

Você tem **2 arquivos de configuração**:
- `config.env` - Configuração principal (com token antigo)
- `config_factorial.env` - Configuração OAuth2 (com token válido)

## 🎯 OBJETIVO: UM ÚNICO ARQUIVO .ENV

Vamos consolidar tudo em **UM ÚNICO ARQUIVO** e automatizar completamente os coletores.

---

## 🔧 PASSO 1: CONSOLIDAR CONFIGURAÇÕES

### 1.1 - Criar o arquivo `.env` definitivo

```env
# ===========================================
# 🚀 ULTIMATE COLLECTOR - CONFIGURAÇÃO ÚNICA
# ===========================================
# Este é o ÚNICO arquivo de configuração do projeto
# Altere apenas este arquivo para configurar todo o sistema

# ===========================================
# 🔗 CONFIGURAÇÕES DA API FACTORIAL
# ===========================================
API_NAME=Factorial API
API_VERSION=2025-07-01
API_DESCRIPTION=API para coleta e envio de dados de RH da Factorial

# URL da API (ambiente demo)
BASE_URL=https://api.eu2.demo.factorial.dev

# SEU TOKEN OAUTH2 VÁLIDO (substitua pelo seu)
API_KEY=eyJraWQiOiJmYWN0b3JpYWwtaWQiLCJhbGciOiJFUzI1NiJ9.eyJpc3MiOiJmYWN0b3JpYWwtaWQiLCJpYXQiOjE3NjEwOTIyOTcsImp0aSI6ImY3MTVhMjUyLWUwYWQtNGQ3OS05MzY4LTYwMTgzMmU1NjM3MiIsImF1ZCI6Ik9yZlo0YTFnaGVQaWtkWFRCenZlTUxWU2hOQXF4SVF0UUlscUdWTTJUR1UiLCJleHAiOjE3NjEwOTU4OTcsImNlbGwiOiJhenVyZS1kZW1vLWd3Yy1ldTIiLCJzdWIiOiJhY2Nlc3M6OTA1ODc4IiwiYWNjZXNzX2lkIjo5MDU4NzgsInVzZXJfaWQiOjkwNTE1OSwiY29tcGFueV9pZCI6MjcyNzUsInR5cCI6ImFjY2VzcyIsInNjb3BlIjoiYmFua2luZyBjb21wYW55X2hvbGlkYXlzIGNvbXBhbnlfbGVnYWxfZW50aXRpZXMgY29tcGFueV9sb2NhdGlvbnMgY29udHJhY3RzIGN1c3RvbV9maWVsZHMgZG9jdW1lbnRzIGVtcGxveWVlcyBlbXBsb3llZV91cGRhdGVzIGV4cGVuc2VzIGZpbmFuY2Ugam9iX2NhdGFsb2cgbWFya2V0cGxhY2UgcGF5cm9sbCBwYXlyb2xsX3N1cHBsZW1lbnRzIHBlcmZvcm1hbmNlIHBvc3RzIHByb2plY3RfbWFuYWdlbWVudF9leHBlbnNlcyBwcm9qZWN0X21hbmFnZW1lbnRfcHJvamVjdHMgcHJvamVjdF9tYW5hZ2VtZW50X3RpbWUgcmVjcnVpdG1lbnQgc2hpZnRfbWFuYWdlbWVudCB0YXNrcyB0aW1lX29mZiB0aW1lX3RyYWNraW5nIHRyYWluaW5ncyJ9.V74oeDoLSBbrY9XtsqJkKQuVKGisC-TYsVuOvBM6e8hupefvSbFbJCcrbE_3OnoVcS1Z-YIfBpfoWvWBm-x7Dw

# Tipo de autenticação
AUTH_TYPE=bearer

# ===========================================
# ⚙️ CONFIGURAÇÕES DE CONEXÃO
# ===========================================
REQUEST_TIMEOUT=60
MAX_RETRIES=3
RETRY_DELAY=2

# ===========================================
# 📊 CONFIGURAÇÕES DE LOGGING
# ===========================================
LOG_LEVEL=DEBUG
LOG_FILE=logs/factorial_api.log

# ===========================================
# 💾 CONFIGURAÇÕES DE CACHE
# ===========================================
CACHE_ENABLED=False
CACHE_TTL=300

# ===========================================
# 🚦 CONFIGURAÇÕES DE RATE LIMITING
# ===========================================
RATE_LIMIT_ENABLED=True
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600

# ===========================================
# 📁 CONFIGURAÇÕES DE DIRETÓRIOS
# ===========================================
DATA_RAW_DIR=Dados_Coletados/Dados_Brutos/Dados da API
DATA_PROCESSED_DIR=Dados_Coletados/Dados_Processados
DATA_REPORTS_DIR=Dados_Coletados/Relatorios
LOGS_DIR=Logs_Sistema

# ===========================================
# 🎯 CONFIGURAÇÕES DE COLETA
# ===========================================
DEFAULT_LIMIT=100
DEFAULT_DAYS_BACK=90
ENABLE_PAGINATION=True

# ===========================================
# 🌍 CONFIGURAÇÕES DE AMBIENTE
# ===========================================
ENVIRONMENT=development
DEBUG=True

# ===========================================
# 🔄 CONFIGURAÇÕES DE AUTOMAÇÃO
# ===========================================
# Executar coleta automática ao iniciar
AUTO_COLLECT_ON_START=False

# Categorias para coleta automática (separadas por vírgula)
AUTO_COLLECT_CATEGORIES=employees,expenses,time_tracking

# Intervalo de coleta automática (em minutos)
AUTO_COLLECT_INTERVAL=60

# ===========================================
# 📧 CONFIGURAÇÕES DE NOTIFICAÇÃO
# ===========================================
# Enviar notificações por email (True/False)
EMAIL_NOTIFICATIONS=False
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USERNAME=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha
EMAIL_TO=destinatario@gmail.com
```

---

## 🔄 PASSO 2: ATUALIZAR COLETORES PARA USAR .ENV

### 2.1 - Modificar `core/config.py`

```python
import os
from dotenv import load_dotenv

# Carregar .env automaticamente
load_dotenv()

class Config:
    # API
    API_NAME = os.getenv('API_NAME', 'Factorial API')
    API_VERSION = os.getenv('API_VERSION', '2025-07-01')
    API_DESCRIPTION = os.getenv('API_DESCRIPTION', 'API Factorial')
    BASE_URL = os.getenv('BASE_URL', 'https://api.eu2.demo.factorial.dev')
    API_KEY = os.getenv('API_KEY', '')
    
    # Autenticação
    AUTH_TYPE = os.getenv('AUTH_TYPE', 'bearer')
    
    # Conexão
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '60'))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
    RETRY_DELAY = int(os.getenv('RETRY_DELAY', '2'))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/factorial_api.log')
    
    # Diretórios
    DATA_RAW_DIR = os.getenv('DATA_RAW_DIR', 'Dados_Coletados/Dados_Brutos/Dados da API')
    DATA_PROCESSED_DIR = os.getenv('DATA_PROCESSED_DIR', 'Dados_Coletados/Dados_Processados')
    DATA_REPORTS_DIR = os.getenv('DATA_REPORTS_DIR', 'Dados_Coletados/Relatorios')
    LOGS_DIR = os.getenv('LOGS_DIR', 'Logs_Sistema')
    
    # Coleta
    DEFAULT_LIMIT = int(os.getenv('DEFAULT_LIMIT', '100'))
    DEFAULT_DAYS_BACK = int(os.getenv('DEFAULT_DAYS_BACK', '90'))
    ENABLE_PAGINATION = os.getenv('ENABLE_PAGINATION', 'True').lower() == 'true'
    
    # Automação
    AUTO_COLLECT_ON_START = os.getenv('AUTO_COLLECT_ON_START', 'False').lower() == 'true'
    AUTO_COLLECT_CATEGORIES = os.getenv('AUTO_COLLECT_CATEGORIES', 'employees').split(',')
    AUTO_COLLECT_INTERVAL = int(os.getenv('AUTO_COLLECT_INTERVAL', '60'))
    
    # Email
    EMAIL_NOTIFICATIONS = os.getenv('EMAIL_NOTIFICATIONS', 'False').lower() == 'true'
    EMAIL_SMTP_SERVER = os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
    EMAIL_SMTP_PORT = int(os.getenv('EMAIL_SMTP_PORT', '587'))
    EMAIL_USERNAME = os.getenv('EMAIL_USERNAME', '')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
    EMAIL_TO = os.getenv('EMAIL_TO', '')
```

### 2.2 - Modificar coletores para usar .env

**Remover todas as linhas hardcoded:**
```python
# ❌ REMOVER ESTAS LINHAS:
# os.environ['BASE_URL'] = 'https://api.eu2.demo.factorial.dev'
# os.environ['API_KEY'] = 'sua_chave_aqui'
# load_dotenv('config_factorial.env')

# ✅ MANTER APENAS:
from dotenv import load_dotenv
load_dotenv()  # Carrega .env automaticamente
```

---

## 🤖 PASSO 3: CRIAR SISTEMA DE AUTOMAÇÃO

### 3.1 - Criar `auto_collector.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 AUTO COLLECTOR - Sistema de Coleta Automática
Executa coleta automática baseada nas configurações do .env
"""

import time
import schedule
from datetime import datetime
from core.config import Config
from ultimate_collector.collectors.hr_data_masterultimate import HRDataMasterUltimate

class AutoCollector:
    def __init__(self):
        self.config = Config()
        self.collector = HRDataMasterUltimate()
        
    def collect_categories(self):
        """Coleta as categorias configuradas"""
        print(f"🤖 AUTO COLLECTOR - Iniciando coleta automática")
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📋 Categorias: {', '.join(self.config.AUTO_COLLECT_CATEGORIES)}")
        
        for category in self.config.AUTO_COLLECT_CATEGORIES:
            try:
                print(f"🔄 Coletando: {category}")
                self.collector.collect_category(category.strip())
                print(f"✅ {category} coletado com sucesso")
            except Exception as e:
                print(f"❌ Erro ao coletar {category}: {e}")
        
        print(f"🎉 Coleta automática concluída!")
    
    def start_scheduler(self):
        """Inicia o agendador de coleta automática"""
        if self.config.AUTO_COLLECT_ON_START:
            print("🚀 Executando coleta inicial...")
            self.collect_categories()
        
        # Agendar coleta periódica
        schedule.every(self.config.AUTO_COLLECT_INTERVAL).minutes.do(self.collect_categories)
        
        print(f"⏰ Agendador iniciado - Coleta a cada {self.config.AUTO_COLLECT_INTERVAL} minutos")
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Verificar a cada minuto

if __name__ == "__main__":
    collector = AutoCollector()
    collector.start_scheduler()
```

### 3.2 - Instalar dependência

```bash
pip install schedule
```

---

## 🚀 PASSO 4: CRIAR SCRIPTS DE EXECUÇÃO

### 4.1 - Criar `start_auto_collector.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 START AUTO COLLECTOR
Inicia o sistema de coleta automática
"""

import sys
from pathlib import Path

# Adicionar o diretório atual ao path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from auto_collector import AutoCollector

if __name__ == "__main__":
    print("🤖 INICIANDO AUTO COLLECTOR")
    print("=" * 50)
    
    try:
        collector = AutoCollector()
        collector.start_scheduler()
    except KeyboardInterrupt:
        print("\n👋 Auto Collector interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro no Auto Collector: {e}")
```

### 4.2 - Criar `collect_once.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 COLLECT ONCE - Coleta única
Executa uma coleta única baseada nas configurações do .env
"""

import sys
from pathlib import Path

# Adicionar o diretório atual ao path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.config import Config
from ultimate_collector.collectors.hr_data_masterultimate import HRDataMasterUltimate

def main():
    print("🎯 COLETA ÚNICA - Ultimate Collector")
    print("=" * 50)
    
    config = Config()
    collector = HRDataMasterUltimate()
    
    print(f"📋 Categorias configuradas: {', '.join(config.AUTO_COLLECT_CATEGORIES)}")
    
    for category in config.AUTO_COLLECT_CATEGORIES:
        try:
            print(f"🔄 Coletando: {category}")
            collector.collect_category(category.strip())
            print(f"✅ {category} coletado com sucesso")
        except Exception as e:
            print(f"❌ Erro ao coletar {category}: {e}")
    
    print("🎉 Coleta única concluída!")

if __name__ == "__main__":
    main()
```

---

## 📋 PASSO 5: ATUALIZAR MAIN.PY

### 5.1 - Adicionar opções de automação

```python
def show_main_menu():
    """Exibe o menu principal do sistema"""
    print("🚀 ULTIMATE COLLECTOR - SISTEMA UNIFICADO")
    print("=" * 60)
    print("📋 ESCOLHA UMA OPÇÃO:")
    print()
    print("📥 COLETA DE DADOS (PULL):")
    print("  1. 🎯 Coletor Master - Todos os dados da API")
    print("  2. ⚡ Coletor de Presença - Dados de presença com filtros")
    print("  3. 🔍 Coleta Personalizada - Escolher categorias específicas")
    print("  4. 🎯 Coleta Única - Baseada no .env")
    print()
    print("🤖 AUTOMAÇÃO:")
    print("  5. 🤖 Auto Collector - Coleta automática contínua")
    print("  6. ⏰ Agendar Coleta - Configurar horários")
    print()
    print("📤 ENVIO DE DADOS (PUSH):")
    print("  7. ⏰ Envio de Presença - Clock in/out")
    print("  8. 🗓️ Gerador de Turnos - Criar turnos automaticamente")
    print()
    print("🛠️ FERRAMENTAS:")
    print("  9. 📊 Analisador de Dados - Analisar dados coletados")
    print("  10. 🧹 Limpeza de Dados - Limpar dados antigos")
    print("  11. 🔧 Ferramentas de Debug - Debug e testes")
    print("  12. 🔍 Utilitários - Ferramentas auxiliares")
    print()
    print("⚙️ CONFIGURAÇÕES:")
    print("  13. 🔑 Testar Conexão - Verificar API")
    print("  14. ⚙️ Configurar .env - Editar configurações")
    print("  0. ❌ Sair")
    print("=" * 60)
```

---

## 🎯 PASSO 6: COMANDOS PARA USAR

### 6.1 - Comandos básicos

```bash
# 🎯 Coleta única (baseada no .env)
python collect_once.py

# 🤖 Auto Collector (contínuo)
python start_auto_collector.py

# 🚀 Menu principal
python main.py

# 🔑 Testar conexão
python -c "from core.api_client import APIClient; APIClient().test_connection()"
```

### 6.2 - Comandos avançados

```bash
# 📊 Coletar apenas funcionários
python -c "from ultimate_collector.collectors.hr_data_masterultimate import HRDataMasterUltimate; HRDataMasterUltimate().collect_category('employees')"

# 💰 Coletar apenas despesas
python -c "from ultimate_collector.collectors.hr_data_masterultimate import HRDataMasterUltimate; HRDataMasterUltimate().collect_category('expenses')"

# ⏰ Coletar apenas presença
python -c "from ultimate_collector.collectors.hr_data_masterultimate import HRDataMasterUltimate; HRDataMasterUltimate().collect_category('time_tracking')"
```

---

## 🔧 PASSO 7: CONFIGURAÇÃO FINAL

### 7.1 - Remover arquivos antigos

```bash
# Remover configurações antigas
rm config_factorial.env
rm config.env

# Manter apenas o .env
```

### 7.2 - Atualizar requirements.txt

```txt
requests>=2.31.0
pandas>=2.0.0
python-dotenv>=1.0.0
schedule>=1.2.0
```

---

## 🎉 RESULTADO FINAL

### ✅ O que você terá:

1. **UM ÚNICO ARQUIVO .ENV** - Toda configuração centralizada
2. **COLETORES AUTOMATIZADOS** - Funcionam sozinhos
3. **COMANDOS SIMPLES** - Fáceis de usar
4. **AUTOMAÇÃO COMPLETA** - Coleta contínua
5. **CONFIGURAÇÃO FLEXÍVEL** - Fácil de alterar

### 🚀 Como usar:

1. **Configure o .env** com suas credenciais
2. **Execute `python collect_once.py`** para coleta única
3. **Execute `python start_auto_collector.py`** para automação
4. **Use `python main.py`** para menu interativo

### 📋 Vantagens:

- ✅ **Zero configuração manual** nos coletores
- ✅ **Um arquivo .env** para tudo
- ✅ **Automação completa** disponível
- ✅ **Fácil de manter** e atualizar
- ✅ **Funciona do zero** sem modificações

---

**🎯 AGORA SEUS COLETORES ESTÃO 100% AUTOMATIZADOS E DEPENDENTES DE UM ÚNICO .ENV!**
