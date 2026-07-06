import hashlib
import datetime
from database.banco import get_connection
from database.models import Usuario

class AuthService:
    
    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    @staticmethod
    def login(username: str, password: str) -> dict:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM Usuarios WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            # Check if password matches
            if row['password_hash'] == AuthService._hash_password(password):
                return {"success": True, "id": row['id'], "role": row['role'], "username": row['username']}
        return {"success": False}

    @staticmethod
    def register(username: str, password: str) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM Usuarios WHERE username = ?", (username,))
        if cursor.fetchone():
            conn.close()
            return False # Usuário já existe
            
        data_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        password_hash = AuthService._hash_password(password)
        
        try:
            cursor.execute("INSERT INTO Usuarios (username, password_hash, data_cadastro) VALUES (?, ?, ?)",
                           (username, password_hash, data_atual))
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()

    @staticmethod
    def update_password(username: str, new_password: str) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        
        password_hash = AuthService._hash_password(new_password)
        
        try:
            cursor.execute("UPDATE Usuarios SET password_hash = ? WHERE username = ?", (password_hash, username))
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()
