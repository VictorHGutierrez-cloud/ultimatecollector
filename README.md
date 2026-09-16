# Ultimate Collector

Sistema para **coletar, enviar e popular** ambientes sandbox da **Factorial** — com CLI, menu e **app desktop (.exe)**.

## App Desktop (recomendado)

### Desenvolvimento (sem .exe)

```bash
pip install -r requirements.txt
python app/main.py
```

### Gerar o .exe

1. Dê dois cliques em [`build/build_exe.bat`](build/build_exe.bat)
2. Abra `dist/UltimateCollector/UltimateCollector.exe`
3. (Opcional) rode [`build/create_shortcut.ps1`](build/create_shortcut.ps1) para atalho na Área de Trabalho

Guia completo: [`build/README_BUILD.md`](build/README_BUILD.md)

### Como usar o app

1. Clique em **Novo cliente (pelo token)**
2. Cole a API key (o Company ID e lido automaticamente)
3. (Opcional) digite um nome tipo `Acme Demo`
4. Clique **Criar cliente**
5. Clique **Testar conexao**
6. Use as abas:
   - **Coletar** — baixa dados da API
   - **Enviar** — clock in/out
   - **Demo** — seed SZV + botão **Editar Demo** (catalog.json)

---

## CLI (`uc.py`)

```bash
pip install -r requirements.txt

python uc.py menu
python uc.py clients list
python uc.py --client africa verify-token
python uc.py --client africa collect employees
python uc.py --client szv seed --dry-run
```

---

## Onde ficam os dados coletados

Cada cliente salva em:

```
data/clients/{cliente}/raw/{categoria}/
```

Exemplo (Africa + employees):

`data/clients/africa/raw/employees/employees_20260912_120000.csv`

## Pasta de materiais por cliente (`{cliente}asset`)

Ao criar (ou ativar) um cliente, o sistema cria:

```
clients/{cliente}/{cliente}asset/
```

Exemplo para Statistic Institute:

`clients/statistic-institute/statistic-instituteasset/`

Coloque aí PDFs, Excel e docs do demo (Time Off, etc.).

## Credenciais por cliente

| Cliente | Pasta | Token |
|---------|-------|-------|
| Africa (55229) | `clients/africa/secrets/` | `seutoken.txt` |
| SZV (167952) | `clients/szv/secrets/` | ou `config/unificado.env` |
| Ibero (28692) | `clients/ibero/secrets/` | `chaveapiibero.txt` |
| Pre-sales (27275) | `clients/presales/secrets/` | `apitenantpresales.txt` |

Config global (fallback): `config/unificado.env`

---

## Estrutura

```
Ultimate_Collector_Limpo/
├── app/                       ← APP DESKTOP (CustomTkinter)
│   ├── main.py
│   ├── ui/                    ← paineis + editor de catalog
│   └── services/
├── build/                     ← gerar .exe
│   ├── build_exe.bat
│   ├── ultimate_collector.spec
│   └── README_BUILD.md
├── uc.py                      ← CLI
├── ultimate_collector/        ← pacote Python
│   ├── cli.py
│   ├── services/sandbox_runner.py
│   └── core/client_config.py
├── clients/                   ← perfis sandbox
├── scripts/
├── config/
├── assets/oas/
└── docs/ESTRUTURA.md
```

---

## Fases concluídas

| Fase | Entrega |
|------|---------|
| Core multi-cliente | `clients/*/profile.json` + CLI |
| Prep desktop | paths PyInstaller + session token + SandboxRunner |
| A | App: token + testar + coletar + log |
| B | App: enviar presença |
| C | App: seed SZV dry-run/apply |
| D | Build `.exe` (PyInstaller onedir) |
| E | Editor visual do `catalog.json` |
