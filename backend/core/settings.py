class Config:
    HOST = 'localhost'
    PORT = 8000

config = Config

BASE_SERVER = ("http://{config.HOST}", {config.PORT})