""" Handler de autenticação, contém rotas como de login e cadastro"""
from core.base_handler import BaseHandler

class AuthHandler(BaseHandler):
    def login(self):
        self.send_json_response({"messagem": "api rodando com sucesso"})

