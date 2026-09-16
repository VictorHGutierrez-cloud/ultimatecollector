# Estrutura do Repositório

## Mapa visual

```
Ultimate_Collector_Limpo/
├── app/                           ← APP DESKTOP (CustomTkinter)
│   ├── main.py                    ← python app/main.py
│   ├── ui/
│   │   ├── app_window.py
│   │   ├── token_panel.py
│   │   ├── collect_panel.py
│   │   ├── send_panel.py
│   │   ├── seed_panel.py
│   │   ├── log_panel.py
│   │   └── catalog/               ← editor do catalog.json
│   └── services/
│       ├── threading_runner.py
│       └── catalog_service.py
│
├── build/                         ← gerar .exe
│   ├── build_exe.bat
│   ├── create_shortcut.ps1
│   ├── ultimate_collector.spec
│   └── README_BUILD.md
│
├── uc.py                          ← CLI principal
├── ultimate_collector.py          ← atalho menu sandbox
│
├── ultimate_collector/            ← pacote Python
│   ├── cli.py
│   ├── sandbox_menu.py
│   ├── services/sandbox_runner.py ← usado pelo app e CLI
│   ├── core/
│   │   ├── client_config.py
│   │   ├── config.py
│   │   ├── paths.py               ← compatível com PyInstaller
│   │   └── api_client.py
│   ├── collectors/
│   └── senders/
│
├── clients/                       ← sandboxes
│   ├── africa/profile.json
│   ├── szv/profile.json + catalog.json
│   ├── ibero/
│   └── presales/
│
├── scripts/
├── config/
├── assets/oas/
├── data/clients/{id}/raw/
└── dist/UltimateCollector/        ← .exe gerado (após build)
```

## Comandos por tarefa

| Tarefa | Comando |
|--------|---------|
| App desktop (dev) | `python app/main.py` |
| Gerar .exe | `build\build_exe.bat` |
| Menu sandbox CLI | `python uc.py menu` |
| Listar clientes | `python uc.py clients list` |
| Validar token | `python uc.py --client africa verify-token` |
| Coletar | `python uc.py --client africa collect employees` |
| Seed SZV | `python uc.py --client szv seed --dry-run` |

## Perfil de cliente (`profile.json`)

Cada cliente tem um arquivo `clients/{id}/profile.json` com `company_id`, API, secrets e features (`collect`, `send`, `seed`).

## Adicionar novo cliente

1. Crie `clients/novo_cliente/profile.json`
2. Crie `clients/novo_cliente/secrets/` com token
3. Rode `python uc.py clients list`
4. Teste: `python uc.py --client novo_cliente verify-token`
5. No app desktop o cliente aparece no dropdown automaticamente
