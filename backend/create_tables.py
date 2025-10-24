""" 
Ao rodar esse arquivo o banco é deletado e os é definido o default de filme, os scripts estão dentro da pasta database.
"""

from database.database_service import DatabaseService as db
from database.database_service import SQL_CREATE_TABLES, SQL_INSERT_DATA

from time import sleep

def create_tables():
    with db.session() as session:
        print("Conexão com o banco de dados sendo realizada...")
        sleep(1)

        session.execute('DROP DATABASE IF EXISTS webflix;')
        session.execute('CREATE DATABASE webflix;')
        session.execute('USE webflix;')

        print("Criando as tabelas do banco de dados...")
        sleep(2)
        with open(SQL_CREATE_TABLES, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        for command in sql_script.split(';'):
            command = command.strip()
            if command:
                session.execute(command)

        print("Inserindo as informações no banco de dados...")
        sleep(2)
        with open(SQL_INSERT_DATA, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        for command in sql_script.split(';'):
            command =command.strip()
            if command:
                session.execute(command)

        print("Conexão e criação do o banco de dados completa!")
        sleep(1)

create_tables()