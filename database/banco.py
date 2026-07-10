import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'casastock.db')
DATABASE_URL = os.getenv("DATABASE_URL")

class PostgresCursorWrapper:
    def __init__(self, cursor):
        self.cursor = cursor
    
    def execute(self, query, params=None):
        # Convert ? to %s for Postgres
        query = query.replace('?', '%s')
        # Convert AUTOINCREMENT to SERIAL
        query = query.replace('AUTOINCREMENT', 'SERIAL')
        
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
            
    def fetchone(self):
        return self.cursor.fetchone()
        
    def fetchall(self):
        return self.cursor.fetchall()
        
    @property
    def lastrowid(self):
        self.cursor.execute("SELECT LASTVAL()")
        return self.cursor.fetchone()[0]

class PostgresConnectionWrapper:
    def __init__(self, conn):
        self.conn = conn
    
    def cursor(self):
        import psycopg2.extras
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        return PostgresCursorWrapper(cur)
        
    def commit(self):
        self.conn.commit()
        
    def rollback(self):
        self.conn.rollback()
        
    def close(self):
        self.conn.close()

def get_connection():
    if DATABASE_URL:
        import psycopg2
        conn = psycopg2.connect(DATABASE_URL)
        return PostgresConnectionWrapper(conn)
    else:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        # Enable foreign keys support in SQLite
        conn.execute("PRAGMA foreign_keys = 1")
        return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tabela Produtos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER NOT NULL,
        nome TEXT NOT NULL,
        categoria TEXT,
        quantidade REAL NOT NULL DEFAULT 0,
        quantidade_minima REAL NOT NULL DEFAULT 0,
        unidade TEXT,
        local TEXT,
        observacoes TEXT,
        data_cadastro TEXT NOT NULL,
        codigo_barras TEXT
    )
    ''')
    
    # Migração para adicionar codigo_barras caso não exista (bancos antigos)
    try:
        cursor.execute("SELECT codigo_barras FROM Produtos LIMIT 1")
    except Exception:
        # Se der erro, a coluna não existe (no sqlite ou postgres)
        try:
            # Precisa fazer rollback no postgres em caso de erro na transação
            if DATABASE_URL:
                conn.rollback()
            cursor.execute("ALTER TABLE Produtos ADD COLUMN codigo_barras TEXT")
        except Exception as e:
            print(f"Erro ao adicionar coluna codigo_barras: {e}")
    
    # Tabela Compras
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Compras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER NOT NULL,
        data TEXT NOT NULL,
        mercado TEXT,
        valor_total REAL NOT NULL DEFAULT 0,
        forma_pagamento TEXT,
        observacoes TEXT
    )
    ''')
    
    # Tabela ItensCompra
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ItensCompra (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_compra INTEGER NOT NULL,
        id_produto INTEGER NOT NULL,
        quantidade REAL NOT NULL,
        valor_unitario REAL NOT NULL,
        valor_total REAL NOT NULL,
        FOREIGN KEY (id_compra) REFERENCES Compras(id) ON DELETE CASCADE,
        FOREIGN KEY (id_produto) REFERENCES Produtos(id)
    )
    ''')
    
    # Tabela ListaCompras
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ListaCompras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER NOT NULL,
        id_produto INTEGER NOT NULL,
        quantidade REAL NOT NULL DEFAULT 1,
        status TEXT NOT NULL DEFAULT 'pendente',
        FOREIGN KEY (id_produto) REFERENCES Produtos(id) ON DELETE CASCADE
    )
    ''')
    
    # Tabela Usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'cliente',
        data_cadastro TEXT NOT NULL
    )
    ''')
    
    # Inserir usuário admin padrão se não houver usuários
    cursor.execute("SELECT COUNT(*) as count FROM Usuarios")
    if cursor.fetchone()['count'] == 0:
        import datetime
        data_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Senha padrão: admin (sha256)
        hash_admin = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"
        cursor.execute("INSERT INTO Usuarios (username, password_hash, role, data_cadastro) VALUES (?, ?, ?, ?)",
                       ("admin", hash_admin, "superadmin", data_atual))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
