from database.banco import get_connection
from database.models import Compra, ItemCompra, ListaCompra, Produto
from datetime import datetime
from typing import List, Dict, Any

class CompraService:
    
    # --- LISTA DE COMPRAS ---
    
    @staticmethod
    def listar_itens_lista() -> List[Dict[str, Any]]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT l.id as lista_id, l.quantidade, l.status, p.* 
            FROM ListaCompras l
            JOIN Produtos p ON l.id_produto = p.id
            ORDER BY p.nome ASC
        ''')
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
                    id=d['id'], nome=d['nome'], categoria=d['categoria'], 
                    quantidade=d['quantidade'], quantidade_minima=d['quantidade_minima'],
                    unidade=d['unidade'], local=d['local'], observacoes=d['observacoes'], 
                    data_cadastro=d['data_cadastro']
                )
            }
            resultado.append(item)
        return resultado

    @staticmethod
    def adicionar_a_lista(id_produto: int, quantidade: float = 1.0):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO ListaCompras (id_produto, quantidade) VALUES (?, ?)", (id_produto, quantidade))
            conn.commit()
        except Exception:
            # Já existe, então não faz nada ou apenas atualiza quantidade
            pass
        finally:
            conn.close()
            
    @staticmethod
    def remover_da_lista(lista_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ListaCompras WHERE id=?", (lista_id,))
        conn.commit()
        conn.close()

    # --- COMPRAS ---

    @staticmethod
    def registrar_compra(mercado: str, forma_pagamento: str, observacoes: str, itens: List[Dict[str, Any]]):
        # itens: [{'id_produto': int, 'quantidade': float, 'valor_unitario': float}]
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # Calcular valor total e criar compra
            valor_total_compra = sum(item['quantidade'] * item['valor_unitario'] for item in itens)
            data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute('''
                INSERT INTO Compras (data, mercado, valor_total, forma_pagamento, observacoes)
                VALUES (?, ?, ?, ?, ?)
            ''', (data_atual, mercado, valor_total_compra, forma_pagamento, observacoes))
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
                cursor.execute("UPDATE Produtos SET quantidade = quantidade + ? WHERE id = ?", (item['quantidade'], item['id_produto']))
                
                # RN006: Remover da lista de compras se existir
                cursor.execute("DELETE FROM ListaCompras WHERE id_produto = ?", (item['id_produto'],))
                
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Erro ao registrar compra: {e}")
            return False
        finally:
            conn.close()
