"""
main.py :: Pipeline de sanitização de dados da Olist.

Gerencia leitura, limpeza e validação dos datasets de produtos e pedidos.

Uso:
    python main.py (ou python3 main.py)

Os CSVs devem estar na pasta data/
"""

import os
import time

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
    # ---------- Cálculo de tempo de processamento ----------
    inicio = time.time()
    data_hoje = time.strftime("%d/%m/%Y, %H:%M")

    # ---------- Produtos ----------
    produtos = funcoes.carregar_csv(CAMINHO_PRODUTOS)
    total_produtos = len(produtos)

    produtos, n_cat = funcoes.preencher_categoria(produtos)
    produtos, n_dim = funcoes.preencher_dimensoes(produtos, COLUNAS_DIMENSOES)
    produtos = funcoes.padronizar_categorias(produtos)
    categorias_unicas = sorted({linha["product_category_name"] for linha in produtos})

    # ---------- Pedidos ----------
    pedidos = funcoes.carregar_csv(CAMINHO_PEDIDOS)
    total_pedidos = len(pedidos)
    sem_data, com_data = funcoes.separar_entregas_vazias(pedidos)
    hipotese = funcoes.verificar_hipotese_cancelamento(sem_data)
    pedidos, n_datas = funcoes.formatar_datas_aprovacao(pedidos)
    total_cancelados = funcoes.contar_status(pedidos, "canceled")

    # ---------- Análise manual ----------
    nulos_corrigidos = n_cat + n_dim

    # ---------- Relatório final ----------
    print(" ")

    # HEADER
    print("╔" + "═" * 62 + "╗")
    print("║      Relatório de Sanitização de Dados - Cliente OLIST       ║")
    print("╠" + "═" * 62 + "╣")

    # DADOS
    print("║  " + " " * 58 + "  ║")
    print(f"║  Produtos processados ............................... {total_produtos}  ║")
    print(f"║  Pedidos processados ................................ {total_pedidos}  ║")
    print(f"║  Total de linhas processadas ....................... {total_produtos + total_pedidos}  ║")
    print("║  " + "─" * 58 + "  ║")
    print(f"║  Categorias preenchidas ('sem categoria').............. {n_cat}  ║")
    print(f"║  Categorias únicas ..................................... {len(categorias_unicas)}  ║")
    print(f"║  Dimensões físicas preenchidas (média) .................. {n_dim}  ║")
    print(f"║  Total de nulos corrigidos ............................ {nulos_corrigidos}  ║")
    print(f"║  Datas de aprovação convertidas (BR) ................ {n_datas}  ║")
    print("║  " + "─" * 58 + "  ║")
    print(f"║  Total de pedidos cancelados .......................... {total_cancelados}  ║")
    print(f"║  Pedidos sem data de entrega ......................... {hipotese['total_sem_data']}  ║")
    print(f"║  -> cancelados ........................................ {hipotese['cancelados']}  ║")
    print(f"║  -> NÃO cancelados ................................... {hipotese['nao_cancelados']}  ║")
    print(f"║  -> sem status .......................................... {hipotese['sem_status']}  ║")
    print("║ " + " " * 60 + " ║")

    # HIPÓTESE
    print("╠" + "═" * 62 + "╣")
    print("║ ╭" + "─" * 58 + "╮ ║")
    print("║ │" + " " * 58 + "│ ║")
    if hipotese["hipotese_confirmada"]:
        print("║ │   Hipótese 'data nula => cancelado': CONFIRMADA          │ ║")
    else:
        print("║ │   Hipótese 'data nula => cancelado': REFUTADA            │ ║")
        print("║ │   Datas nulas também ocorrem em pedidos não cancelados   │ ║")
        print("║ │   (invoiced, processing, shipped, unavailable, etc.).    │ ║")
    print("║ │" + " " * 58 + "│ ║")
    print("║ ╰" + "─" * 58 + "╯ ║")
    print("╚" + "═" * 62 + "╝")

    # Firula: Cálculo de espaçamento para processamentos lentos
    fim = time.time()
    tempo_total = fim - inicio
    if tempo_total > 10:
        espacos = 17
    else:
        espacos = 18

    # FOOTER
    print(f" {data_hoje}" + " " * espacos + f"Processado em {tempo_total:.2f} segundos ")
    print(" ")


if __name__ == "__main__":
    main()
