from handlers._base import BaseHandler

class AuthHandler(BaseHandler):
    def do_GET(self):
        if self.path == '/login':
            self.login()
        elif self.path == 'sing_up':
            self.sing_up()
