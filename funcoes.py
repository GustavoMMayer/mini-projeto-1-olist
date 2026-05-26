import csv
import re
from datetime import datetime


# ==========================================================
# CARREGAMENTO DOS CSV
# ==========================================================

def carregar_csv(caminho):

    dados = []

    with open(caminho, encoding="utf-8") as arquivo:

        leitor = csv.DictReader(arquivo)

        for linha in leitor:

            dados.append(linha)

    return dados


# ==========================================================
# LIMPEZA DE STRINGS
# ==========================================================

def limpar_categoria(categoria):

    if categoria == "" or categoria is None:

        return "sem categoria"

    categoria = categoria.strip().lower()

    categoria = re.sub(
        r'[^a-z0-9\s]',
        '',
        categoria
    )

    return categoria


# ==========================================================
# CONVERSÃO DE DATAS
# ==========================================================

def converter_data(data_string):

    if data_string == "":

        return ""

    try:

        data_obj = datetime.strptime(
            data_string,
            "%Y-%m-%d %H:%M:%S"
        )

        return data_obj.strftime(
            "%d/%m/%Y"
        )

    except:

        return "data inválida"


# ==========================================================
# RESUMO INICIAL
# ==========================================================

def gerar_resumo_inicial(produtos):

    total = 0

    categorias_vazias = 0

    dimensoes_vazias = 0

    campos_dimensoes = [
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm"
    ]

    for produto in produtos:

        total += 1

        # Categoria vazia
        if produto["product_category_name"] == "":

            categorias_vazias += 1

        # Dimensões vazias
        for campo in campos_dimensoes:

            if produto[campo] == "":

                dimensoes_vazias += 1

    return {
        "total": total,
        "categorias_vazias":
            categorias_vazias,
        "dimensoes_vazias":
            dimensoes_vazias
    }


# ==========================================================
# MÉDIAS DAS DIMENSÕES
# ==========================================================

def calcular_medias(produtos):

    campos = [
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm"
    ]

    medias = {}

    for campo in campos:

        soma = 0

        contador = 0

        for produto in produtos:

            valor = produto[campo]

            if valor != "":

                soma += float(valor)

                contador += 1

        if contador > 0:

            medias[campo] = soma / contador

        else:

            medias[campo] = 0

    return medias


# ==========================================================
# TRATAMENTO DE PRODUTOS
# ==========================================================

def tratar_produtos(produtos):

    categorias_corrigidas = 0

    dimensoes_corrigidas = 0

    medias = calcular_medias(produtos)

    campos_dimensoes = [
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm"
    ]

    for produto in produtos:

        # ==============================================
        # LIMPEZA DE STRINGS
        # ==============================================

        categoria_original = (
            produto["product_category_name"]
        )

        categoria_limpa = limpar_categoria(
            categoria_original
        )

        if categoria_original == "":

            categorias_corrigidas += 1

        produto["product_category_name"] = (
            categoria_limpa
        )

        # ==============================================
        # TRATAMENTO DE NULOS
        # ==============================================

        for campo in campos_dimensoes:

            if produto[campo] == "":

                """
                Escolha técnica:
                Utilizar média evita perda
                de registros importantes
                para futuras análises e
                modelos de Machine Learning.
                """

                produto[campo] = round(
                    medias[campo],
                    2
                )

                dimensoes_corrigidas += 1

    return {
        "produtos": produtos,
        "categorias_corrigidas":
            categorias_corrigidas,
        "dimensoes_corrigidas":
            dimensoes_corrigidas
    }


# ==========================================================
# REGRAS DE NEGÓCIO
# ==========================================================

def tratar_pedidos(pedidos):

    total_pedidos = 0

    pedidos_cancelados = 0

    entregas_vazias_nao_canceladas = 0

    for pedido in pedidos:

        total_pedidos += 1

        status = pedido["order_status"]

        entrega = (
            pedido[
                "order_delivered_customer_date"
            ]
        )

        # ==============================================
        # REGRA DE NEGÓCIO
        # ==============================================

        if entrega == "":

            if status == "canceled":

                pedidos_cancelados += 1

            else:

                entregas_vazias_nao_canceladas += 1

        # ==============================================
        # DATETIME
        # ==============================================

        pedido["order_approved_at"] = (
            converter_data(
                pedido["order_approved_at"]
            )
        )

    return {
        "total_pedidos":
            total_pedidos,

        "pedidos_cancelados":
            pedidos_cancelados,

        "entregas_vazias_nao_canceladas":
            entregas_vazias_nao_canceladas
    }


