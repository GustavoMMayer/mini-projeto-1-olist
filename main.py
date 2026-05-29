import sys


import funcoes as fc

sys.stdout.reconfigure(encoding='utf-8')

def main():
    products_path = "data/olist_products_dataset.csv"
    orders_path = "data/olist_orders_dataset.csv"
    produscts_tratados_path = "data/olist_products_dataset_limpo.csv"
    orders_tratados_path = "data/olist_orders_dataset_limpo.csv"


    print("=" * 60)
    print("SISTEMA DE TRATAMENTO DE DADOS - OLIST")
    print("PIPELINE PARA MACHINE LEARNING")
    print("=" * 60)

    print("\nCarregando arquivos...\n")

    # ======================================================
    # LEITURA / CARREGAMENTO DOS DADOS
    # ======================================================

    produtos = fc.carregar_csv(
        products_path
    )

    pedidos = fc.carregar_csv(
        orders_path
    )

    print("Arquivos carregados com sucesso.\n")

    # ======================================================
    # RESUMO INICIAL
    # ======================================================

    resumo_inicial = fc.gerar_resumo_inicial(
        produtos
    )

    # ======================================================
    # TRATAMENTO DOS DADOS
    # ======================================================

    # Escolha técnica: nulos substituídos pela média da coluna.
    # A remoção do registro foi descartada pois geraria perda de dados
    # que comprometeria a representatividade do dataset em modelos de ML.


    produtos_tratados = fc.tratar_produtos(
        produtos
    )

    # ======================================================
    # REGRAS DE NEGÓCIO
    # ======================================================

    pedidos_tratados = fc.tratar_pedidos(
        pedidos
    )

    # ======================================================
    # RESUMO FINAL
    # ======================================================

    resumo_final = fc.gerar_resumo_final(
        produtos_tratados
    )
 

    # ======================================================
    # RELATÓRIO
    # ======================================================

    relatorio = fc.montar_relatorio(
        resumo_inicial,
        resumo_final,
        pedidos_tratados
        
    )

    # ======================================================
    # DISPLAY
    # ======================================================

    fc.exibir_display(relatorio)

    # ======================================================
    # SALVAR TXT
    # ======================================================

    fc.salvar_relatorio(relatorio)

    print("\nRelatório salvo em resultados.txt")

    # ======================================================
    # SALVAR BASES CORRIGIDAS
    # ======================================================

    fc.salvar_csv(
        produscts_tratados_path,
        produtos_tratados["produtos"]
    )

    fc.salvar_csv(
        orders_tratados_path,
        pedidos_tratados["pedidos"]
    )

    print("\nBases corrigidas salvas na pasta data/")

    print("\nPipeline executado com sucesso.")

  


if __name__ == "__main__":
    main()