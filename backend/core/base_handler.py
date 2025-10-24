""" 
Raiz do handler do servidor, tem como objetivo passar funções específicas que poderam ser usadas em todos os endpoints, 
como envio de resposta e conversão do body da requisição.

É aqui onde o SimplesHTTPHandler é chamado e tem sua criação principal, todos os outros metódos e questões do servidor 
vão se basear no presente nesse arquivo.
"""

from http.server import SimpleHTTPRequestHandler
import json as json

class BaseHandler(SimpleHTTPRequestHandler):
    def send_json_response(self, data, status=200):
        """ Envia resposta JSON padrão """
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
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
        
    def send_error_response(self,  message: str, status = 500):
        """ Envia uma resposta padrão negativa """
        self.send_response(status)
        self.send_error(code=status, message=message)