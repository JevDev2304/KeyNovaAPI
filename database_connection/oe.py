import time
import mysql.connector
from mysql.connector.errors import Error
from fastapi import HTTPException
class DB:
    def get_mysql_connection(self):
        try:
            connection = mysql.connector.connect(
                host='project1.mysql.database.azure.com',
                port='3306',
                user='JUANFER',
                password='Duko0505',
                database='keynova'
            )
            return connection
        except Error as e:
            print("Error while connecting to MySQL", e)
            raise HTTPException(status_code=500, detail=e.msg)

    def agregar_propiedad_con_agente_mysql_connector(self,id_agente: int, Propietario_idPropietario: int, direccion: str, imagen: str, firmado: int = 0):
        connection = self.get_mysql_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("START TRANSACTION")
            cursor.execute("INSERT INTO `keynova`.`propiedad` (`Propietario_idPropietario`, `direccion`, `imagen`, `firmado`) "
                           "VALUES (%s, %s, %s, %s) "
                           "ON DUPLICATE KEY UPDATE `Propietario_idPropietario` = VALUES(`Propietario_idPropietario`), "
                           "`direccion` = VALUES(`direccion`), `imagen` = VALUES(`imagen`), `firmado` = VALUES(`firmado`);",
                           (Propietario_idPropietario, direccion, imagen, firmado))
            property_id = cursor.lastrowid
            cursor.execute("INSERT INTO `keynova`.`acceso` (`Propiedad_idPropiedad`, `Agente_idAgente`) "
                           "VALUES (%s, %s) "
                           "ON DUPLICATE KEY UPDATE `Propiedad_idPropiedad` = VALUES(`Propiedad_idPropiedad`), "
                           "`Agente_idAgente` = VALUES(`Agente_idAgente`);",
                           (property_id, id_agente))
            cursor.execute("COMMIT")
            cursor.execute("SELECT * FROM propiedad WHERE idPropiedad = %s", (property_id,))
            return cursor.fetchone()
        except mysql.connector.Error as e:
            if e.errno == 1452:
                cursor.execute("ROLLBACK")
                raise HTTPException(status_code=400, detail="No se encontró el agente o la propiedad")
            # Revertir la transacción en caso de error
        finally:
            cursor.close()
            connection.close()

# Función para medir el tiempo de ejecución del método
def compare_execution_time():
    db = DB()
    connection = db.get_mysql_connection()
    cursor = connection.cursor()

    start_time = time.time()
    propiedad = db.agregar_propiedad_con_agente_mysql_connector(1, 1, "prueba optimizada", "imagen")
    end_time = time.time()
    execution_time = end_time - start_time

    cursor.close()
    connection.close()

    print("Tiempo de ejecución para mysql-connector-python:", execution_time)
    return propiedad

propiedad_mysql_connector = compare_execution_time()
print(propiedad_mysql_connector)

