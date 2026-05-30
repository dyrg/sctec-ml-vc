"""
funcoes.py :: Funções de sanitização do pipeline de dados da Olist.

RESTRIÇÃO: SOMENTE bibliotecas nativas (csv, re, datetime) e operadores padrões do Python. Nada de Pandas =(

Funções com propósito único, parâmetros e retorno bem definidos.
"""

import csv
import re
from datetime import datetime


def carregar_csv(caminho):
    """Lê um arquivo CSV e devolve uma lista de dicionários (uma por linha).

    Usa gerenciador de contexto with open() e csv.DictReader para extrair os dados de forma estruturada e nativa (sem Pandas!).

    Parâmetros:
        caminho (str): caminho do arquivo .csv.
    Retorna:
        list[dict]: cada item representa uma linha, chaveada pelo cabeçalho.
    """
    with open(caminho, mode="r", encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        return [linha for linha in leitor]


def preencher_categoria(linhas):
    """Preenche product_category_name vazio/nulo com 'Sem Categoria'.

    Parâmetros:
        linhas (list[dict]): registros de produtos.
    Retorna:
        tuple[list[dict], int]: as linhas tratadas e quantas foram corrigidas.
    """
    n_corrigidos = 0
    for linha in linhas:
        valor = (linha.get("product_category_name") or "").strip()
        if valor == "":
            linha["product_category_name"] = "Sem Categoria"
            n_corrigidos += 1
    return linhas, n_corrigidos


def calcular_media_coluna(linhas, coluna):
    """Calcula a média dos valores numéricos não vazios de uma coluna.

    Valores vazios ou não numéricos são ignorados no cálculo.
    Retorna 0.0 se não houver nenhum valor válido.
    """
    valores = []
    for linha in linhas:
        bruto = (linha.get(coluna) or "").strip()
        if bruto != "":
            try:
                valores.append(float(bruto))
            except ValueError:
                pass  # ignora valores não numéricos
    if not valores:
        return 0.0
    return sum(valores) / len(valores)


def preencher_dimensoes(linhas, colunas_dim):
    """Preenche nulos das dimensões físicas com a MÉDIA de cada coluna.

    JUSTIFICATIVA TÉCNICA DESTA ESCOLHA:
    A quantidade de nulos nas dimensões físicas é muito pequena em relação ao total de registros.
    Optou-se por imputar a MÉDIA (e não descartar a linha) para:
      1) preservar todos os registros para análises estatísticas futuras, evitando perda de dados (drop) que reduziria a amostra;
      2) evitar o viés que um valor fixo (ex.: 0) introduziria nas agregações (médias, somas), distorcendo o dataset.

    Parâmetros:
        linhas (list[dict]): registros de produtos.
        colunas_dim (list[str]): nomes das colunas de dimensão a tratar.
    Retorna:
        tuple[list[dict], int]: linhas tratadas e total de células corrigidas.
    """
    medias = {col: calcular_media_coluna(linhas, col) for col in colunas_dim}
    n_corrigidos = 0
    for linha in linhas:
        for col in colunas_dim:
            bruto = (linha.get(col) or "").strip()
            if bruto == "":
                linha[col] = round(medias[col], 2)
                n_corrigidos += 1
    return linhas, n_corrigidos


def padronizar_categoria(texto):
    """Normaliza um nome de categoria usando RegEx.

    Etapas:
      - remove espaços nas extremidades (.strip());
      - converte para minúsculas (.lower());
      - remove caracteres especiais/pontuação via RegEx, mantendo apenas letras, dígitos, underscore (_) e espaço;
      - strip espaços internos repetidos em um único espaço.

    Parâmetros:
        texto (str): nome bruto da categoria.
    Retorna:
        str: nome padronizado.
    """
    texto = (texto or "").strip().lower()
    texto = re.sub(r"[^a-z0-9_ ]", "", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def padronizar_categorias(linhas):
    """Aplica padronizar_categoria a product_category_name de cada registro.

    Parâmetros:
        linhas (list[dict]): registros de produtos.
    Retorna:
        list[dict]: linhas com a categoria padronizada.
    """
    for linha in linhas:
        linha["product_category_name"] = padronizar_categoria(
            linha.get("product_category_name", "")
        )
    return linhas


def formatar_data_br(texto):
    """Converte 'AAAA-MM-DD HH:MM:SS' para 'DD/MM/AAAA' usando datetime.

    Retorna string vazia se a entrada for vazia; se o formato for inesperado, devolve o texto original sem interromper o processamento.

    Parâmetros:
        texto (str): data no formato original.
    Retorna:
        str: data formatada ou valor de fallback.
    """
    bruto = (texto or "").strip()
    if bruto == "":
        return ""
    try:
        dt = datetime.strptime(bruto, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%d/%m/%Y")
    except ValueError:
        return bruto


def formatar_datas_aprovacao(linhas):
    """Aplica formatar_data_br a order_approved_at de cada pedido.

    Parâmetros:
        linhas (list[dict]): registros de pedidos.
    Retorna:
        tuple[list[dict], int]: linhas tratadas e total de datas convertidas.
    """
    n_convertidas = 0
    for linha in linhas:
        original = (linha.get("order_approved_at") or "").strip()
        if original != "":
            convertida = formatar_data_br(original)
            linha["order_approved_at"] = convertida
            if convertida != original:
                n_convertidas += 1
    return linhas, n_convertidas


def separar_entregas_vazias(linhas):
    """Separa pedidos com order_delivered_customer_date vazio dos demais.

    Parâmetros:
        linhas (list[dict]): registros de pedidos.
    Retorna:
        tuple[list[dict], list[dict]]: (sem_data, com_data).
    """
    sem_data = []
    com_data = []
    for linha in linhas:
        valor = (linha.get("order_delivered_customer_date") or "").strip()
        if valor == "":
            sem_data.append(linha)
        else:
            com_data.append(linha)
    return sem_data, com_data


def verificar_hipotese_cancelamento(sem_data):
    """Testa a hipótese de negócio sobre datas de entrega nulas.

    Hipótese: registros sem data de entrega ocorrem OBRIGATORIAMENTE porque o pedido foi cancelado. Conta, entre os sem data, quantos são 'canceled' e quantos tem outro status (usando if/elif/else).

    Parâmetros:
        sem_data (list[dict]): pedidos sem data de entrega.
    Retorna:
        dict: contagens e veredito (hipotese_confirmada True/False).
    """
    cancelados = 0
    outros = 0
    for linha in sem_data:
        status = (linha.get("order_status") or "").strip().lower()
        if status == "canceled":
            cancelados += 1
        elif status == "":
            outros += 1
        else:
            outros += 1
    return {
        "total_sem_data": len(sem_data),
        "cancelados": cancelados,
        "nao_cancelados": outros,
        # a hipótese só se confirma se NENHUM registro sem data tiver status diferente de 'canceled'
        "hipotese_confirmada": outros == 0,
    }
