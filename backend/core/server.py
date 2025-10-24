"""
Aqui funciona como uma "rota" de como o servidor deve reagir, ele vefica qual metódo o frontend realizou e o envia 
atráves da instancia do router para permitir a funcionamento da lógica daquela requisição.
"""

from http.server import HTTPServer
from core.settings import config

from core.base_handler import BaseHandler
from core.routers.router import Router

class AppHandler(BaseHandler):
    router = Router()
    
    def do_POST(self):
        self.router.handler_post(self)

    def do_GET(self):
        self.router.handler_get(self)
    
    def do_PUT(self):
        self.router.handler_put(self)

    def do_DELETE(self):
        self.router.handler_delete(self)

def main():
    """Função para iniciar o servidor, recebe a porta que deve ser utilizada, ou seja , o endereço do servidor, e o handle personalidado criado na classe acima. """
    httpd = HTTPServer((config.HOST, config.PORT), AppHandler)
    print(f"Servidor rodando na porta {config.BASE_SERVER}")
    httpd.serve_forever()