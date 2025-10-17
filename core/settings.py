import mysql.connector
from mysql.connector import Error

""" Aquoi é tentado realizar a conexão com o banco de dados, caso seja inválida é retornado uma mensagem """
try: 
    DB_CONNECTION = mysql.connector.connect(
        host="localhost",
        user="root",
        password="senai",
    )
    if DB_CONNECTION.is_connected():
        print("Banco de dados conectado com sucesso!")
except Error as e:
    print(f"Erro ao conectar com o banco de dados: {e}")

# Variáveis de Ambiente
SQL_CREATE_TABLES = 'database/scripts/CREATE_TABLES_WEBFLIX.sql'
SQL_INSERT_DATA = 'database/scripts/INSERT_DATA_WEBFLIX.sql'
