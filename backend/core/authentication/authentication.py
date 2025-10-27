"""
Funções gerais do jwt para permitir a autenticação e validação de qual usuário está sendo utilizado
"""

import jwt as jwt
from datetime import datetime, timedelta

SECRET_KEY = "senha_super_secreta"

class Authentication:
    @staticmethod
    def generate_token(user: dict):
        payload = {
            "id_usuario": user["id_usuario"],
            "role": user["role"],
            "exp": datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token

    @staticmethod
    def verify_token(token: str):
        try:
            dados = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return dados
        except jwt.ExpiredSignatureError:
            print("[AUTH] Token Expirado")
            return None
        except jwt.InvalidTokenError:
            print("[AUTH] Token Inválido")
            return None
        
    @staticmethod
    def verify_password(password_form: str, password_db: str):
        password_form = password_form.strip()
        password_db = password_db.strip()

        if password_form == password_db: return True
        return False