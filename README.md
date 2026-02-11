BotTelegramVigiLigga
=====================

Resumo
------
Este repositório contém um bot Telegram (arquivo `bot.py`) e scripts auxiliares para gerar planilhas (`gerar_excel_formularios.py`, `atualiza_itens_excel.py`, `gerar_toolkit_sections.py`) e para rodar o bot com reinício automático (`run_bot_with_watchdog.py`).

Pré-requisitos
--------------
- Python 3.12+
- Variáveis de ambiente (.env) contendo o token do Telegram (ex.: `TELEGRAM_TOKEN=...`).

Instalação (recomendada com virtualenv)
--------------------------------------
```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip setuptools wheel
.venv/bin/python -m pip install -r requirements.txt
```

Gerar planilhas
---------------
- `gerar_excel_formularios.py` gera `itens_formularios.xlsx` a partir das estruturas internas.
- `atualiza_itens_excel.py` também pode ser usado para atualizar o arquivo.

Rodar o bot
-----------
Coloque seu token no `.env` e rode:

```bash
.venv/bin/python run_bot_with_watchdog.py
```

Observações
-----------
- Não comite tokens ou `.env` no repositório público.
- Recomendo adicionar `requirements.txt` (já incluído) com versões pinadas antes de produção.

Como salvar (commit e push) neste repositório no GitHub
------------------------------------------------------
1) Se você já tem o repositório remoto configurado (origin):

```bash
git add .
git commit -m "Add helper scripts, requirements and README"
git push origin main
```

2) Se ainda não tem repositório remoto, crie um no GitHub e empurre (exemplo com `gh`):

```bash
# cria repo remoto no GitHub (interativo) e adiciona remote origin
gh repo create familiapinheiro0095/BotTelegramVigiLigga --public --source=. --remote=origin --push
```

Ou manual (sem `gh`):
```bash
# criar no GitHub via web, então:
git remote add origin git@github.com:SEU_USUARIO/NOME_REPO.git
git branch -M main
git push -u origin main
```

Se precisar, posso criar o commit e abrir o PR/Push para você (preciso de autorização para operar git aqui).