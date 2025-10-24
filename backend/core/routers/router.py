from handlers.auth_handler import AuthHandler
from handlers.movies_handler import MovieHandler

class Router:
    def handler_post(self, handler):
        server_path = handler.path
        if  server_path.startswith('/api/movies'):
            MovieHandler.post_movie(self, handler)

    def handler_get(self, handler):
        server_path = handler.path 
        if server_path == '/api':
            """ Fazer uma página basica para api """
            pass
        elif server_path == '/api/movies':
            MovieHandler.get_movies(self, handler)
        elif server_path.startswith('/api/movies'):
            parts_path = server_path.split('/')
            id_movie = parts_path[3]
            MovieHandler.get_movie(self, handler, id_movie)

    def handler_put(self, handler):
        server_path = handler.path 
        pass 

    def handler_delete(self, handler):
        server_path = handler.path 

        if server_path.startswith('/api/movies'):
            parts_path = server_path.split('/')
            id_movie = parts_path[3]
            MovieHandler.delete_movie(self, handler, id_movie)
    
