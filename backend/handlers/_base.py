from http.server import SimpleHTTPRequestHandler, HTTPServer
import json as json

class BaseHandler(SimpleHTTPRequestHandler):
    def send_json_response(self, data, status=200):
        """Envia resposta JSON padrão"""
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
        
def main():
    from core.settings import BASE_SERVER
    """Função para iniciar o servidor, recebe a porta que deve ser utilizada, ou seja , o endereço do servidor, e o handle personalidado criado na classe acima. """
    server_address = ("", 8000)
    httpd = HTTPServer(BASE_SERVER, BaseHandler)
    print(f"Servidor rodando na porta {BASE_SERVER}")
    httpd.serve_forever()