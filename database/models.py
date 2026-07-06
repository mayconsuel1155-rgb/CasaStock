from dataclasses import dataclass
from typing import Optional

@dataclass
class Produto:
    id: Optional[int]
    id_usuario: int
    nome: str
    categoria: str
    quantidade: float
    quantidade_minima: float
    unidade: str
    local: str
    observacoes: str
    data_cadastro: str

@dataclass
class Compra:
    id: Optional[int]
    id_usuario: int
    data: str
    mercado: str
    valor_total: float
    forma_pagamento: str
    observacoes: str

@dataclass
class ItemCompra:
    id: Optional[int]
    id_compra: int
    id_produto: int
    quantidade: float
    valor_unitario: float
    valor_total: float

@dataclass
class ListaCompra:
    id: Optional[int]
    id_usuario: int
    id_produto: int
    quantidade: float
    status: str

@dataclass
class Usuario:
    id: Optional[int]
    username: str
    password_hash: str
    role: str
    data_cadastro: str
