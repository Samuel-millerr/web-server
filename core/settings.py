import mysql.connector

DB_CONNECTION = mysql.connector.connect(
    host="localhost",
    user="root",
    password="senai"
)

# Variáveis de Ambiente
SQL_CREATE_TABLES = 'database/scripts/CREATE_TABLES_WEBFLIX.sql'
SQL_INSERT_DATA = 'database/scripts/INSERT_DATA_WEBFLIX.sql'
