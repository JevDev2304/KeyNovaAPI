import random
from fastapi import HTTPException, status
import mysql.connector

from mysql.connector import pooling, Error

config = {'user': 'JUANFER',
          'host': 'project1.mysql.database.azure.com',
          'password': 'Duko0505',
          'database': 'keynova',
          'port': 3306,  # Puerto predeterminado de MySQL
          'raise_on_warnings': True}  # Para que se generen excepciones en caso de advertencias


class ConnectionDB:
    conn = None  # Mantén la conexión abierta en la instancia

    def __init__(self):
        dbconfig = {
            "user": 'JUANFER',
            "password": 'Duko0505',
            "host": 'project1.mysql.database.azure.com',
            "port": '3306',
            "database": 'keynova'
        }

        pool = pooling.MySQLConnectionPool(pool_name="mypool",
                                           pool_size=5,
                                           **dbconfig)

        try:
            connection = pool.get_connection()
            ConnectionDB.conn = connection
        except Error as e:
            print("Error while connecting to MySQL", e)
            raise HTTPException(status_code=500, detail=e.msg)

    def executeSQL(self, consulta_sql, variables_adicionales=None):

        cursor = conn.cursor()
        try:

            # Agregar la propiedad y obtener el id de la propiedad recién agregada
            cursor.execute(consulta_sql, variables_adicionales)

            if consulta_sql.strip().upper().startswith("INSERT") or consulta_sql.strip().upper().startswith(
                    "UPDATE") or consulta_sql.strip().upper().startswith(
                "DELETE") or consulta_sql.strip().upper().startswith("CREATE"):
                return None

            return cursor.fetchone()

        finally:
            cursor.close()
