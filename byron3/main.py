from flask import Flask, jsonify, request
from psycopg import connect
import psycopg
from psycopg.rows import dict_row

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
'''@app.get('/')
def home():
    #Probar la cadena de conexion con un selecc * from catalogo
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    cursor.execute("SELECT * FROM compania")
    row = cursor.fetchall()
    
    #Cerrar el cursor y la conexion
    cursor.close()
    conn.close()
    #Retornar un jsonfy
    return jsonify(row)'''
'''@app.route('/')
def home():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM compania")
        
        # Obtener los nombres de las columnas
        column_names = [desc[0] for desc in cursor.description]
        
        # Obtener los datos y convertirlos en una lista de diccionarios
        rows = cursor.fetchall()
        result = [dict(zip(column_names, row)) for row in rows]
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        cursor.close()
        conn.close()'''

@app.get("/")
def home():
    try:
        # Conexión a la base de datos
        with get_connection() as conn:
            with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
                # Ejecutar la consulta
                cur.execute("SELECT * FROM compania")                
                # Obtener todos los registros como diccionarios
                rows = cur.fetchall()                
                return jsonify(rows)  # Retorna la lista de diccionarios como JSON
    except Exception as e:
        return jsonify({"error": str(e)})

# Ruta para obtener un registro por ID
@app.get("/compania/<int:id>")
def get_by_id(id):
    try:
        # Conexión a la base de datos
        with get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                # Ejecutar la consulta con un parámetro
                cur.execute("SELECT * FROM compania WHERE id = %s", (id,))
                # Obtener el registro
                row = cur.fetchone()
                if row:
                    return jsonify(row)  # Retorna el registro como JSON
                else:
                    return jsonify({"error": "Registro no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})
    
# Ruta para insertar un nuevo registro
@app.post("/compania")
def create_compania():
    try:
        # Obtener datos del cuerpo de la solicitud (formato JSON)
        data = request.get_json()
        nombre = data.get("nombre")
        direccion = data.get("direccion")

        # Validar los datos
        if not nombre or not direccion:
            return jsonify({"error": "El nombre y la dirección son obligatorios"}), 400

        # Conexión a la base de datos
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Insertar el nuevo registro
                cur.execute(
                    "INSERT INTO compania (nombre, direccion) VALUES (%s, %s) RETURNING id",
                    (nombre, direccion)
                )
                # Obtener el ID del registro insertado
                new_id = cur.fetchone()[0]
                conn.commit()  # Confirmar la transacción

                return jsonify({"id": new_id, "nombre": nombre, "direccion": direccion}), 201
    except Exception as e:
        return jsonify({"error": str(e)})

# Ruta para actualizar un registro
@app.put("/compania/<int:id>")
def update_compania(id):
    try:
        # Obtener datos del cuerpo de la solicitud (formato JSON)
        data = request.get_json()
        nombre = data.get("nombre")
        direccion = data.get("direccion")

        # Validar los datos
        if not nombre or not direccion:
            return jsonify({"error": "El nombre y la dirección son obligatorios"}), 400

        # Conexión a la base de datos
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Ejecutar la actualización
                cur.execute(
                    "UPDATE compania SET nombre = %s, direccion = %s WHERE id = %s",
                    (nombre, direccion, id)
                )
                # Confirmar la transacción
                conn.commit()

                # Verificar si se actualizó alguna fila
                if cur.rowcount == 0:
                    return jsonify({"error": "Registro no encontrado"}), 404

                return jsonify({"id": id, "nombre": nombre, "direccion": direccion})
    except Exception as e:
        return jsonify({"error": str(e)})

# Ruta para eliminar un registro
@app.delete("/compania/<int:id>")
def delete_compania(id):
    try:
        # Conexión a la base de datos
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Ejecutar la eliminación
                cur.execute("DELETE FROM compania WHERE id = %s", (id,))
                conn.commit()

                # Verificar si se eliminó alguna fila
                if cur.rowcount == 0:
                    return jsonify({"error": "Registro no encontrado"}), 404

                return jsonify({"message": f"Registro con id {id} eliminado exitosamente"})
    except Exception as e:
        return jsonify({"error": str(e)})   


#Habilitar debug
if __name__ == '__main__':
    app.run(debug=True)