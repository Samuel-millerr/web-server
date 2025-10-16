from core.settings import DB_CONNECTION

cursor = DB_CONNECTION.cursor()

cursor.execute("USE webflix;")
cursor.execute("SELECT * FROM usuarios;")
users = cursor.fetchall()
print(users)


cursor.close()
DB_CONNECTION.close()