import mysql.connector
from mysql.connector import Error

from contextlib import contextmanager
from typing import Generator

""" CAMINHOS DOS SCRIPTS SQL """
SQL_CREATE_TABLES = 'database/scripts/CREATE_TABLES_WEBFLIX.sql'
SQL_INSERT_DATA = 'database/scripts/INSERT_DATA_WEBFLIX.sql'

class DatabaseService:
    """
    Classe com todos os métodos relacionados ao banco de dados:
    - Inicialização
    - Criação de tabelas
    - Criação de sessões (para CRUD)

    Todas as funções do DatabaseService são estáticas, feitas atráves do decorator
    @staticmethod, isso por que não necessitam de receber informações self, 
    já que não se comunicam com nenhum atributo ou metódo da classe;
    """
    @staticmethod 
    def get_connection():
        """
        Função essencial para pegar os dados do banco de dados, como 
        host, user, password, database. Utilizado somente para encontrar e permitir a conexão 
        com o servidor mysql;
        """
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="webflix"
            )
            print("[DB] Conexão com o banco realizada com sucesso.")
            return conn
        
        except Error as e:
            print(f"[DB ERROR] Erro de conexão com a raiz do banco - Função do DatabaseService.get_connection \n{e}")
            return None
    
    @staticmethod
    def init_db(): 
        """ 
        Função para apenas testar a conexão com o banco, caso a conexão não 
        consiga ser feita, será retornado uma resposta negativa sobre a conexão 
        """       
        conn = DatabaseService.get_connection()

        if conn.is_connected():
            print("[DB] Conexão com o banco testada com sucesso.")
            conn.close()
            return True
        else:
            print("[DB] Erro na conexão - Função do DatabaseService.get_init().")
            return False   
        
    @staticmethod
    @contextmanager
    def session() -> Generator:
        """ 
        Aqui é definido um pequeno processo para criar um cursor/session dentro do banco,
        ele será repetido em todos os momentos que o sistema necessitar enviar, buscar, editar ou
        deletar dados do banco;

        O decorator contextmanager é utilizado para referenciar ao Python que esta é uma função
        generator. Em suma, um generator é uma função que prove algo e tem responsabilidades/separações 
        específicas dentro da própria função — isso é feito geralmente de maneira cronológica, sendo 
        antes do 'yield' e depois do 'yield'. Além de fazer essa separação de responsabilidades, o 'yield'
        também serve como return na função.
        """

        conn = DatabaseService.get_connection()
        if not conn or not conn.is_connected():
            raise ConnectionError("[DB ERROR] Erro na criação da sessão.")

        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"[DB ERROR] Erro na criação do cursor/session - Função do DatabaseService.session(). \n{e}")
        finally:
            cursor.close()
            conn.close()