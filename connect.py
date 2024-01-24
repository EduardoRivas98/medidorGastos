import mysql.connector

config = {
  'user': 'root',
  'password': '',
  'host': 'localhost',
  'database': 'ingresos',
  'raise_on_warnings': True
}

cnx = mysql.connector.connect(**config)
