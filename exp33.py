from database import config
import mysql.connector
db = mysql.connector.connect(**config)
cursor = db.cursor()

cursor.execute("""
show databases;
""")
print(cursor.fetchall())
