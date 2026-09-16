# Cliente Africa (Factorial RH Africa — company 55229)

## Arquivos

| Arquivo | Descrição |
|---------|-----------|
| `run_collector.py` | Menu de coleta |
| `run_sender.py` | Menu de envio |
| `secrets/seutoken.txt` | Token da API |
| `secrets/config_local.env` | Config local (opcional) |

## Como usar

```bash
python clients/africa/run_collector.py
python clients/africa/run_sender.py
```

O token em `secrets/seutoken.txt` tem prioridade sobre a config global.
