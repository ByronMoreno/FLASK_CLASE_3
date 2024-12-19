from flask import Flask
from psycopg import connect

#Instanciar flask
app = Flask(__name__)

#Definir las variables para la cadena de conexion
host = 'localhost'
port = 5432
dbname = 'postgres'
username = 'postgres'
password = None

#Construir la cadena de conexio a la base de datos
def get_connection():
    conn = connect(host=host, port=port,dbname=dbname, user=username, password=password)
    return conn

#Get simple
@app.get('/')
def home():
    #Probar la cadena de conexion con un selecc * from catalogo
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM catalogo")
    print(cursor.fetchall())
    return "Prueba de base de datos OK"

#Habilitar debug
if __name__ == '__main__':
    app.run(debug=True)
    
    