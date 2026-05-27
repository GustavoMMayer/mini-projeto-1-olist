import sys


from funcoes import carregar_csv, salvar_csv
from funcoes import gerar_resumo_inicial
from funcoes import tratar_produtos
from funcoes import tratar_pedidos
from funcoes import gerar_resumo_final
from funcoes import montar_relatorio
from funcoes import exibir_display
from funcoes import salvar_relatorio

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

    produtos = carregar_csv(
        products_path
    )

    pedidos = carregar_csv(
        orders_path
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

    # Escolha técnica: nulos substituídos pela média da coluna.
    # A remoção do registro foi descartada pois geraria perda de dados
    # que comprometeria a representatividade do dataset em modelos de ML.


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
    # RELATÓRIO
    # ======================================================

    relatorio = montar_relatorio(
        resumo_inicial,
        resumo_final,
        pedidos_tratados
        
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

    # ======================================================
    # SALVAR BASES CORRIGIDAS
    # ======================================================

    salvar_csv(
        produscts_tratados_path,
        produtos_tratados["produtos"]
    )

    salvar_csv(
        orders_tratados_path,
        pedidos
    )

    print("\nBases corrigidas salvas na pasta data/")

    print("\nPipeline executado com sucesso.")

  


if __name__ == "__main__":
    main()