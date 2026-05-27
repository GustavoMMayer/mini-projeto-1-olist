# Mini Projeto - Machine Learning e Visão Computacional

## Descrição do Projeto

Este projeto realiza a sanitização de dados da base da Olist
utilizando apenas bibliotecas nativas do Python, sem Pandas.

O pipeline executa:
- Leitura de arquivos CSV com `csv.DictReader`
- Tratamento de valores nulos (categorias e dimensões físicas)
- Limpeza e padronização de strings com `re` e métodos nativos
- Validação de regra de negócio (pedidos cancelados vs. entregas vazias)
- Formatação de datas com `datetime`
- Geração de relatório estatístico exportado em `.txt`

## Como Executar

1. Clone o repositório:
```bash
   git clone https://github.com/GustavoMMayer/mini-projeto-1-olist
   cd seu-repo
```

2. Certifique-se de ter Python 3.8+ instalado.

3. Coloque os arquivos CSV na pasta `data/`.

4. Execute o pipeline:
```bash
   python main.py
```

5. O relatório será gerado em `resultados.txt`.


## Reflexão Teórica sobre Machine Learning

A qualidade dos dados é o alicerce de qualquer modelo de Machine
Learning. Quando alimentamos um algoritmo com dados sujos —
categorias nulas, dimensões ausentes ou datas mal formatadas —
o modelo aprende padrões incorretos ou enviesados, fenômeno
conhecido como *Garbage In, Garbage Out*. Isso pode gerar
**overfitting**, onde o modelo decora ruídos dos dados de treino
e performa mal em dados novos, ou **underfitting**, quando a
sujeira mascara padrões reais e o modelo não consegue aprender
nada útil.

Ao preencher valores nulos com a média da coluna, padronizar
strings e separar registros inconsistentes antes do treinamento,
garantimos que o modelo receba uma representação fiel da
realidade. No contexto da Olist, um modelo de previsão de
atrasos de entrega treinado com datas vazias ou pedidos
cancelados misturados com pedidos ativos produziria previsões
inúteis. O pipeline de sanitização desenvolvido aqui é,
portanto, uma etapa indispensável antes de qualquer aplicação
de inteligência artificial sobre estes dados.

## Decisões Técnicas

**Nulos nas dimensões físicas:** valores ausentes foram substituídos
pela média aritmética da coluna. A alternativa de descartar o registro
foi rejeitada pois geraria perda desnecessária de dados, prejudicando
a representatividade do dataset em futuros modelos de Machine Learning.

## Estrutura do Projeto
├── main.py         # Script principal (orquestra o pipeline)
├── funcoes.py      # Funções auxiliares de tratamento
├── resultados.txt  # Relatório gerado após execução
├── README.md       # Documentação
└── data/
├── olist_products_dataset.csv
└── olist_orders_dataset.csv
