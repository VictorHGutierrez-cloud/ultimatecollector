# Arquivo legado

Código antigo e duplicado. **Não use estes arquivos.**

O código ativo está em `ultimate_collector/`. Scripts ativos estão em `scripts/`.

| Subpasta | Conteúdo |
|----------|----------|
| `core/`, `collectors/`, `senders/`, `src/` | Duplicatas da Fase 1 |
| `v1_codes/` | Scripts v1 originais |

## Conteúdo

| Pasta | Descrição |
|-------|-----------|
| `core/` | Cópia antiga de `ultimate_collector/core/` |
| `collectors/` | Cópia antiga dos coletores |
| `senders/` | Cópia antiga dos senders |
| `src/` | Estrutura intermediária da reestruturação incompleta |

## Imports corretos (use estes)

```python
from ultimate_collector.core.config import Config
from ultimate_collector.core.api_client import APIClient
from ultimate_collector.collectors.hr_data_masterultimate import HRDataMasterUltimate
from ultimate_collector.senders.attendance_sender import AttendanceSender
from ultimate_collector.senders.ultimate_sender import UltimateSender
```
