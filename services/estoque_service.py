from database.banco import get_connection
from database.models import Produto
from datetime import datetime
from typing import List

class EstoqueService:
    @staticmethod
    def listar_produtos(id_usuario: int, pesquisa: str = "", categoria: str = "") -> List[Produto]:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM Produtos WHERE id_usuario = ?"
        params = [id_usuario]
        
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
    def obter_produto(produto_id: int, id_usuario: int) -> Produto:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Produtos WHERE id=? AND id_usuario=?", (produto_id, id_usuario))
        row = cursor.fetchone()
        conn.close()
        return Produto(**dict(row)) if row else None

    @staticmethod
    def buscar_por_codigo_barras(codigo_barras: str, id_usuario: int) -> Produto:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Produtos WHERE codigo_barras=? AND id_usuario=?", (codigo_barras, id_usuario))
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
                    unidade=?, local=?, observacoes=?, codigo_barras=?
                WHERE id=? AND id_usuario=?
            ''', (produto.nome, produto.categoria, produto.quantidade, 
                  produto.quantidade_minima, produto.unidade, produto.local, 
                  produto.observacoes, getattr(produto, 'codigo_barras', ''), produto.id, produto.id_usuario))
        else:
            cursor.execute('''
                INSERT INTO Produtos (id_usuario, nome, categoria, quantidade, quantidade_minima, unidade, local, observacoes, data_cadastro, codigo_barras)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (produto.id_usuario, produto.nome, produto.categoria, produto.quantidade, 
                  produto.quantidade_minima, produto.unidade, produto.local, 
                  produto.observacoes, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), getattr(produto, 'codigo_barras', '')))
            produto.id = cursor.lastrowid
            
        conn.commit()
        conn.close()
        return produto

    @staticmethod
    def excluir_produto(produto_id: int, id_usuario: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ItensCompra WHERE id_produto IN (SELECT id FROM Produtos WHERE id=? AND id_usuario=?)", (produto_id, id_usuario))
        cursor.execute("DELETE FROM ListaCompras WHERE id_produto=? AND id_usuario=?", (produto_id, id_usuario))
        cursor.execute("DELETE FROM Produtos WHERE id=? AND id_usuario=?", (produto_id, id_usuario))
        conn.commit()
        conn.close()
        
    @staticmethod
    def obter_categorias(id_usuario: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT categoria FROM Produtos WHERE categoria != '' AND id_usuario = ? ORDER BY categoria", (id_usuario,))
        rows = cursor.fetchall()
        conn.close()
        return [row['categoria'] for row in rows]
