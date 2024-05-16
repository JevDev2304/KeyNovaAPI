from fastapi import HTTPException, status
import mysql.connector

config = {'user': 'JUANFER',
          'host': 'project1.mysql.database.azure.com',
          'password': 'Duko0505',
          'database': 'keynova',
          'port': 3306,  # Puerto predeterminado de MySQL
          'raise_on_warnings': True}  # Para que se generen excepciones en caso de advertencias


class ConnectionDB:
    conn = None  # Mantén la conexión abierta en la instancia

    def __init__(self):
        pass

    def executeSQL(self, consulta_sql, variables_adicionales=None):
        try:
            conn = mysql.connector.connect(**config)  # Abre la conexión si no está abierta

            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute(consulta_sql, variables_adicionales)

                if consulta_sql.strip().upper().startswith("INSERT") or consulta_sql.strip().upper().startswith(
                        "UPDATE") or consulta_sql.strip().upper().startswith(
                    "DELETE") or consulta_sql.strip().upper().startswith("CREATE"):
                    conn.commit()
                    return None

                resultados = cursor.fetchall()
                conn.close()
                return resultados
        except mysql.connector.Error as e:
            print("Error al conectar a la base de datos:", e)

    # TODO: AGENTE (Siempre están quemados)
    def obtener_agente_por_id(self, id: int):
        query = "SELECT * FROM AGENTE a WHERE a.idAgente = %s;"
        agent = self.executeSQL(query, (id,))
        if len(agent) > 0:
            return agent[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent with this id was not found")

    def eliminar_agente(self, id: int):
        self.obtener_agente_por_id(id)  # Para que salga la excepcion de ahi
        query = "DELETE FROM AGENTE WHERE idAgente = %s;"
        self.executeSQL(query, (id,))

    def obtener_agente_por_correo(self, correo):
        query = "SELECT * FROM AGENTE a WHERE a.correo = %s;"
        owner = self.executeSQL(query, (correo,))
        if len(owner) > 0:
            return owner[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent with this email was not found")

    def existe_agente_con_correo(self, correo):
        query = "SELECT * FROM AGENTE a WHERE a.correo = %s;"
        owner = self.executeSQL(query, (correo,))
        if len(owner) > 0:
            return True
        else:
            return False

    def existe_agente_con_id(self, id):
        query = "SELECT * FROM AGENTE a WHERE a.idAgente = %s;"
        owner = self.executeSQL(query, (id,))
        if len(owner) > 0:
            return True
        else:
            return False

    # TODO: PROPIETARIO

    def obtener_propietario_por_id(self, id: int):
        query = "SELECT * FROM PROPIETARIO p WHERE p.idPropietario = %s;"
        owner = self.executeSQL(query, (id,))
        if len(owner) > 0:
            return owner[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner with this email was not found")

    def eliminar_propietario(self, id: int):
        self.obtener_propietario_por_id(id)
        query = "DELETE FROM PROPIETARIO p WHERE p.idPropietario = %s"
        self.executeSQL(query, (id,))

    def agregar_propietario(self, nombre: str, correo: str, genero: str, contrasennia: str):
        if self.existe_propietario_con_correo(correo):
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                                detail="You cannot post an OWNER  with an existing email")
        else:
            query = "INSERT INTO `keynova`.`propietario` (`nombre`,`correo`,`genero`, `contrasennia`) " \
                    "VALUES (%s,%s,%s,%s);"
            variables = (nombre, correo, genero, contrasennia)
            self.executeSQL(query, variables)

    def obtener_propietario_por_correo(self, correo):
        query = "SELECT * FROM PROPIETARIO p WHERE p.correo = %s;"
        owner = self.executeSQL(query, (correo,))
        if len(owner) > 0:
            return owner[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner with this email was not found")

    def existe_propietario_con_correo(self, correo):
        query = "SELECT * FROM PROPIETARIO p WHERE p.correo = %s;"
        owner = self.executeSQL(query, (correo,))
        if len(owner) > 0:
            return True
        else:
            return False

    def existe_propietario_con_id(self, id):
        try:
            query = "SELECT * FROM PROPIETARIO p WHERE p.idPropietario = %s;"
            owner = self.executeSQL(query, (id,))
            if len(owner) > 0:
                return True
            else:
                return False
        except Exception as e:
            return False

    # TODO: ACCESO

    def obtener_accesos_por_id(self, id_propiedad: int, id_agente: int):
        if not self.existe_agente_con_id(id_agente):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent with this id was not found")
        elif not self.existe_propiedad_con_id(id_propiedad):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner with this id was not found")
        else:
            query = "SELECT * FROM ACCESO a WHERE a.Propiedad_idPropiedad = %s AND a.Agente_idAgente = %s;"
            accesos = self.executeSQL(query, (id_propiedad, id_agente))
            return accesos

    def eliminar_acceso(self, id_propiedad: int, id_agente: int):
        if not self.existe_propiedad_con_id(id_propiedad):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property with this id was not found")
        elif not self.existe_agente_con_id(id_agente):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent with this id was not found")
        else:
            query = "DELETE FROM ACCESO a WHERE a.Propiedad_idPropiedad = %s AND a.Agente_idAgente = %s;"
            self.executeSQL(query, (id_propiedad, id_agente))

    def agregar_acceso(self, id_propiedad: int, id_agente: int):
        if len(self.obtener_accesos_por_id(id_propiedad, id_agente)) > 0:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Access already exist")
        else:
            query = "INSERT INTO `keynova`.`acceso` (`Propiedad_idPropiedad`,`Agente_idAgente`) " \
                    "VALUES (%s,%s);"
            variables = (id_propiedad, id_agente)
            self.executeSQL(query, variables)

    # TODO: PROPIEDAD

    def obtener_propiedad_por_id(self, id: int):
        query = "SELECT * FROM PROPIEDAD p WHERE p.idPropiedad = %s;"
        propiedad = self.executeSQL(query, (id,))
        if len(propiedad) > 0:
            return propiedad[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property with this id was not found")

    def actualizar_propiedad(self, id_propiedad: int, id_propietario: int, direccion: str, imagen: str):
        query = ("UPDATE `keynova`.`propiedad` SET `Propietario_idPropietario` = %s,`direccion` = %s,"
                 "`imagen` = %sWHERE `idPropiedad` = %s;")
        variables = (id_propietario, direccion, imagen, id_propiedad)
        self.executeSQL(query, variables)

    def eliminar_propiedad(self, id: int):
        self.obtener_propiedad_por_id(id)
        query = "DELETE FROM PROPIEDAD p WHERE p.idPropiedad = %s"
        self.executeSQL(query, (id,))

    def agregar_propiedad(self, Propietario_idPropietario: int, direccion: str, imagen: str):
        if not self.existe_propietario_con_id(Propietario_idPropietario):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner with this id was not found")
        else:
            query = "INSERT INTO `keynova`.`propiedad` (`Propietario_idPropietario`,`direccion`,`imagen`) " \
                    "VALUES (%s,%s,%s);"
            variables = (int(Propietario_idPropietario), direccion, imagen)
            self.executeSQL(query, variables)
            query = "SELECT * FROM propiedad ORDER BY idPropiedad DESC LIMIT 1;"
            return self.executeSQL(query)[0]

    def agregar_propiedad_con_agente(self, id_agente: int, id_propietario: int, direccion: str, imagen: str):
        if not self.existe_propietario_con_id(id_propietario):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner with this id was not found")
        else:
            query = "INSERT INTO `keynova`.`propiedad` (`Propietario_idPropietario`,`direccion`,`imagen`) " \
                    "VALUES (%s,%s,%s);"
            variables = (int(id_propietario), direccion, imagen)
            self.executeSQL(query, variables)

    # ADICIONALES PROPIEDAD

    def obtener_propiedades_por_id_propietario(self, id_propietario):
        if not self.existe_propietario_con_id(id_propietario):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner with this id was not found")
        else:
            query = "SELECT * FROM PROPIEDAD p WHERE p.Propietario_idPropietario = %s;"
            propiedades = self.executeSQL(query, (id_propietario,))
            return propiedades

    def existe_propiedad_con_id(self, id):
        query = "SELECT * FROM PROPIEDAD p WHERE p.idPropiedad = %s;"
        propiedad = self.executeSQL(query, (id,))
        if len(propiedad) > 0:
            return True
        else:
            return False

    def obtener_propiedades_por_id_agente(self, id_agente):
        if not self.existe_agente_con_id(id_agente):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent with this id was not found")
        else:
            query = "select idPropiedad,Propietario_idPropietario, direccion, p.imagen from propiedad p join (select * from agente ag JOIN acceso ac on ag.idAgente = ac.Agente_idAgente where ag.idAgente = %s) acg on p.idPropiedad = acg.Propiedad_idPropiedad;"
            variables = (id_agente,)
            properties = self.executeSQL(query, variables)
            return properties

    # TODO: HABITACION

    def obtener_habitacion_por_id(self, id: int):
        query = "SELECT * FROM HABITACION h WHERE h.idHabitacion = %s;"
        habitacion = self.executeSQL(query, (id,))
        if len(habitacion) > 0:
            return habitacion[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room with this id was not found")

    # Aquí como que sobra id_propiedad, pero no se si te daña el modelo de la api
    def actualizar_habitacion(self, id_habitacion: int, estado: str, imagen: str, nombre: str):
        query = ("UPDATE `keynova`.`habitacion` SET `estado` = %s,`imagen` = %s,"
                 "`nombre` = %s WHERE `idHabitacion` = %s;")
        variables = (estado, imagen, nombre, id_habitacion)
        self.executeSQL(query, variables)

    def eliminar_habitacion(self, id: int):
        self.obtener_habitacion_por_id(id)
        query = "DELETE FROM HABITACION h WHERE h.idHabitacion = %s"
        self.executeSQL(query, (id,))

    def agregar_habitacion(self, id_propiedad: int, estado: str, imagen: str, nombre: str):
        if not self.existe_propiedad_con_id(id_propiedad):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property with this id was not found")
        else:
            query = "INSERT INTO `keynova`.`habitacion` (`Propiedad_idPropiedad`,`estado`,`imagen`,`nombre`) " \
                    "VALUES (%s,%s,%s,%s);"
            variables = (int(id_propiedad), estado, imagen, nombre)
            self.executeSQL(query, variables)
            query = "SELECT * FROM habitacion ORDER BY idHabitacion DESC LIMIT 1;"
            return self.executeSQL(query)[0]

    # ADICIONALES HABITACIÓN

    def obtener_habitaciones_por_id_propiedad(self, id_propiedad):
        if not self.existe_propiedad_con_id(id_propiedad):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property with this id was not found")
        else:
            query = "SELECT * FROM HABITACION h WHERE h.Propiedad_idPropiedad = %s;"
            habitaciones = self.executeSQL(query, (id_propiedad,))
            return habitaciones

    def existe_habitacion_con_id(self, id):
        query = "SELECT * FROM HABITACION h WHERE h.idHabitacion = %s;"
        room = self.executeSQL(query, (id,))
        if len(room) > 0:
            return True
        else:
            return False

    # TODO: MUEBLE

    def obtener_mueble_por_id(self, id: int):
        if not self.existe_mueble_con_id(id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Furniture with this id was not found")
        else:
            query = "SELECT * FROM MUEBLE m WHERE m.idMueble = %s;"
            mueble = self.executeSQL(query, (id,))
            return mueble

    def existe_mueble_con_id(self, id):
        query = "SELECT * FROM MUEBLE m WHERE m.idMueble = %s;"
        mueble = self.executeSQL(query, (id,))
        if len(mueble) > 0:
            return True
        else:
            return False

    def actualizar_mueble(self, id_mueble: int, estado: str, imagen: str, descripcion: str,
                          nombre: str):
        query = ("UPDATE `keynova`.`mueble` SET `estado` = %s, `imagen` = %s, "
                 "`descripcion` = %s, `nombre` = %s WHERE `idMueble` = %s;")
        variables = ( estado, imagen, descripcion, nombre, id_mueble)
        self.executeSQL(query, variables)

    def eliminar_mueble(self, id: int):
        self.obtener_mueble_por_id(id)
        query = "DELETE FROM MUEBLE m WHERE m.idMueble = %s"
        self.executeSQL(query, (id,))

    def agregar_mueble(self, id_habitacion: int, estado: str, imagen: str, descripcion: str, nombre: str):
        if not self.existe_habitacion_con_id(id_habitacion):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room with this id was not found")
        else:
            query = "INSERT INTO `keynova`.`habitacion` (`Habitacion_idHabitacion`,`estado`,`imagen`,`descripcion`,`nombre`) " \
                    "VALUES (%s,%s,%s,%s,%s);"
            variables = (int(id_habitacion), estado, imagen, descripcion, nombre)
            self.executeSQL(query, variables)
            query = "SELECT * FROM mueble ORDER BY idMueble DESC LIMIT 1;"
            return self.executeSQL(query)[0]

    # ADICIONALES MUEBLE

    def obtener_muebles_por_id_habitacion(self, id_habitacion):
        if not self.existe_habitacion_con_id(id_habitacion):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room with this id was not found")
        else:
            query = "SELECT * FROM MUEBLE m WHERE m.Habitacion_idHabitacion = %s;"
            mueble = self.executeSQL(query, (id_habitacion,))
            return mueble

#AGENTE GENERAL
#OTP PARA INVENTARIO  (OBLIGATORIO) (TODO)

#ACTUALIZAR , HABITACION Y MUEBLES DE LAS PROPIEDADES QUE TIENE ACCESO  (LISTO EN BD)
#OBTENER PROPIEDAD DE UN AGENTE, HABITACIONES Y MUEBLES (LISTO BD)

#AGENTE COMERCIAL
#CREAR PROPIEDADES DE UN AGENTE , HABITACION Y MUEBLES  (LISTO EN BD)
#OBTENER AGENTES DE MANTENIMIENTO  (TODO)
#CREAR ACCESOS PARA UN AGENTE DE MANTENIMIENTO (LISTO EN BD)
#ELIMINAR ACCESO (LISTO EN BD)
#OBTENER PROPIETARIOS DE LAS PROPIEDADES DE UN AGENTE ///////////(TODO)
# OBTENER LAS PROPIEDADES DE UN PROPIETARIO ///////////////// (LISTO EN BD)
#CREAR PROPIETARIO (LISTO EN BD)
#MANDAR CORREO AL PROPIETARIO CON SU INVENTARIO (TODO)

#CRD DE MANTENIMIENTO (TODO)
#OBTENER TODOS LOS MANTENIMIENTO DE UNA PROPIEDAD (TODO)
#OBTENER TODOS LOS MANTENIMIENTOS DE LAS PROPIEDADES DE UN AGENTE COMERCIAL(TODO)

#AGENTE MANTENIMIENTO
#MANDAR CORREO CADA VEZ QUE SE HACE UN MANTENIMIENTO (TODO)
