""" 
Handler para permitir a criação, atualização, adição e remoção de filmes do banco de dados. 
"""
from core.handlers.base_handler import BaseHandler
from core.settings import config

from database.database_service import DatabaseService as db

status = config.status

class MovieHandler(BaseHandler):
    @staticmethod
    def get_movie_by_id(id_movie: int):
        with db.session() as session:
            session.execute("USE webflix;")
            session.execute("SELECT * FROM filme WHERE id_filme = %s;", (id_movie,))
            return session.fetchone()

    def post_movie(self, handler):
        body = handler.parse_json_body()

        with db.session() as session:
            session.execute("USE webflix;")
            session.execute("SELECT * from webflix.filme WHERE filme.titulo = %s;", (body["titulo"],))
            result = session.fetchone()

        if not result:
            with db.session() as session:
                session.execute("USE webflix;")
                
                query = """
                    INSERT INTO webflix.filme(titulo, orcamento, tempo_duracao, ano_publicacao, poster) 
                    VALUES
                        (%s, %s, %s, %s, %s);
                """
                session.execute(query, (body["titulo"], body["orcamento"], body["tempo_duracao"], body["ano_publicacao"], body["poster"],))

            handler.send_json_response({"message": "movie successfully created."}, status["HTTP_201_CREATED"])
        else:
            handler.send_json_response({"message": "movie alredy exist!"}, status["HTTP_409_CONFLICT"])


    def get_movies(self, handler):
        with db.session() as session:
            session.execute("USE webflix;")
            session.execute("SELECT * FROM webflix.filme;")
            result = session.fetchall()

        movies_json = []
        for res in result:
            movie = {
                "id": int(res[0]),
                "titulo": str(res[1]),
                "orcamento": int(res[2]),
                "tempo_duracao": str(res[3]),
                "ano_publicacao": str(res[4]),
                "poster": str(res[5])
            }

            movies_json.append(movie)

        handler.send_json_response(movies_json, status["HTTP_200_OK"])
        
    def get_movie(self, handler, id_movie: int):
        result = MovieHandler.get_movie_by_id(id_movie)
        
        if result:
            movie_json = {
                "id": int(result[0]),
                "titulo": str(result[1]),
                "orcamento": int(result[2]),
                "tempo_duracao": str(result[3]),
                "ano_publicacao": str(result[4]),
                "poster": str(result[5])
            }
            
            handler.send_json_response(movie_json, status["HTTP_200_OK"])
        else:
            handler.send_json_response({"message": "movie not found."}, status["HTTP_404_NOT_FOUND"])

    def put_movie(self, handler, id_movie: int):
        body = handler.parse_json_body()

        result = MovieHandler.get_movie_by_id(id_movie)

        if result:
            with db.session() as session:
                session.execute("USE webflix;")
                query = """
                    UPDATE webflix.filme 
                    SET 
                        titulo = %s, 
                        orcamento = %s,
                        tempo_duracao = %s, 
                        ano_publicacao = %s, 
                        poster = %s
                    WHERE 
                        id_filme = %s;
                """

                session.execute(query, (body["titulo"], body["orcamento"], body["tempo_duracao"], body["ano_publicacao"], body["poster"], id_movie,))

            handler.send_json_response(body, status["HTTP_200_OK"])
        else:
            handler.send_json_response({"message": "movie not found."}, status["HTTP_404_NOT_FOUND"])

    def delete_movie(self, handler, id_movie: int):
        result = MovieHandler.get_movie_by_id(id_movie)

        if result:
            with db.session() as session:
                session.execute("USE webflix;")
                session.execute("DELETE FROM webflix.filme WHERE filme.id_filme = %s;", (id_movie,))  

            handler.send_json_response({}, status["HTTP_204_NO_CONTENT"])
        else:
            handler.send_json_response({"message": "movie not found."}, status["HTTP_404_NOT_FOUND"])

    def filter_movies(self, handler, query):
        query = query.split("=")[1]
        query = f"%{query}%"
        with db.session() as session:
            session.execute("USE webflix;")
            session.execute("SELECT * FROM webflix.filme WHERE LOWER(titulo) LIKE %s;", (query,))
            result = session.fetchall()

        movies_json = []
        for res in result:
            movie = {
                "id": int(res[0]),
                "titulo": str(res[1]),
                "orcamento": int(res[2]),
                "tempo_duracao": str(res[3]),
                "ano_publicacao": str(res[4]),
                "poster": str(res[5])
            }

            movies_json.append(movie)
        
        handler.send_json_response(movies_json, status["HTTP_200_OK"])