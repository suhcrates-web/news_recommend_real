import mysql.connector

config = {
    'user' : 'root',
    'password': 'Seoseoseo7!',
    'host':'localhost',
    # 'database':'shit',
    'port':'3306'
}

db = mysql.connector.connect(**config)
cursor = db.cursor()

