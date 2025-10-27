"""
Essa função é o centro da autenticação por jwt.
Ela cria um decorator que adiciona uma verificação de acesso antes da execução de uma função específica.

- permissao_necessaria(role_requerida): recebe a role exigida para executar a função (ex: @permissao_necessaria('administrador'))
- wrapper(func): recebe a função que será decorada (ex: deletar_filme())
- inner(*args, **kwargs): a função que é executada antes da função original, validando o token
  Os parâmetros *args e **kwargs permitem capturar todos os argumentos da função original
"""

from functools import wraps
from core.authentication.authentication import Authentication

def permission(role):
    def wrapper(func):
        @wraps(func)
        def inner(*args):
            token = args[3]
            dados = Authentication.verify_token(token)
            
            if not dados:
                print("[PERMISSION] Token inválido ou exirado")
                return {"erro": "Token inválido ou expirado"}, 401

            if dados["role"] != role:
                print("[PERMISSION] Acesso negado, role não permitida")
                return {"erro": "Acesso negado"}, 403
            
            return func(*args)
        return inner
    return wrapper