# Pipeline de Sanitização de Dados - cliente Olist

Script em Python puro que limpa e valida os datasets de produtos e pedidos da Olist, preparando-os para uso em modelos de ML.

## Pré-requisitos

- Python 3.8 ou superior. Verifique a versão instalada:

  - **Linux / macOS:** `python3 --version`
  - **Windows (PowerShell):** `python --version`

Se não tiver o Python: https://www.python.org/downloads/ (no Windows, marque para adicionar Python ao PATH, em inglês "Add Python to PATH", no instalador).

## Instalação

Não há dependências externas, apenas bibliotecas padrões do Python.

1. Clone este repositório:

   - **Linux / macOS / Windows:**
     ```bash
     git clone https://github.com/dyrg/sctec-m1s07-mini-projeto-avaliativo
     cd sctec-m1s07-mini-projeto-avaliativo
     ```

2. Baixe os datasets para a pasta `data/` (não versionada):

   - **Linux / macOS:**
     ```bash
     mkdir -p data
     git clone --depth 1 https://github.com/fiesc-junior-prado/mine_projeto_bloco_1 tmp_olist
     mv tmp_olist/olist_*.csv data/
     rm -rf tmp_olist
     ```
   - **Windows (PowerShell):**
     ```powershell
     mkdir data -Force
     git clone --depth 1 https://github.com/fiesc-junior-prado/mine_projeto_bloco_1 tmp_olist
     move tmp_olist\olist_*.csv data\
     Remove-Item -Recurse -Force tmp_olist
     ```

Ao final, `data/` deve conter `olist_products_dataset.csv` e `olist_orders_dataset.csv`.

## Execução

Na raiz do projeto:

- **Linux / macOS:**
  ```bash
  python3 main.py
  ```
- **Windows (PowerShell ou CMD):**
  ```powershell
  python main.py
  ```
`
