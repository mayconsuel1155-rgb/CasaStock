from database.banco import get_connection
from database.models import Produto
from datetime import datetime
from typing import List

class EstoqueService:
    @staticmethod
    def listar_produtos(pesquisa: str = "", categoria: str = "") -> List[Produto]:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM Produtos WHERE 1=1"
        params = []
        
        if pesquisa:
            query += " AND (nome LIKE ? OR observacoes LIKE ?)"
            params.extend([f"%{pesquisa}%", f"%{pesquisa}%"])
            
        if categoria:
            query += " AND categoria = ?"
            params.append(categoria)
            
        query += " ORDER BY nome ASC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [Produto(**dict(row)) for row in rows]
        
    @staticmethod
    def obter_produto(produto_id: int) -> Produto:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Produtos WHERE id=?", (produto_id,))
        row = cursor.fetchone()
        conn.close()
        return Produto(**dict(row)) if row else None
        
    @staticmethod
    def salvar_produto(produto: Produto) -> Produto:
        conn = get_connection()
        cursor = conn.cursor()
        
        if produto.quantidade < 0:
            produto.quantidade = 0 # RN001: Não permitir quantidade negativa
            
        if produto.id:
            cursor.execute('''
                UPDATE Produtos SET 
                    nome=?, categoria=?, quantidade=?, quantidade_minima=?, 
                    unidade=?, local=?, observacoes=?
                WHERE id=?
            ''', (produto.nome, produto.categoria, produto.quantidade, 
                  produto.quantidade_minima, produto.unidade, produto.local, 
                  produto.observacoes, produto.id))
        else:
            cursor.execute('''
                INSERT INTO Produtos (nome, categoria, quantidade, quantidade_minima, unidade, local, observacoes, data_cadastro)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (produto.nome, produto.categoria, produto.quantidade, 
                  produto.quantidade_minima, produto.unidade, produto.local, 
                  produto.observacoes, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            produto.id = cursor.lastrowid
            
        conn.commit()
        conn.close()
        return produto

    @staticmethod
    def excluir_produto(produto_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ItensCompra WHERE id_produto=?", (produto_id,))
        cursor.execute("DELETE FROM ListaCompras WHERE id_produto=?", (produto_id,))
        cursor.execute("DELETE FROM Produtos WHERE id=?", (produto_id,))
        conn.commit()
        conn.close()
        
    @staticmethod
    def obter_categorias():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT categoria FROM Produtos WHERE categoria != '' ORDER BY categoria")
        rows = cursor.fetchall()
        conn.close()
        return [row['categoria'] for row in rows]
