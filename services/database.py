import mysql.connector
SQL_CREATE_TABLES = 'services/scripts/CREATE_TABLES_WEBFLIX.sql'

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="senai",
)

cursor = conexao.cursor()

cursor.execute('DROP DATABASE IF EXISTS webflix;')
cursor.execute('CREATE DATABASE webflix;')
cursor.execute('USE webflix;')


with open(SQL_CREATE_TABLES, 'r', encoding='utf-8') as f:
    sql_script = f.read()

for command in sql_script.split(';'):
    command = command.strip()
    if command:
        cursor.execute(command)


cursor.close()
conexao.close()
