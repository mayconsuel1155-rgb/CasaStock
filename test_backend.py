import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.banco import init_db
from database.models import Produto
from services.estoque_service import EstoqueService
from services.compra_service import CompraService
from services.historico_service import HistoricoService

def testar():
    print("Iniciando testes do backend CasaStock...")
    init_db()

    # 1. Cadastro de Produto
    p1 = Produto(
        id=None,
        nome="Arroz 5kg Teste",
        categoria="Alimentos",
        quantidade=0.0,
        quantidade_minima=1.0,
        unidade="pct",
        local="Despensa",
        observacoes="Teste unitario",
        data_cadastro=""
    )
    p_salvo = EstoqueService.salvar_produto(p1)
    print(f"Produto salvo com ID: {p_salvo.id}")

    # 2. Listagem de Produtos
    produtos = EstoqueService.listar_produtos()
    print(f"Total de produtos no estoque: {len(produtos)}")

    # 3. Adicionar à Lista de Compras
    CompraService.adicionar_a_lista(p_salvo.id, quantidade=2.0)
    itens_lista = CompraService.listar_itens_lista()
    print(f"Itens na lista de compras: {len(itens_lista)}")

    # 4. Registrar Compra
    itens_compra = [{
        'id_produto': p_salvo.id,
        'quantidade': 2.0,
        'valor_unitario': 25.50
    }]
    sucesso = CompraService.registrar_compra(
        mercado="Mercadinho Teste",
        forma_pagamento="Dinheiro",
        observacoes="",
        itens=itens_compra
    )
    print(f"Compra registrada com sucesso: {sucesso}")

    # 5. Verificar Estoque Atualizado
    p_atualizado = EstoqueService.obter_produto(p_salvo.id)
    print(f"Estoque atual do produto após compra: {p_atualizado.quantidade} (Esperado: 2.0)")

    # 6. Verificar Histórico
    compras = HistoricoService.listar_compras()
    print(f"Total de compras no histórico: {len(compras)}")

    # 7. Dashboard
    resumo = HistoricoService.obter_resumo_dashboard()
    print("Resumo do Dashboard:")
    print(resumo)

    # 8. Limpar testes
    EstoqueService.excluir_produto(p_salvo.id)
    print("Produto de teste excluído.")
    
    print("Todos os testes concluídos com sucesso!")

if __name__ == "__main__":
    testar()
