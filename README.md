# Pipeline de Sanitização de Dados - cliente Olist

Script em Python puro que limpa e valida os datasets de produtos e pedidos da Olist, preparando-os para uso em modelos de ML.


## Descrição do Projeto

A equipe de Engenharia de Dados da Olist (e-commerce) extraiu dois lotes de dados (`olist_products_dataset.csv` e `olist_orders_dataset.csv`) que apresentam inconsistências (valores nulos, strings mal formatadas, datas ausentes), travando os relatórios automatizados.

Este projeto é um **pipeline de sanitização (ETL)** escrito em **Python** que:

1. lê os CSVs de forma nativa com `csv.DictReader`;
2. preenche categorias vazias com `"sem categoria"` e imputa a média nas dimensões físicas nulas;
3. padroniza os nomes de categoria (minúsculas, sem espaços/caracteres especiais) com strings e expressões regulares/RegEx;
4. separa pedidos sem data de entrega e testa a hipótese de negócio de que essas datas nulas seriam exclusivas de pedidos cancelados;
5. converte as datas de aprovação para o formato brasileiro `DD/MM/AAAA`;
6. imprime um relatório estatístico construído manualmente (usando [Box Drawing](https://en.wikipedia.org/wiki/Box-drawing_characters))


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


---


## Resultado

**Resultado de negócio:** a hipótese "data de entrega nula ⇒ pedido cancelado" é **refutada**: dos 2965 pedidos sem data de entrega, apenas 619 estão cancelados; os demais tem outros status (`invoiced`, `processing`, `shipped`, `unavailable`, etc.).


## Reflexão Teórica sobre Machine Learning

A qualidade de um modelo de Machine Learning depende da qualidade dos dados que entram no treino: é o velho "[*Garbage in, garbage out*](https://en.wikipedia.org/wiki/Garbage_in,_garbage_out)". Neste lote da Olist, 610 produtos chegaram sem categoria e algumas dimensões físicas vieram nulas. Se esses nulos fossem preenchidos com zero, a média e o desvio das colunas de peso e tamanho seriam puxados para baixo, e o modelo herdaria esse viés sem perceber. Foi por isso que a imputação usou a média da própria coluna, e não um valor fixo arbitrário.

Já a padronização das categorias (minúsculas, strip e regex) funciona como defesa preventiva. Mesmo que neste lote os nomes já venham limpos, um lote futuro pode trazer `Cama Mesa Banho` e `cama_mesa_banho` como se fossem diferentes, fragmentando uma categoria só em várias e enfraquecendo o sinal estatístico. Tratar isso antes do treino reduz viés e ajuda o modelo a generalizar, em vez de decorar artefatos de formatação (*overfitting*). Um dataset consistente expõe a estrutura real do problema, enquanto um sujo ensina o modelo a confiar em coincidências.


---
