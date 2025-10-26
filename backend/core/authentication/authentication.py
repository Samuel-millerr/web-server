"""
Funções gerais do jwt para permitir a autenticação e validação de qual usuário está sendo utilizado
"""

import jwt as jwt
from datetime import datetime, timedelta

SECRET_KEY = "senha_super_secreta"

class Authentication:
    @staticmethod
    def gerar_token(usuario):
        payload = {
            "id_user": usuario["id"],
            "role": usuario["role"],
            "exp": datetime.utcnow() + timedelta(hours=1)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


    @staticmethod
    def verificar_token(token):
        try:
            dados = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return dados
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None