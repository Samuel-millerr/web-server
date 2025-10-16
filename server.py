import os
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer
from core.settings import DB_CONNECTION

"""A definição do handler personalizado é criado através de uma classe que herda o "SimpleHTTPRequestHandler".
O objetivo receber e processar as respostas de um evento específico que ocorre dentro do servidor."""

json_filmes_cadastrados = "./data/movies.json"
json_usuarios_cadastrados = "./data/users.json"

class MyHandle(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        """ Função utilizada para renderizar a primeira página """
        try:
            f = open(os.path.join(path, "./templates/index.html"), encoding="utf-8")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f.read().encode("utf-8"))
            f.close()
            return None
        except FileNotFoundError:
            self.send_error(404, "File Not Found")
        return super().list_directory(path)

    def load_movies(self):
        from core.settings import DB_CONNECTION

        cursor = DB_CONNECTION.cursor()

        cursor.execute("SELECT * FROM webflix.filme")

        result = cursor.fetchall()

        filmes_json = []
        for res in result:
            filme = {
                "id": int(res[0]),
                "titulo": str(res[1]),
                "orcamento": int(res[2]),
                "tempo_duracao": str(res[3]),
                "ano_publicacao": str(res[4]),
                "poster": str(res[5])
            }
            filmes_json.append(filme)
        
        return filmes_json
    
    def carregar_pagina(self, caminho):
        try:
            """ Função simples para reutilização de código, utilizada nos metódos GET para carregar a página """
            with open(os.path.join(os.getcwd(), caminho), "r", encoding="utf-8") as arquivo:
                content = arquivo.read()
                self.send_response(200)
                self.send_header("content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
        except FileNotFoundError:
            self.send_error(404, f"Arquivo não {caminho} encontrado")

    def do_GET(self):
        try:    
            """ Esse bloco de código tem como objetivo "renderizar" todas as páginas dentro do servidor, cada caminho indicado dentro das condições 
            é um caminho possível de ser feito dentro do site. Todas as páginas estão utilizando de uma função em comum para abrir as páginas. """

            if self.path == "/login":
                self.carregar_pagina("./templates/login.html")   
                self.load_movies()
            elif self.path == "/cadastro":
                self.carregar_pagina("./templates/cadastro.html")
            elif self.path == "/filmes_cadastro":
                self.carregar_pagina("./templates/filmes_cadastro.html")
            elif self.path == "/filmes_edicao":
                self.carregar_pagina('./templates/filmes_edicao.html')
            elif self.path == "/filmes_listagem":
                self.carregar_pagina("./templates/filmes_listagem.html")
            elif self.path == "/get_movies":
                try:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    data = self.load_movies()
                except (json.JSONDecodeError):
                    data = []
                    self.send_response(404)         

                self.wfile.write(json.dumps(data).encode("utf-8"))           
            else:
                super().do_GET()

        except FileNotFoundError:
            self.send_error(404, "File Not Found")
    
    def do_POST(self):
        """ Os dois metódos POST abaixo funcionam da mesma forma, recebendo informações dos formulário do java script e realizando questões como autenticação e liberação. """
        if self.path == "/send_login":
            """ Recebe a requisição do fetch do java script e armazena as informações na variável 'data' """
            content_lenght = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_lenght).decode("utf-8")
            data = json.loads(body)

            user_form = data.get("user")
            password_form = data.get("password")

            auth: bool = False
            
            cursor = DB_CONNECTION.cursor()

            if cursor:
                cursor.execute("USE webflix")
                cursor.execute("SELECT usuario, senha FROM usuarios")
                users = cursor.fetchall()

                for user in users:
                    if user[0] == user_form and user[1] == password_form:
                        auth = True
                        break

                cursor.close()
                        
                if auth:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"message": "ok"}).encode("utf-8"))
                else:
                    self.send_response(403)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"message": "usuário ou senha inválidos"}).encode("utf-8"))
            else:
                self.send_error(404, "File not found")

        elif self.path == "/send_cadastro":
            content_lenght = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_lenght).decode("utf-8")
            data = json.loads(body)

            user_form = data.get("user")
            password_form = data.get("password")
            confirm_password_form = data.get("confirmPassword")

            cursor = DB_CONNECTION.cursor()

            if cursor:
                if password_form == confirm_password_form:
                    valid_user = True
                    cursor.execute("USE webflix")
                    cursor.execute(f"INSERT INTO usuarios(usuario, senha) VALUES ('{user_form}', '{password_form}');")
                    cursor.close()
    
            if valid_user:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
            else:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()

        elif self.path == "/send_movie":
            content_lenght = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_lenght).decode("utf-8")
            data = json.loads(body)
            
            if os.path.exists(json_filmes_cadastrados):
                with open(json_filmes_cadastrados, "r", encoding="utf-8") as arquivo_json:
                    movie = json.load(arquivo_json)

                """ Pequena lógica para permitir a inserção de um novo filme no json """
                id_movie = len(movie) + 1
                data = {"id": id_movie, **data}
                movie.append(data)

                with open(json_filmes_cadastrados, "w", encoding="utf-8") as arquivo_json:
                    json.dump(movie, arquivo_json, indent=4, ensure_ascii=False)

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"message": "ok"}).encode("utf-8"))
            else:
                self.send_error(404, "File not found")
        else:
            super().do_GET()

    def do_PUT(self):
        path = self.path.split("/") # Busca os path parameters da requisição e os divide em uma lista, sendo o caminho em si e o id do filme
        if f"/{path[1]}" == "/update_movie": # Verfica se o caminho corresponde ao de atualização de filmes
            content_lenght = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_lenght).decode("utf-8")
            data = json.loads(body)

            movie_id = path[2] # Pega o id do filme de acordo com a lista gerada pelo split do caminho
            try:
                with open(json_filmes_cadastrados, "r", encoding="utf-8") as arquivo_json:
                    filmes = json.load(arquivo_json)

                """ For para verificar qual filme corresponde ao filme editado """
                for filme in filmes:
                    if filme['id'] == int(movie_id):
                        filme.update(data)

                with open(json_filmes_cadastrados, "w", encoding="utf-8") as arquivo_json:
                    json.dump(filmes, arquivo_json, indent=4, ensure_ascii=False)

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(filme).encode("utf-8"))

            except (json.JSONDecodeError):
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"message": "erro ao ler o arquivo JSON."}).encode("utf-8"))
        else:
            super().do_GET()

    def do_DELETE(self): 
        url = self.path
        id_movie = url.split('/')[2]

        if url.split('/')[1] == "delete_movie":
            try:
                with open(json_filmes_cadastrados, "r", encoding="utf-8") as arquivo_json:
                    filmes = json.load(arquivo_json)
                
                filmes_novos = [filme for filme in filmes if filme['id'] != int(id_movie)]

                with open(json_filmes_cadastrados, "w", encoding="utf-8") as arquivo_json:
                    json.dump(filmes_novos, arquivo_json, indent=4, ensure_ascii=False)

                if len(filmes) > len(filmes_novos):
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"message": "filme deletado com sucesso"}).encode("utf-8"))
            except (json.JSONDecodeError):
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"message": "erro ao ler o arquivo JSON."}).encode("utf-8"))
            
def main():
    """Função para iniciar o servidor, recebe a porta que deve ser utilizada, ou seja , o endereço do servidor, e o handle personalidado criado na classe acima. """
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, MyHandle)
    print(f"Servidor rodando na porta http://localhost:{server_address[1]}") # Os colchetes no server_address é utilizado para pegar a porta indicada no código
    httpd.serve_forever()

main()