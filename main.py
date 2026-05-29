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

# Colunas de dimensão física que podem conter nulos
COLUNAS_DIMENSOES = [
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm",
]


def main():
    # ---------- Produtos ----------
    produtos = funcoes.carregar_csv(CAMINHO_PRODUTOS)
    total_produtos = len(produtos)

    produtos, n_cat = funcoes.preencher_categoria(produtos)
    produtos, n_dim = funcoes.preencher_dimensoes(produtos, COLUNAS_DIMENSOES)

    # ---------- Pedidos ----------
    pedidos = funcoes.carregar_csv(CAMINHO_PEDIDOS)
    total_pedidos = len(pedidos)

    # ---------- Relatório parcial ----------
    print(" ")
    print("------------- Relatório Parcial -------------")
    print("Produtos processados:", total_produtos)
    print("Pedidos processados:", total_pedidos)
    print("Categorias preenchidas ('Sem Categoria'):", n_cat)
    print("Dimensoes fisicas preenchidas (media):", n_dim)
    print("Total de nulos corrigidos:", n_cat + n_dim)
    print("------------- ################# -------------")
    print(" ")


if __name__ == "__main__":
    main()