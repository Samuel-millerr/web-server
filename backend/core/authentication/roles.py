"""
Estrutura de quais roles/tipos de usuario vão estar presentes dentro do sistema
"""

from abc import ABC, abstractmethod

class BaseUser(ABC):
    def __init__(self, id_usuario, nome, role):
        super().__init__()
        self.id_usuario = id_usuario
        self.nome = nome
        self.role = role

    @abstractmethod 
    def pode_adicionar(self):
        return self.role in ["administrador", "comum"]
    
    def pode_editar(self):
        return self.role in ["administrador", "comum"]
    

class Usuario(BaseUser):
    def __init__(self, id_usuario, nome, role):
        self.id_usuario = id_usuario
        self.nome = nome
        self.role = role 

    def pode_adicionar(self):
        pass

    def pode_editar(self):
        pass

class Administrador(BaseUser):
    def __init__(self, id_usuario, nome, role):
        super().__init__(id_usuario, nome, role)

    def pode_adicionar(self):
        pass

    def pode_editar(self):
        pass

    def pode_deletar(self):
        return True
    
def criar_usuario(dados):
    if dados["role"] == "administrador":
        return Administrador(dados["id_user"], dados["nome"], dados["role"])
    return Usuario(dados["id_user"], dados["nome"], dados["role"])

