from http.server import SimpleHTTPRequestHandler, HTTPServer

class BaseHandler(SimpleHTTPRequestHandler):
    pass

def main():
    """Função para iniciar o servidor, recebe a porta que deve ser utilizada, ou seja , o endereço do servidor, e o handle personalidado criado na classe acima. """
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, BaseHandler)
    print(f"Servidor rodando na porta http://localhost:{server_address[1]}") # Os colchetes no server_address é utilizado para pegar a porta indicada no código
    httpd.serve_forever()