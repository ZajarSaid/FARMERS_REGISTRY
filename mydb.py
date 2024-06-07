import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'zajar@gmail9977'
)

cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE Farmersdb")

print('Deal done!')

