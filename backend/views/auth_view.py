""" Handler de autenticação, contém rotas como de login e cadastro"""
from core.handlers.base_handler import BaseHandler
from core.authentication.authentication import Authentication as auth
from core.settings import config

from database.database_service import DatabaseService as db

status = config.status
class AuthHandler(BaseHandler):
    def login(self, handler):
        body = handler.parse_json_body()

        with db.session() as session:
            session.execute("USE webflix;")
            session.execute("SELECT * FROM usuario WHERE LOWER(usuario.nome) = %s", (body["nome"].lower(),))
            result = session.fetchone()

        user = {
            "id_usuario": result[0],
            "nome": result[1],
            "email": result[2],
            "senha": result[3],
            "role": result[4]
        }
        
        if not result:
            return self.send_json_response({"error": "User not found"}, status=status["HTTP_401_UNAUTHORIZED"])

        if not auth.verify_password(body["senha"], user["senha"]):
            return self.send_json_response({"error": "User or password wrongs"}, status=status["HTTP_401_UNAUTHORIZED"])
        
        token = auth.generate_token(user)

        handler.send_token({"token": f"{token}"}, token)
        
    def sing_up(self, handler):
        body = handler.parse_json_body()

        with db.session() as session:
            session.execute("USE webflix;")
            session.execute("SELECT * FROM usuario WHERE LOWER(usuario.nome) = %s", (body["nome"].lower(),))
            result = session.fetchone()

        if not result:
            with db.session() as session:
                session.execute("USE webflix;")
                query = """
                INSERT INTO usuario(nome, email, senha, tipo_usuario)
                VALUES
                    (%s, %s, %s, %s);
                """
                session.execute(query, (body["nome"], body["email"], body["senha"], body["tipo_usuario"],))
        
            handler.send_json_response({"message": "user successfully created"}, status["HTTP_201_CREATED"])
        else:
            handler.send_json_response({"message": "user alredy exist"}, status["HTTP_409_CONFLICT"])
        
        return {"message": "user successfully created"}
    