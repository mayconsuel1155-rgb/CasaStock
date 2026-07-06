import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'casastock.db')

def upgrade():
    if not os.path.exists(DB_PATH):
        print("Database does not exist, nothing to upgrade.")
        return
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("ALTER TABLE Usuarios ADD COLUMN role TEXT DEFAULT 'cliente'")
        # Força o admin atual a ser superadmin
        cursor.execute("UPDATE Usuarios SET role = 'superadmin' WHERE username = 'admin'")
    except Exception as e:
        print("Usuarios role column already exists or error:", e)

    try:
        cursor.execute("ALTER TABLE Produtos ADD COLUMN id_usuario INTEGER DEFAULT 1")
    except Exception as e:
        print("Produtos id_usuario column already exists or error:", e)
        
    try:
        cursor.execute("ALTER TABLE Compras ADD COLUMN id_usuario INTEGER DEFAULT 1")
    except Exception as e:
        print("Compras id_usuario column already exists or error:", e)
        
    try:
        cursor.execute("ALTER TABLE ListaCompras ADD COLUMN id_usuario INTEGER DEFAULT 1")
    except Exception as e:
        print("ListaCompras id_usuario column already exists or error:", e)

    conn.commit()
    conn.close()
    print("Database upgrade completed successfully.")

if __name__ == "__main__":
    upgrade()
