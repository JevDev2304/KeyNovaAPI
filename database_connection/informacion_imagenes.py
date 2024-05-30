# PROPIEDADES
# 5a984fb8-f60e-4e50-a0ee-8db0209c9383.jpg FACHADA CASA 1
# 10feb17e-09f9-403b-a711-db95c6e68ad9.jpg FACHADA CASA 2
# 07be1ae6-d2e4-4cb6-92eb-b19b6134df3d.jpg FACHADA CASA 3
# ad62eca5-e759-4f6c-be51-056b95251e7a.jpg FACHADA CASA 4
# b272950c-ae57-4b4a-986f-a70a3b886c6f.jpg FACHADA CASA 5

# ESPACIOS
# b3cc58df-8e43-40cf-9daa-54820d4498a7.jpg COCINA 1
# 26a4f58b-cab6-433e-bbc0-0d7fda2b78ad.jpg BAÑO 1
# 93cd050e-f6f9-44d5-bb64-b87445141913.jpg HABITACION PRINCIPAL 1
# ac9c55bc-7fa8-4f3a-8251-ada6164b179e.jpg BAÑO 2
# fefd8e80-2398-48d6-bad5-6c971b609341.jpg COCINA 2
# 0a521878-142f-44de-8450-198d6e23da26.jpg HABITACIÓN PRINCIPAL 2
# bfcd4615-d521-4b4c-946f-1a3997580c92.jpg HABITACIÓN SECUNDARIA
# 37b4e85b-3b5d-4820-be32-a62531acc706.jpg COCINA 3

# MUEBLES
# 5cf9dfa7-4501-4bb3-aa26-9dbe08cdc0f7.jpg SILLA RIMAX
# f62e8337-7a64-4f76-b16e-0f81b29c3cdb.jpg SILLA PLAYERA
# b2d8c10e-9210-4886-a374-379131a7927d.jpg FLORERO
# ed74f966-d12f-4f69-8ebf-241aaeb1ac35.jpg ESCRITORIO
# 030c7e35-311b-4ff2-9bad-aaae8121104f.jpg LAMPARA

# 38937ae9-591b-4782-88da-62f820c011e7.jpg LICUADORA

# FOTOS DE PERFIL.
# 3882d8af-37cf-4d70-bb55-b85dce26f845.jpg FOTO 1
# ccf9baca-316f-40a6-b6bc-5b06f12c35eb.jpg FOTO 2

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

