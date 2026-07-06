from database.banco import get_connection
from database.models import Compra, ItemCompra, Produto
from typing import List, Dict, Any

class HistoricoService:
    @staticmethod
    def listar_compras(limite: int = 50) -> List[Compra]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Compras ORDER BY id DESC LIMIT ?", (limite,))
        rows = cursor.fetchall()
        conn.close()
        return [Compra(**dict(row)) for row in rows]
        
    @staticmethod
    def obter_detalhes_compra(compra_id: int) -> List[Dict[str, Any]]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT ic.*, p.nome, p.unidade 
            FROM ItensCompra ic
            JOIN Produtos p ON ic.id_produto = p.id
            WHERE ic.id_compra = ?
        ''', (compra_id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]

    @staticmethod
    def obter_resumo_dashboard() -> Dict[str, Any]:
        conn = get_connection()
        cursor = conn.cursor()
        
        resumo = {
            'total_produtos': 0,
            'produtos_em_falta': 0,
            'produtos_estoque_baixo': 0,
            'itens_lista_compras': 0,
            'valor_gasto_mes': 0.0
        }
        
        # Produtos em falta (qtde == 0)
        cursor.execute("SELECT COUNT(*) as c FROM Produtos WHERE quantidade = 0")
        resumo['produtos_em_falta'] = cursor.fetchone()['c']
        
        # Total produtos
        cursor.execute("SELECT COUNT(*) as c FROM Produtos")
        resumo['total_produtos'] = cursor.fetchone()['c']
        
        # Produtos estoque baixo (qtde > 0 e qtde <= minima)
        cursor.execute("SELECT COUNT(*) as c FROM Produtos WHERE quantidade > 0 AND quantidade <= quantidade_minima")
        resumo['produtos_estoque_baixo'] = cursor.fetchone()['c']
        
        # Itens lista de compras
        cursor.execute("SELECT COUNT(*) as c FROM ListaCompras")
        resumo['itens_lista_compras'] = cursor.fetchone()['c']
        
        # Valor gasto no mês atual
        from datetime import datetime
        mes_atual = datetime.now().strftime("%Y-%m")
        cursor.execute("SELECT SUM(valor_total) as s FROM Compras WHERE data LIKE ?", (f"{mes_atual}%",))
        s = cursor.fetchone()['s']
        resumo['valor_gasto_mes'] = s if s else 0.0
        
        conn.close()
        return resumo

    @staticmethod
    def zerar_historico_mes():
        from datetime import datetime
        mes_atual = datetime.now().strftime("%Y-%m")
        conn = get_connection()
        cursor = conn.cursor()
        
        # Delete items first to maintain referential integrity
        cursor.execute("DELETE FROM ItensCompra WHERE id_compra IN (SELECT id FROM Compras WHERE data LIKE ?)", (f"{mes_atual}%",))
        # Delete purchases
        cursor.execute("DELETE FROM Compras WHERE data LIKE ?", (f"{mes_atual}%",))
        
        conn.commit()
        conn.close()
