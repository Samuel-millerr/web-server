""" 
Handler para permitir a criação, atualização, adição e remoção de filmes do banco de dados. 
"""
from core.base_handler import BaseHandler
from core.settings import config

from database.database_service import DatabaseService as db

status = config.status

class MovieHandler(BaseHandler):
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
                        (%s, %s, %s, %s, %s, %s);
                """
                session.execute(query, (body["titulo"], body["orcamento"], body["tempo_duracao"], body["tempo_duracao"], body["ano_publicacao"], body["poster"]))
                result = session.fetchone()

            print(result)
        else:
            handler.send_json_response({'message': 'movie alredy exist!'}, status['HTTP_409_CONFLICT'])


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

        handler.send_json_response(movies_json, status['HTTP_200_OK'])
        
    def get_movie(self, handler, id_movie):
        with db.session() as session:
            session.execute("USE webflix")
            session.execute("SELECT * FROM webflix.filme WHERE filme.id_filme = %s;", (id_movie,))
            result = session.fetchone()
        
        if result:
            movie_json = {
                "id": int(result[0]),
                "titulo": str(result[1]),
                "orcamento": int(result[2]),
                "tempo_duracao": str(result[3]),
                "ano_publicacao": str(result[4]),
                "poster": str(result[5])
            }
            
            handler.send_json_response(movie_json, status['HTTP_200_OK'])
        else:
            handler.send_json_response({'message': 'movie not found!'}, status['HTTP_404_NOT_FOUND'])

    def delete_movie(self, handler, id_movie):
        with db.session() as session:
            session.execute("USE webflix")
            session.execute("SELECT * FROM webflix.filme WHERE filme.id_filme = %s", (id_movie,))  
            result = session.fetchone()

        if result:
            with db.session() as session:
                session.execute("USE webflix")
                session.execute("DELETE FROM webflix.filme WHERE filme.id_filme = %s", (id_movie,))  

            handler.send_json_response({'message': 'movie successfully deleted'}, status['HTTP_204_NO_CONTENT'])
        else:
            handler.send_json_response({'message': 'movie not found!'}, status['HTTP_404_NOT_FOUND'])