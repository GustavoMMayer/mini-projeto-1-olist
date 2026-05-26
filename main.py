import sys

sys.stdout.reconfigure(encoding='utf-8')
from funcoes import carregar_csv
from funcoes import gerar_resumo_inicial
from funcoes import tratar_produtos
from funcoes import tratar_pedidos
from funcoes import gerar_resumo_final
from funcoes import gerar_grafico
from funcoes import montar_relatorio
from funcoes import exibir_display
from funcoes import salvar_relatorio



def main():

    print("=" * 60)
    print("SISTEMA DE TRATAMENTO DE DADOS - OLIST")
    print("PIPELINE PARA MACHINE LEARNING")
    print("=" * 60)

    print("\nCarregando arquivos...\n")

    # ======================================================
    # LEITURA / CARREGAMENTO DOS DADOS
    # ======================================================

    produtos = carregar_csv(
        "data/olist_products_dataset.csv"
    )

    pedidos = carregar_csv(
        "data/olist_orders_dataset.csv"
    )

    print("Arquivos carregados com sucesso.\n")

    # ======================================================
    # RESUMO INICIAL
    # ======================================================

    resumo_inicial = gerar_resumo_inicial(
        produtos
    )

    # ======================================================
    # TRATAMENTO DOS DADOS
    # ======================================================

    produtos_tratados = tratar_produtos(
        produtos
    )

    # ======================================================
    # REGRAS DE NEGÓCIO
    # ======================================================

    pedidos_tratados = tratar_pedidos(
        pedidos
    )

    # ======================================================
    # RESUMO FINAL
    # ======================================================

    resumo_final = gerar_resumo_final(
        produtos_tratados
    )
 
    # ======================================================
    # GRÁFICOS
    # ======================================================

    grafico_categorias = gerar_grafico(
        "CATEGORIAS VAZIAS",
        resumo_inicial["categorias_vazias"],
        0
    )

    grafico_dimensoes = gerar_grafico(
        "DIMENSÕES VAZIAS",
        resumo_inicial["dimensoes_vazias"],
        0
    )

    # ======================================================
    # RELATÓRIO
    # ======================================================

    relatorio = montar_relatorio(
        resumo_inicial,
        resumo_final,
        pedidos_tratados,
        grafico_categorias,
        grafico_dimensoes
    )

    # ======================================================
    # DISPLAY
    # ======================================================

    exibir_display(relatorio)

    # ======================================================
    # SALVAR TXT
    # ======================================================

    salvar_relatorio(relatorio)

    print("\nRelatório salvo em resultados.txt")

    print("\nPipeline executado com sucesso.")

  


if __name__ == "__main__":
    main()