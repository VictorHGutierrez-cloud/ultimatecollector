# Como gerar o .exe (passo a passo)

## O que você precisa

1. Python instalado no Windows
2. Este projeto na pasta `Ultimate_Collector_Limpo`

## Passo a passo

### 1. Abrir a pasta do projeto

No Explorer, entre em:

`Documents\Projetos Random\Ultimate_Collector_Limpo`

### 2. Gerar o executável

Dê **dois cliques** em:

`build\build_exe.bat`

Espere terminar (pode demorar alguns minutos na primeira vez).

### 3. Onde fica o .exe

Quando terminar, abra:

`dist\UltimateCollector\UltimateCollector.exe`

**Importante:** mantenha a pasta `dist\UltimateCollector` inteira (não só o `.exe`).
Dentro dela ficam `clients/`, `assets/`, `config/` e `data/`.

### 4. Atalho na Área de Trabalho (opcional)

1. Clique com o botão direito em `build\create_shortcut.ps1`
2. Escolha **Executar com o PowerShell**
3. Vai aparecer o atalho **Ultimate Collector** na Área de Trabalho

Se o Windows bloquear o script:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Depois rode de novo.

## Como usar o app

1. Abra o `UltimateCollector.exe`
2. Escolha o **cliente** (africa, szv, ibero, presales)
3. Cole o **token**
4. Clique em **Testar conexao**
5. Use as abas:
   - **Coletar** — baixa dados da API
   - **Enviar** — clock in/out
   - **Demo** — popular sandbox SZV / editar catalog

## Desenvolvimento (sem gerar .exe)

Na pasta do projeto:

```bash
pip install -r requirements.txt
python app/main.py
```

## Problemas comuns

| Problema | Solucao |
|----------|---------|
| `pip` nao encontrado | Instale Python e marque "Add to PATH" |
| App abre e fecha | Rode `python app/main.py` para ver o erro |
| Token falhou | Confira se o company_id do token bate com o cliente |
| Seed nao aparece | Selecione o cliente **szv** |
| Apply escreveu demais | Use sempre **Simular (dry-run)** primeiro |
