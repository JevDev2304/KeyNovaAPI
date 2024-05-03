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

    # TODO: PROPIETARIO
    def obtener_propietarios(self):
        query = "SELECT * FROM PROPIETARIO"
        owners = self.executeSQL(query)
        return owners

    def obtener_propietario_por_id(self, id: int):
        query = "SELECT * FROM PROPIETARIO p WHERE p.idPropietario = %s;"
        owner = self.executeSQL(query, (id,))
        return owner

    def eliminar_propietario(self, id: int):
        query = "DELETE FROM PROPIETARIO p WHERE p.idPropietario = %s"
        self.executeSQL(query, (id,))

    def agregar_propietario(self, nombre: str, correo: str, edad: str, genero: str):
        query = "INSERT INTO `keynova`.`propietario` (`nombre`,`correo`,`edad`,`genero`) " \
                "VALUES (%s,%s,%s);"
        variables = (nombre, correo, int(edad), genero)
        self.executeSQL(query, variables)

    def obtener_propietario_por_correo(self, correo):
        query = "SELECT * FROM PROPIETARIO p WHERE p.correo = %s;"
        owner = self.executeSQL(query, (correo,))
        if len(owner) > 0:
            return owner[0]
        else:
            return None
    # TODO: AGENTE
    def obtener_agentes(self):
        query = "SELECT * FROM AGENTE"
        agents = self.executeSQL(query)
        return agents

    def obtener_agente_por_id(self, id: int):
        query = "SELECT * FROM AGENTE a WHERE a.idAgente = %s;"
        agent = self.executeSQL(query, (id,))
        return agent

    def eliminar_agente(self, id: int):
        query = "DELETE FROM AGENTE a WHERE a.idAgente = %s"
        self.executeSQL(query, (id,))

    def agregar_agente(self, nombre: str, correo: str, tipo: str, contrasennia: str):
        query = "INSERT INTO `keynova`.`agente` (`nombre`,`correo`,`tipo`,`contrasennia`) " \
                "VALUES (%s,%s,%s);"
        variables = (nombre, correo, tipo, contrasennia)
        self.executeSQL(query, variables)

    def obtener_agente_por_correo(self, correo):
        query = "SELECT * FROM AGENTE a WHERE a.correo = %s;"
        owner = self.executeSQL(query, (correo,))
        if len(owner) > 0:
            return owner[0]
        else:
            return None

    # TODO: ARRENDATARIO
    def obtener_arrendatarios(self):
        query = "SELECT * FROM ARRENDATARIO"
        arrendatario = self.executeSQL(query)
        return arrendatario

    def obtener_arrendatario_por_id(self, id: int):
        query = "SELECT * FROM ARRENDATARIO a WHERE a.idArrendatario = %s;"
        arrendatario = self.executeSQL(query, (id,))
        return arrendatario



    def obtener_arrendatario_por_correo(self, correo):
        query = "SELECT * FROM ARRENDATARIO a WHERE a.correo = %s;"
        owner = self.executeSQL(query, (correo,))
        if len(owner) > 0:
            return owner[0]
        else:
            return None


    def eliminar_arrendatario(self, id: int):
        query = "DELETE FROM ARRENDATARIO a WHERE a.idArrendatario = %s"
        self.executeSQL(query, (id,))

    def agregar_arrendatario(self, nombre: str, correo: str, edad: str, genero: str):
        query = "INSERT INTO `keynova`.`arrendatario` (`nombre`,`correo`,`edad`,`genero`) " \
                "VALUES (%s,%s,%s,%s);"
        variables = (nombre, correo, int(edad), genero)
        self.executeSQL(query, variables)

    # TODO: ARRENDAMIENTO
    def obtener_arrendamientos(self):
        query = "SELECT * FROM ARRENDAMIENTO"
        arrendamientos = self.executeSQL(query)
        return arrendamientos

    def obtener_arrendamiento_por_id(self, id:int):
        query = "SELECT * FROM ARRENDAMIENTO a WHERE a.idArrendamiento = %s;"
        arrendamiento = self.executeSQL(query, (id,))
        return arrendamiento

    def eliminar_arrendamiento(self, id:int):
        query = "DELETE FROM ARRENDATARIO a WHERE a.idArrendatario = %s"
        self.executeSQL(query, (id,))

    def agregar_arrendamiento(self, id_propiedad:int, id_arrendatario:int, fecha_inicio:str):
        query = "INSERT INTO `keynova`.`arrendamiento` (`Propiedad_idPropiedad`,`Arriendatario_idArrendatario`,`fecha_inicio`) " \
                "VALUES (%s,%s,%s);"
        variables = (int(id_propiedad), int(id_arrendatario), fecha_inicio)
        self.executeSQL(query, variables)

    # TODO: ARRENDAMIENTO
    def obtener_propiedades(self):
        query = "SELECT * FROM ARRENDAMIENTO"
        arrendamientos = self.executeSQL(query)
        return arrendamientos

    def obtener_propiedad_por_id(self):
        query = "SELECT * FROM PROPIEDAD p WHERE p.idPropiedad = %s;"
        propiedad = self.executeSQL(query, (id,))
        return propiedad

    def eliminar_propiedad(self, id:int):
        query = "DELETE FROM PROPIEDAD p WHERE p.idPropiedad = %s"
        self.executeSQL(query, (id,))

    def agregar_propiedad(self, id_propietario:int, direccion:str, tipo:str, imagen:str):
        query = "INSERT INTO `keynova`.`propiedad` (`Propietario_idPropietario`,`direccion`,`tipo`,`imagen`) " \
                "VALUES (%s,%s,%s,%s);"
        variables = (int(id_propietario), direccion, tipo, imagen)
        self.executeSQL(query, variables)


    # TODO: HABITACION
    def obtener_habitaciones(self):
        query = "SELECT * FROM HABITACION"
        habitaciones = self.executeSQL(query)
        return habitaciones

    def obtener_habitacion_por_id(self):
        query = "SELECT * FROM HABITACION h WHERE h.idHabitacion = %s;"
        habitacion = self.executeSQL(query, (id,))
        return habitacion

    def eliminar_habitacion(self, id:int):
        query = "DELETE FROM HABITACION h WHERE h.idHabitacion = %s"
        self.executeSQL(query, (id,))

    def agregar_habitacion(self, id_propiedad:int, estado:str, video:str):
        query = "INSERT INTO `keynova`.`habitacion` (`Propiedad_idPropiedad`,`estado`,`video`) " \
                "VALUES (%s,%s,%s);"
        variables = (int(id_propiedad), estado, video)
        self.executeSQL(query, variables)

    # TODO: MUEBLE
    def obtener_muebles(self):
        query = "SELECT * FROM MUEBLE"
        muebles = self.executeSQL(query)
        return muebles

    def obtener_mueble_por_id(self):
        query = "SELECT * FROM MUEBLE m WHERE m.idMueble = %s;"
        mueble = self.executeSQL(query, (id,))
        return mueble
    def obtener_mueble_por_imagen(self, imagen):
        query = "SELECT * FROM MUEBLE m WHERE m.imagen = %s;"
        mueble = self.executeSQL(query, (imagen,))
        if len(mueble) > 0:
            return mueble[0]
        else:
            return None
    def eliminar_mueble(self, id: int):
        query = "DELETE FROM MUEBLE m WHERE m.idMueble = %s"
        self.executeSQL(query, (id,))

    def agregar_mueble(self, id_habitacion:int, estado: str, imagen:str, descripcion:str):
        query = "INSERT INTO `keynova`.`habitacion` (`Habitacion_idHabitacion`,`estado`,`imagen`,`descripcion`) " \
                "VALUES (%s,%s,%s,%s);"
        variables = (int(id_habitacion), estado, imagen, descripcion)
        self.executeSQL(query, variables)

