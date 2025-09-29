import os
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

"""A definição do handler personalizado é criado através de uma classe que herda o 'SimpleHTTPRequestHandler'.
O objetivo receber e processar as respostas de um evento específico que ocorre dentro do servidor."""

usuarios_cadastrados = [{"id": "1", "user": "samuel", "password": "1234"}]

class MyHandle(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            f = open(os.path.join(path, './templates/index.html'), encoding='utf-8')
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f.read().encode('utf-8'))
            f.close()
            return None
        except FileNotFoundError:
            pass 
        return super().list_directory(path)

    def carregar_pagina(self, caminho):
        try:
            with open(os.path.join(os.getcwd(), caminho), 'r', encoding='utf-8') as arquivo:
                content = arquivo.read()
                self.send_response(200)
                self.send_header("content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
        except FileNotFoundError:
            self.send_error(404, f"Arquivo não {caminho} encontrado")

    def retornar_post_formulario(self):
        """ Função usada para ler e retornar o corpo do POST já decodificado."""
        content_length = int(self.headers['Content-length'])
        body = self.rfile.read(content_length).decode('utf-8')
        form_data = parse_qs(body)
        return form_data

    def do_GET(self):
        try:    
            """ Esse bloco de código tem como objetivo 'renderizar' todas as páginas dentro do servidor, cada caminho indicado dentro das condições 
            é um caminho possível de ser feito dentro do site. Todas as páginas estão utilizando de uma função em comum para abrir as páginas. """

            if self.path == "/login":
                self.carregar_pagina('./templates/login.html')   
            elif self.path == "/cadastro":
                self.carregar_pagina('./templates/cadastro.html')
            elif self.path == "/filmes_cadastro":
                self.carregar_pagina('./templates/filmes_cadastro.html')
            elif self.path == "/filmes_listagem":
                self.carregar_pagina('./templates/filmes_listagem.html')
            else:
                return super().do_GET()
        except FileNotFoundError:
            self.send_error(404, "File Not Found")
    
    def do_POST(self):
        """ Os dois metódos POST abaixo funcionam da mesma forma, recebendo informações dos formulário
        e realizando questões como autenticação e liberação. """
        if self.path == '/send_login':
            content_lenght = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_lenght).decode('utf-8')
            data = json.loads(body)

            user_form = data.get('user')
            password_form = data.get('password')

            arquivo = './data/users.json'
            auth: bool = False

            if os.path.exists(arquivo):
                with open('./data/users.json', "r", encoding='utf-8') as f:
                    users = json.load(f)
                
                for user in users:
                    if user['user'] == user_form and user['password'] == password_form:
                        auth = True
                        
                if auth:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"message": "ok"}).encode("utf-8"))
                else:
                    self.send_response(403)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"message": "Usuário ou senha inválidos"}).encode("utf-8"))
            else:
                print({"error": "problema ao encontrar o arquivo de usuários"})


        elif self.path == '/send_cadastro':
            content_lenght = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_lenght).decode('utf-8')
            data = json.loads(body) 

            print(data.get('password'))
            print(data.get('confirmPassword'))

            user_form = data.get('user')
            password_form = data.get('password')
            confirm_password_form = data.get('confirmPassword')

            
            if password_form == confirm_password_form:
                user = {"user": user_form, "password": password_form}
                usuarios_cadastrados.append(user)

                with open('./data/users.json', 'w', encoding='utf-8') as arquivo_json:
                    json.dump(usuarios_cadastrados, arquivo_json, indent=4, ensure_ascii=False)
                        

                self.carregar_pagina('./login.html')
                message = "<script>alert('Usuário cadastrado com sucesso!')</script>"
                self.wfile.write(message.encode("utf-8"))

        elif self.path == "/send_cadastro_filmes":
            """ O cadastro de filmes se consiste em uma lógica bem simples, os dados
            são recolhidos do formulário e depois passados para um dinionário em python """
            form_data = self.retornar_post_formulario()

            title = form_data.get('title', [""])[0]
            actors = form_data.get('actor', [""])[0]
            director = form_data.get('director', [""])[0]
            year = form_data.get('year', [""])[0]
            genre = form_data.get('genre', [""])[0]
            producer = form_data.get('producer', [""])[0]
            summary = form_data.get('summary', [""])[0]

            film = {
                "title": title,
                "actors": actors,
                "director": director,
                "year": year,
                "genre": genre,
                "producer": producer,
                "summary": summary
            }
            
            i = len(filmes_cadastrados)
            filmes_cadastrados[i+1] = film

            self.carregar_pagina('./filmes_listagem.html')
            self.gerar_arquivo_js(filmes_cadastrados)  # Ativa a função de criação do arquivo js, caso tenha filmes cadastrados, eles apareceram na tela
            message = "<script>alert('Filme cadastrado com sucesso!')</script>"
            self.wfile.write(message.encode("utf-8"))
            
 
def main():
    """Função para iniciar o servidor, recebe a porta que deve ser utilizada, ou seja , o endereço do servidor, e o handle personalidado criado na classe
    acima.
    """
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, MyHandle)
    print(f"Servidor rodando na porta http://localhost:{server_address[1]}") # Os colchetes no server_address é utilizado para pegar a porta indicada no código
    httpd.serve_forever()

main()