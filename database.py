from core.settings import DB_CONNECTION, SQL_CREATE_TABLES, SQL_INSERT_DATA
print("Conexão com o banco de dados sendo realizada...")
cursor = DB_CONNECTION.cursor()

cursor.execute('DROP DATABASE IF EXISTS webflix;')
cursor.execute('CREATE DATABASE webflix;')
cursor.execute("USE webflix;")

print("Criando as tabelas do banco de dados...")
with open(SQL_CREATE_TABLES, 'r', encoding='utf-8') as f:
    sql_script = f.read()

for command in sql_script.split(';'):
    command = command.strip()
    if command:
        cursor.execute(command)

print("Inserindo as informações no banco de dados..")
with open(SQL_INSERT_DATA, 'r', encoding='utf-8') as f:
    sql_script = f.read()

for command in sql_script.split(';'):
    command =command.strip()
    if command:
        cursor.execute(command)

cursor.close()

DB_CONNECTION.commit()

print("Conexão e criação do o banco de dados completa!")
