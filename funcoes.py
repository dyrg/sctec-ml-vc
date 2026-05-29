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
