# Projeto final do módulo 1: previsão de churn

Documento em construção. Os trechos em aberto serão preenchidos conforme o notebook for evoluindo.

## Resumo executivo

Seção para a diretoria. Escrever por último.

- Problema: prever quais clientes têm maior risco de sair da plataforma.
- Achados da EDA: a base tem 16,84% de churn; clientes que saíram têm mediana de 1 em `Tenure`, contra 10 entre os que permaneceram.
- Modelo recomendado: _
- Por quê: _

## Problema de negócio

Uma plataforma de e-commerce quer achar clientes prestes a parar de comprar, para oferecer cupons de retenção a tempo.

Dois erros importam:

- falso positivo: gastar cupom com quem já ia continuar comprando;
- falso negativo: deixar escapar um cliente que estava saindo.

O objetivo é treinar e comparar KNN e Árvore de Decisão para prever `Churn`, e escolher o modelo olhando tanto generalização quanto o custo desses erros.

## Base de dados

- Arquivo: [`ecommerce_dataset.csv`](../datasets/ecommerce_dataset.csv)
- Registros: 5.630
- Colunas originais: 20
- Alvo: `Churn`
- Distribuição das classes: 83,16% permaneceram e 16,84% saíram

## Dicionário de dados

| Coluna | Tipo | Descrição |
| --- | --- | --- |
| `CustomerID` | numérica | ID do cliente |
| `Churn` | binária | 1 se o cliente saiu, caso contrário 0 |
| `Tenure` | numérica | tempo de relacionamento com a plataforma |
| `PreferredLoginDevice` | categórica | dispositivo preferido de login |
| `CityTier` | ordinal | classificação da cidade |
| `WarehouseToHome` | numérica | distância do armazém até a casa |
| `PreferredPaymentMode` | categórica | forma de pagamento preferida |
| `Gender` | categórica | gênero |
| `HourSpendOnApp` | numérica | horas no app |
| `NumberOfDeviceRegistered` | numérica | dispositivos cadastrados |
| `PreferedOrderCat` | categórica | categoria preferida de pedido |
| `SatisfactionScore` | ordinal | nota de satisfação |
| `MaritalStatus` | categórica | estado civil |
| `NumberOfAddress` | numérica | endereços cadastrados |
| `Complain` | binária | se houve reclamação |
| `OrderAmountHikeFromlastYear` | numérica | variação percentual do valor dos pedidos vs. ano anterior |
| `CouponUsed` | numérica | cupons usados |
| `OrderCount` | numérica | quantidade de pedidos |
| `DaySinceLastOrder` | numérica | dias desde o último pedido |
| `CashbackAmount` | numérica | valor de cashback |
| `cashback_por_pedido` | calculada | cashback recebido por pedido |

## Desenvolvimento e execução

O projeto foi desenvolvido no [Visual Studio Code](https://code.visualstudio.com/) com estas extensões:

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter)

### Preparação do ambiente

- Python 3.10+

```bash
cd modulo-1/projeto-final
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Use o `python`/`pip` do `.venv` depois de ativar. Se instalar com o Python do sistema, o kernel do notebook pode falhar ao iniciar.

### Dados

Cópia usada neste projeto:

```text
https://raw.githubusercontent.com/dyrg/sctec-ml-vc/main/modulo-1/datasets/ecommerce_dataset.csv
```

Se quiser a versão mais recente, o mesmo dataset está no [Kaggle](https://www.kaggle.com/datasets/ankitverma2010/ecommerce-customer-churn-analysis-and-prediction). Pode haver diferenças em relação ao arquivo daqui.

### Execução no VS Code

1. Abra a pasta `modulo-1/projeto-final` no VS Code.
2. Abra o arquivo `projeto_final.ipynb`.
3. Clique em **Selecionar Kernel** e escolha o interpretador Python da pasta `.venv`.
4. Use **Executar Tudo** para rodar as células na ordem.

### Execução pelo terminal

```bash
cd modulo-1/projeto-final
source .venv/bin/activate
jupyter notebook projeto_final.ipynb
```

## Metodologia

### 1. Análise exploratória

A base tem 5.630 registros e 20 colunas. Só 16,84% dos clientes saíram, então a acurácia sozinha pode passar uma impressão errada.

`Tenure` é o sinal mais forte até agora, com correlação de -0,349. Quem saiu tem mediana 1; quem ficou, 10. Reclamação também puxa o churn, com correlação de 0,250.

Sete colunas numéricas têm valores ausentes. O split vai manter a proporção das classes, e o balanceamento ficará só no treino.

### 2. Limpeza e tratamento

Não encontrei linhas duplicadas. Mesmo assim, `drop_duplicates()` continua no fluxo para proteger a limpeza caso a fonte mude (e devemos considerar que ela sempre pode mudar).

`HourSpendOnApp` é praticamente simétrica, então seus nulos foram preenchidos com a média. Nas outras seis colunas, a cauda à direita e os valores extremos puxam a média; nelas usamos a mediana. A base ficou sem valores ausentes.

Mantive os outliers. O IQR marcou muitos valores de `OrderCount` e `CouponUsed`, mas são contagens plausíveis de clientes ativos. Removê-los apagaria comportamento real.
Essa decisão pede atenção no KNN, enquanto a Árvore de Decisão tende a lidar melhor com os extremos.

### 3. Engenharia de atributos

```text
cashback_por_pedido = CashbackAmount / OrderCount
```

As colunas de origem já estavam sem nulos, e `OrderCount` não tinha zeros. A nova variável ficou sem valores ausentes ou infinitos.

A mediana de cashback por pedido é 88,50 para quem permaneceu e 77,50 para quem saiu. A diferença existe, mas é pequena demais para explicar o churn por si só. Com isso, `cashback_por_pedido` entra como mais um sinal, junto com as outras colunas.

### 4. Preparação dos dados

Codificar categóricas. Separar `X` e `y`. Split 80/20 com `stratify=y`. Balancear só o treino. `StandardScaler` só no KNN (fit no treino, transform no teste). Árvore sem escalonamento.

Escolhas: _

### 5. Modelagem e overfitting

Testar no mínimo quatro valores de `n_neighbors` e quatro de `max_depth`, comparando treino e teste.

| Modelo | Hiperparâmetro | Treino | Teste | Diagnóstico |
| --- | --- | ---: | ---: | --- |
| KNN | _ | _ | _ | _ |
| Árvore de Decisão | _ | _ | _ | _ |

Configurações escolhidas: _

### 6. Avaliação

Para as melhores configurações: classification report, matriz de confusão e leitura de FP/FN.

| Modelo | Acurácia | Precisão | Recall | F1 |
| --- | ---: | ---: | ---: | ---: |
| KNN | _ | _ | _ | _ |
| Árvore de Decisão | _ | _ | _ | _ |

## Veredito de negócio

Ligar o resultado ao custo de cupom desperdiçado vs. cliente perdido.

- Erro mais caro: _
- Modelo para produção: _
- Justificativa: _
- Limitações: _

## Estrutura

```text
projeto-final/
├── README.md
├── requirements.txt
└── projeto_final.ipynb
```
