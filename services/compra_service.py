from database.banco import get_connection
from database.models import Compra, ItemCompra, ListaCompra, Produto
from datetime import datetime
from typing import List, Dict, Any

class CompraService:
    
    # --- LISTA DE COMPRAS ---
    
    @staticmethod
    def listar_itens_lista(id_usuario: int) -> List[Dict[str, Any]]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT l.id as lista_id, l.quantidade, l.status, p.* 
            FROM ListaCompras l
            JOIN Produtos p ON l.id_produto = p.id
            WHERE l.id_usuario = ?
            ORDER BY p.nome ASC
        ''', (id_usuario,))
        rows = cursor.fetchall()
        conn.close()
        
        resultado = []
        for row in rows:
            d = dict(row)
            # Separa os dados de lista e produto
            item = {
                'lista_id': d['lista_id'],
                'quantidade_lista': d['quantidade'],
                'status': d['status'],
                'produto': Produto(
                    id=d['id'], id_usuario=id_usuario, nome=d['nome'], categoria=d['categoria'], 
                    quantidade=d['quantidade'], quantidade_minima=d['quantidade_minima'],
                    unidade=d['unidade'], local=d['local'], observacoes=d['observacoes'], 
                    data_cadastro=d['data_cadastro']
                )
            }
            resultado.append(item)
        return resultado

    @staticmethod
    def adicionar_a_lista(id_usuario: int, id_produto: int, quantidade: float = 1.0):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO ListaCompras (id_usuario, id_produto, quantidade) VALUES (?, ?, ?)", (id_usuario, id_produto, quantidade))
            conn.commit()
        except Exception:
            # Já existe, então não faz nada ou apenas atualiza quantidade
            pass
        finally:
            conn.close()
            
    @staticmethod
    def remover_da_lista(lista_id: int, id_usuario: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ListaCompras WHERE id=? AND id_usuario=?", (lista_id, id_usuario))
        conn.commit()
        conn.close()

    # --- COMPRAS ---

    @staticmethod
    def registrar_compra(id_usuario: int, mercado: str, forma_pagamento: str, observacoes: str, itens: List[Dict[str, Any]]):
        # itens: [{'id_produto': int, 'quantidade': float, 'valor_unitario': float}]
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # Calcular valor total e criar compra
            valor_total_compra = sum(item['quantidade'] * item['valor_unitario'] for item in itens)
            data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute('''
                INSERT INTO Compras (id_usuario, data, mercado, valor_total, forma_pagamento, observacoes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (id_usuario, data_atual, mercado, valor_total_compra, forma_pagamento, observacoes))
            compra_id = cursor.lastrowid
            
            # Adicionar itens, atualizar estoque, e remover da lista
            for item in itens:
                valor_total_item = item['quantidade'] * item['valor_unitario']
                
                # Inserir item da compra
                cursor.execute('''
                    INSERT INTO ItensCompra (id_compra, id_produto, quantidade, valor_unitario, valor_total)
                    VALUES (?, ?, ?, ?, ?)
                ''', (compra_id, item['id_produto'], item['quantidade'], item['valor_unitario'], valor_total_item))
                
                # RN003: Atualizar estoque automaticamente
                cursor.execute("UPDATE Produtos SET quantidade = quantidade + ? WHERE id = ? AND id_usuario = ?", (item['quantidade'], item['id_produto'], id_usuario))
                
                # RN006: Remover da lista de compras se existir
                cursor.execute("DELETE FROM ListaCompras WHERE id_produto = ? AND id_usuario = ?", (item['id_produto'], id_usuario))
                
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Erro ao registrar compra: {e}")
            return False
        finally:
            conn.close()
