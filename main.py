"""
main.py :: Pipeline de sanitização de dados da Olist.

Gerencia leitura, limpeza e validação dos datasets de produtos e pedidos.

Uso:
    python main.py (ou python3 main.py)

Os CSVs devem estar na pasta data/
"""

import os

import funcoes

# Pasta com os datasets baixados localmente
DIR_DADOS = os.path.join(os.path.dirname(__file__), "data")
CAMINHO_PRODUTOS = os.path.join(DIR_DADOS, "olist_products_dataset.csv")
CAMINHO_PEDIDOS = os.path.join(DIR_DADOS, "olist_orders_dataset.csv")


def main():
    produtos = funcoes.carregar_csv(CAMINHO_PRODUTOS)
    pedidos = funcoes.carregar_csv(CAMINHO_PEDIDOS)

    print("Produtos carregados:", len(produtos))
    print("Pedidos carregados:", len(pedidos))


if __name__ == "__main__":
    main()
