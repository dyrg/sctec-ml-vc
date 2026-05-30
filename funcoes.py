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
        tuple[list[dict], int]: linhas tatadas e total de células corrigidas.
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
