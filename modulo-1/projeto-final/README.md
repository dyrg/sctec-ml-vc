# Projeto final do módulo 1: previsão de churn

Este projeto compara KNN e Árvore de Decisão para encontrar clientes com risco de churn.

## Resumo executivo

- Problema: prever quais clientes têm maior risco de sair da plataforma.
- Achados da EDA: a base tem 16,84% de churn; clientes que saíram têm mediana de 1 em `Tenure`, contra 10 entre os que permaneceram.
- Modelo recomendado: Árvore de Decisão com `max_depth=7`.
- Por quê: alcançou F1 de 0,635 e precisão de 0,505 na classe de churn. Em comparação com o KNN, reduziu 89 cupons desnecessários ao custo de 7 churners adicionais não identificados.

Relatório completo em linguagem não técnica, com todos os gráficos: [relatorio/RELATORIO.md](relatorio/RELATORIO.md).

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

![Distribuição de clientes que saíram e que permaneceram](relatorio/imagens/distribuicao_churn.png)

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

[Arquivo do projeto, restrito a membros SCTEC](https://drive.google.com/file/d/1Gcdv7zg4BDquToRBdRwIDksHicJPO0dd/view?usp=sharing)

Cópia usada neste projeto (acesso público pelo GitHub):

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

![Mapa de correlação de Pearson entre as variáveis numéricas](relatorio/imagens/correlacao_pearson.png)

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

Antes do encoding, juntamos nomes que representavam a mesma categoria, como `Phone` e `Mobile Phone`. `CustomerID` ficou fora dos preditores porque é apenas um identificador.

O split reservou 20% da base para teste com `stratify=y`. Ficamos com 4.504 clientes no treino e 1.126 no teste, ambos com cerca de 16,84% de churn.

As cinco colunas categóricas passaram por one-hot encoding. O encoder foi ajustado somente no treino e depois aplicado ao teste. Assim, o teste não influenciou a criação das colunas. Os dois conjuntos ficaram com 31 preditores numéricos e nenhum valor ausente.

O treino foi balanceado com `RandomUnderSampler`. A classe majoritária caiu de 3.746 para 758 registros, igualando os 758 casos de churn. Escolhi essa técnica para não criar combinações artificiais nas colunas one-hot. O teste não foi balanceado e continua com a proporção original de churn (190 de 1.126 clientes, 16,87%; o mesmo 16,84% da base completa, só que arredondado a partir de um número menor de clientes).

No fluxo do KNN, o `StandardScaler` foi ajustado em 11 variáveis quantitativas do treino balanceado e aplicado ao teste. As variáveis categóricas e ordinais continuaram na escala original. A Árvore de Decisão usa o mesmo treino balanceado, mas sem escalonamento, porque seus cortes não dependem da escala.

### 5. Modelagem e overfitting

Testamos cinco valores de `n_neighbors` (3, 5, 7, 9 e 11) e cinco de `max_depth` (3, 5, 7, 10 e sem limite). Em cada cenário, comparamos F1 de treino e teste.

| Modelo | Hiperparâmetro | F1 treino | F1 teste | Recall teste (Churn) | Gap de F1 |
| --- | --- | ---: | ---: | ---: | ---: |
| KNN | `n_neighbors=5` | 0,911 | 0,558 | 0,895 | 0,353 |
| Árvore de Decisão | `max_depth=7` | 0,905 | 0,635 | 0,858 | 0,269 |

No KNN, K=3 teve F1 de teste quase igual ao de K=5, mas com gap maior. Preferi K=5. Na Árvore, profundidade ilimitada decorou o treino (F1 1,000) e `max_depth=10` ainda carregou overfitting demais. Ficamos então com `max_depth=7`.

Até aqui, a Árvore generaliza melhor no F1 de teste e tem o menor gap. Mas no recall da classe Churn o KNN é maior (0,895 contra 0,858): o F1 mais alto da Árvore vem de uma precisão melhor, não de pegar mais churners. Um pega mais churn enquanto o outro desperdiça menos cupom.

### 6. Avaliação

| Modelo | Acurácia | Precisão churn | Recall churn | F1 churn | FP | FN |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| KNN | 0,761 | 0,406 | 0,895 | 0,558 | 249 | 20 |
| Árvore de Decisão | 0,834 | 0,505 | 0,858 | 0,635 | 160 | 27 |

O KNN encontra 170 dos 190 churners, sete a mais que a Árvore. A Árvore, por outro lado, evita 89 cupons enviados a clientes que permaneceriam.

![Matrizes de confusão do KNN e da Árvore de Decisão no conjunto de teste](relatorio/imagens/matrizes_confusao.png)

## Veredito de negócio

O falso negativo é o erro mais caro por caso, pois o cliente em risco não recebe nenhuma tentativa de retenção. Por isso colocaria a Árvore de Decisão com `max_depth=7` em produção, primeiro num piloto controlado: é o modelo com melhor equilíbrio entre F1, precisão e quantidade de cupons desnecessários. O KNN só passa a compensar se perder um churner custar mais de ~12 vezes o valor de um cupom.

Falta ainda o custo do cupom e o valor de um cliente retido, que o projeto não traz. A decisão também precisa ser reavaliada com novas levas de clientes e acompanhamento de mudança de comportamento.

## Contexto de mercado (curiosidade, fora do escopo do dataset)

A base não traz o custo do cupom nem o valor de um cliente retido, então a razão de ~12 do veredito fica sem comparação real. Fui pesquisar se esse número faz algum sentido no mundo real, só por curiosidade.

Antes de mais nada, quase passou batido um detalhe importante. Essa base vem do Kaggle e tem `UPI` como método de pagamento em `PreferredPaymentMode`, e UPI é o sistema de pagamento instantâneo da Índia[^1]. Então o dataset provavelmente reflete uma operação indiana, não brasileira. Isso importa porque qualquer valor em reais que eu buscasse pra comparar com `CashbackAmount` ia misturar moeda e poder de compra de economias diferentes, sem nenhuma conversão. Por isso não dá pra colocar um preço de cupom em R$ em cima dos números da base.

O que ainda dá pra usar é uma proporção, que não depende de moeda nenhuma. Tem uma estatística clássica de marketing que diz que adquirir cliente novo custa de 5 a 25 vezes mais que reter um que já existe. Fui atrás de onde isso vem: é de Frederick Reichheld e W. Earl Sasser Jr., num artigo de 1990 da Harvard Business Review chamado "Zero Defections: Quality Comes to Services"[^2], baseado em dados de cartão de crédito e seguros. Depois virou praticamente consenso com pesquisas da Bain & Company, e a própria HBR retomou o assunto num artigo de 2014[^3].

A razão de equilíbrio do projeto (~12) cai dentro dessa faixa de 5 a 25 vezes. Isso não prova nada sobre o negócio real por trás da base, só mostra que a ordem de grandeza não é absurda perto do que a literatura de retenção costuma considerar plausível em qualquer mercado. Também busquei benchmarks de CAC (custo de aquisição de cliente) fora do dataset: a Moyker[^4] reporta algo entre R$ 20 e R$ 150 pro e-commerce brasileiro; já Shopify[^5] e First Page Sage[^6] reportam CAC de e-commerce em dólar, também variando bastante por categoria (na casa de US$ 70 a US$ 400, dependendo do setor). Prefiro não usar nenhum desses números aqui porque são de mercados e moedas diferentes do dataset, que provavelmente reflete uma operação indiana, e não tem como saber se o cupom da base equivale a qualquer um deles. Ficam só registrados como algo que pesquisei e descartei.

## Glossário de termos técnicos

Alguns termos técnicos que aparecem no texto podem soar complicados para quem não é da área, segue abaixo uma referência rápida para auxiliar no entendimento:

- **Churn**: cliente que deixou de comprar na plataforma. É o que o modelo tenta prever.
- **Falso positivo**: o modelo aponta churn num cliente que ia continuar comprando. Custa um cupom oferecido à toa.
- **Falso negativo**: o modelo não percebe um cliente que realmente ia sair. Custa a perda desse cliente, sem nenhuma tentativa de retê-lo.
- **KNN (k-vizinhos mais próximos)**: modelo que decide olhando os clientes mais parecidos com aquele que está sendo avaliado, dentro da base de treino. [Documentação (scikit-learn)](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html)
- **Árvore de Decisão**: modelo que decide através de uma sequência de perguntas do tipo sim ou não sobre as variáveis, por exemplo "Tenure é menor que 2?". [Documentação (scikit-learn)](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html)
- **Overfitting**: quando o modelo decora os dados de treino em vez de aprender um padrão que também funcione em dados novos. Ele acerta quase tudo no treino e erra bem mais no teste. [Exemplo visual (scikit-learn)](https://scikit-learn.org/stable/auto_examples/model_selection/plot_underfitting_overfitting.html)
- **One-hot encoding**: transforma uma coluna de texto, como forma de pagamento, em várias colunas de 0 e 1, porque os modelos só trabalham com número. [Documentação (scikit-learn)](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html)
- **RandomUnderSampler**: técnica de balanceamento que remove parte dos clientes da classe mais comum (quem ficou), pra equilibrar com a classe rara (quem saiu). [Documentação (imbalanced-learn)](https://imbalanced-learn.org/stable/references/generated/imblearn.under_sampling.RandomUnderSampler.html)
- **StandardScaler**: coloca as variáveis numéricas na mesma escala. Sem isso, uma variável com números grandes, como distância em km, pesaria mais na conta do que uma com números pequenos, como nota de satisfação de 1 a 5. [Documentação (scikit-learn)](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html)
- **Precisão**: dos clientes que o modelo apontou como churn, quantos realmente eram. [Documentação (scikit-learn)](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html)
- **Recall**: dos clientes que realmente saíram, quantos o modelo conseguiu encontrar. [Documentação (scikit-learn)](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html)
- **F1**: uma nota única que equilibra precisão e recall, útil pra comparar modelos sem precisar escolher entre os dois separadamente. [Documentação (scikit-learn)](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html)
- **Matriz de confusão**: tabela que mostra lado a lado os acertos e os dois tipos de erro do modelo. [Documentação (scikit-learn)](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html)

## Estrutura final

```text
projeto-final/
├── README.md
├── requirements.txt
├── projeto_final.ipynb
└── relatorio/
    ├── RELATORIO.md
    └── imagens/
        ├── distribuicao_churn.png
        ├── tempo_relacionamento_por_classe.png
        ├── correlacao_pearson.png
        ├── boxplots_variaveis.png
        ├── overfitting_knn.png
        ├── overfitting_arvore.png
        └── matrizes_confusao.png
```

-----

## Referências

[^1]: What is UPI (Unified Payments Interface)? Stripe. https://stripe.com/br/resources/more/unified-payments-interface-upi

[^2]: REICHHELD, Frederick F.; SASSER, W. Earl Jr. Zero Defections: Quality Comes to Services. Harvard Business Review, set./out. 1990. https://hbr.org/1990/09/zero-defections-quality-comes-to-services

[^3]: The Value of Keeping the Right Customers. Harvard Business Review, out. 2014. https://hbr.org/2014/10/the-value-of-keeping-the-right-customers

[^4]: Como calcular CAC real em e-commerce. Moyker Inteligência. https://www.moyker.com.br/inteligencia/satelite/como-calcular-cac-real-ecommerce (empresa nova, número usado com reserva)

[^5]: Custo de aquisição de clientes por setor (2025). Shopify Brasil. https://www.shopify.com/br/blog/custo-de-aquisicao-de-clientes-por-setor (dado próprio de 2021, mercado americano, empresas com menos de 4 funcionários)

[^6]: Average CAC for eCommerce Companies. First Page Sage. https://firstpagesage.com/reports/average-cac-for-ecommerce-companies/ (dado próprio da agência, carteira de clientes 2020-2025, mercado americano)
