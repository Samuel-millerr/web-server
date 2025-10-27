""" 
Raiz do handler do servidor, tem como objetivo passar funções específicas que poderam ser usadas em todos os endpoints, 
como envio de resposta e conversão do body da requisição.

É aqui onde o SimplesHTTPHandler é chamado e tem sua criação principal, todos os outros metódos e questões do servidor 
vão se basear no presente nesse arquivo.
"""

from http.server import SimpleHTTPRequestHandler
import json as json
import os as os # Mudar biblioteca
from urllib.parse import urlsplit, unquote

class BaseHandler(SimpleHTTPRequestHandler):
    """ Parte para respostas e comunicação com o client desde json a erros ou conversão de body das requisições"""
    def send_json_response(self, data, status=200):
        """ Envia resposta JSON padrão """
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))
    
    def send_token(self, data,token, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Authorization", f"Bearer {token}")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))
        
    def parse_json_body(self):
        """ Lê e decodifica JSON recebido no body pelo """
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return None
    
    def parse_headers(self):
        auth_header = self.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header.split(" ")[1]
        return None

    """ Função para permitir maior manipulação sobre a url requerida """
    def parse_path(self, url):
        split = urlsplit(url)
        path_parts = split.path.strip("/").split("/") # Coleta a url sem espaço nas laterais e com separação entre as "/"
        result = {"path": "/" + "/".join(path_parts)}

        if path_parts and path_parts[-1].isdigit():
            result["id"] = int(path_parts[-1])
        else:
            result["id"] = False

        result["query"] = unquote(split.query.strip().lower())

        return result
    
    """ Função simples somente para listar o diretorio da página da API """
    def list_api_directory(self):
        """ Função utilizada para renderizar a página da API """
        path = os.path.join(os.getcwd(), r"core\template.html")
        try:
            with open(path, "r", encoding="utf-8") as arquivo:
                content = arquivo.read()
                self.send_response(200)
                self.send_header("content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
        except FileNotFoundError:
            self.send_error(404, f"Arquivo não {path} encontrado")
        