# ==========================================================
# RESUMO FINAL
# ==========================================================

def gerar_resumo_final(resultado):

    return {

        "categorias_corrigidas":
            resultado[
                "categorias_corrigidas"
            ],

        "dimensoes_corrigidas":
            resultado[
                "dimensoes_corrigidas"
            ]
    }


# ==========================================================
# GRÁFICOS ASCII
# ==========================================================

def gerar_grafico(
    titulo,
    antes,
    depois
):

    barra_antes = "#" * int(antes / 10)

    barra_depois = "#" * int(depois / 10)

    return f"""
{titulo}

ANTES : {antes}
{barra_antes}

DEPOIS: {depois}
{barra_depois}
"""

# ==========================================================
# VISUALIZAÇÃO DE TABELA
# ==========================================================

def visualizar_csv_tabela(dados, limite=100):
    """
    Exibe os dados em formato de tabela.
    """
    if not dados:
        print("Nenhum dado encontrado para exibição.")
        return

    # Pega nomes das colunas
    colunas = list(dados[0].keys())

    # ======================================================
    # CALCULA LARGURA DAS COLUNAS
    # ======================================================
    larguras = {}

    for coluna in colunas:
        maior = len(coluna)

        for linha in dados[:limite]:
            # Usar get previne erros se a chave não existir na linha
            tamanho = len(str(linha.get(coluna, ""))) 

            if tamanho > maior:
                maior = tamanho

        larguras[coluna] = maior + 2

    # ======================================================
    # LINHA SUPERIOR
    # ======================================================
    linha_divisoria = "+"

    for coluna in colunas:
        linha_divisoria += "-" * larguras[coluna] + "+"

    print(linha_divisoria)

    # ======================================================
    # CABEÇALHO
    # ======================================================
    cabecalho = "|"

    for coluna in colunas:
        cabecalho += (
            " "
            + coluna.ljust(larguras[coluna] - 1)
            + "|"
        )

    print(cabecalho)
    print(linha_divisoria)

    # ======================================================
    # DADOS
    # ======================================================
    for registro in dados[:limite]:
        linha_dados = "|"

        for coluna in colunas:
            valor = str(registro.get(coluna, ""))

            linha_dados += (
                " "
                + valor.ljust(larguras[coluna] - 1)
                + "|"
            )

        print(linha_dados)

    print(linha_divisoria)
    
    # Ajustei para exibir a quantidade real caso o CSV tenha menos linhas que o limite
    quantidade_exibida = len(dados[:limite])
    print(f"\nExibindo {quantidade_exibida} registros.")


# ==========================================================
# RELATÓRIO
# ==========================================================

def montar_relatorio(
    resumo_inicial,
    resumo_final,
    pedidos,
    grafico_categorias,
    grafico_dimensoes
):

    return f"""
============================================================
RELATÓRIO INICIAL
============================================================

Total de produtos:
{resumo_inicial['total']}

Categorias vazias:
{resumo_inicial['categorias_vazias']}

Dimensões vazias:
{resumo_inicial['dimensoes_vazias']}


============================================================
RELATÓRIO FINAL
============================================================

Categorias corrigidas:
{resumo_final['categorias_corrigidas']}

Dimensões corrigidas:
{resumo_final['dimensoes_corrigidas']}


============================================================
REGRAS DE NEGÓCIO
============================================================

Total de pedidos:
{pedidos['total_pedidos']}

Pedidos cancelados:
{pedidos['pedidos_cancelados']}

Pedidos sem entrega mas NÃO cancelados:
{pedidos['entregas_vazias_nao_canceladas']}


============================================================
GRÁFICOS COMPARATIVOS
============================================================

{grafico_categorias}

{grafico_dimensoes}


============================================================
STATUS FINAL
============================================================

Base sanitizada com sucesso.
"""


# ==========================================================
# DISPLAY
# ==========================================================

def exibir_display(relatorio):

    largura = 60

    print("\n" + "=" * largura)

    print(
        "PAINEL DE SANITIZAÇÃO DE DADOS"
        .center(largura)
    )

    print("=" * largura)

    print(relatorio)

    print("=" * largura)


# ==========================================================
# SALVAR RELATÓRIO
# ==========================================================

def salvar_relatorio(relatorio):

    with open(
        "resultados.txt",
        "w",
        encoding="utf-8"
    ) as arquivo:

        arquivo.write(relatorio)