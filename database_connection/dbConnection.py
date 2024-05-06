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

    def agregar_propietario(self, nombre: str, correo: str, edad: str, genero: str,contrasennia:str):
        # Verificar si no existe un correo igual
        if self.existe_propietario_con_correo(correo):
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="You cannot post an OWNER  with an existing email")
        else:
            query = "INSERT INTO `keynova`.`propietario` (`nombre`,`correo`,`edad`,`genero`, `contrasennia`) " \
                    "VALUES (%s,%s,%s,%s, %s);"
            variables = (nombre, correo, int(edad), genero,contrasennia)
            self.executeSQL(query, variables)

    # ADICIONAL PROPIETARIO
    def obtener_propietario_por_correo(self, correo):
        query = "SELECT * FROM PROPIETARIO p WHERE p.correo = %s;"
        owner = self.executeSQL(query, (correo,))
        if len(owner) > 0:
            return owner[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Owner with this email was not found")

    def existe_propietario_con_correo(self,correo):
        query = "SELECT * FROM PROPIETARIO p WHERE p.correo = %s;"
        owner = self.executeSQL(query, (correo,))
        if len(owner) > 0:
            return True
        else:
            return False


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
                "VALUES (%s,%s,%s, %s);"
        variables = (nombre, correo, tipo, contrasennia)
        self.executeSQL(query, variables)

    def existe_agente_con_correo(self,correo):
        query = "SELECT * FROM AGENTE a WHERE a.correo = %s;"
        owner = self.executeSQL(query, (correo,))
        if len(owner) > 0:
            return True
        else:
            return False

    def obtener_agente_por_correo(self, correo):
        query = "SELECT * FROM AGENTE a WHERE a.correo = %s;"
        owner = self.executeSQL(query, (correo,))
        if len(owner) > 0:
            return owner[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner with this email was not found")

    # ADICIONAL AGENTE



    # TODO: ARRENDATARIO
    def obtener_arrendatarios(self):
        query = "SELECT * FROM ARRENDATARIO"
        arrendatarios = self.executeSQL(query)
        return arrendatarios

    def obtener_arrendatario_por_id(self, id: int):
        query = "SELECT * FROM ARRENDATARIO a WHERE a.idArrendatario = %s;"
        arrendatario = self.executeSQL(query, (id,))
        return arrendatario

    def eliminar_arrendatario(self, id: int):
        query = "DELETE FROM ARRENDATARIO a WHERE a.idArrendatario = %s"
        self.executeSQL(query, (id,))

    def agregar_arrendatario(self, nombre: str, correo: str, edad: str, genero: str):
        if(self.existe_arrendatario_con_correo(correo)):
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                                detail="You cannot post a tenant with an existing email")

        query = "INSERT INTO `keynova`.`arrendatario` (`nombre`,`correo`,`edad`,`genero`) " \
                "VALUES (%s,%s,%s,%s);"
        variables = (nombre, correo, int(edad), genero)
        self.executeSQL(query, variables)

    def existe_arrendatario_con_correo(self,correo):
        query = "SELECT * FROM ARRENDATARIO a WHERE a.correo = %s;"
        arrendatario = self.executeSQL(query, (correo,))
        if len(arrendatario) > 0:
            return True
        else:
            return False

    # ADICIONAL AGENTE

    def obtener_arrendatario_por_correo(self, correo):
        query = "SELECT * FROM ARRENDATARIO a WHERE a.correo = %s;"
        owner = self.executeSQL(query, (correo,))
        if len(owner) > 0:
            return owner[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Tenant with this email was not found")

    # TODO: ARRENDAMIENTO
    def obtener_arrendamientos(self):
        query = "SELECT * FROM ARRENDAMIENTO"
        arrendamientos = self.executeSQL(query)
        return arrendamientos

    def obtener_arrendamiento_por_id(self, id:int):
        query = "SELECT * FROM ARRENDAMIENTO a WHERE a.idArrendamiento = %s;"
        arrendamiento = self.executeSQL(query, (id,))
        if len(arrendamiento) > 0:
            return arrendamiento[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Rent with this id was not found")

    def eliminar_arrendamiento(self, id:int):
        query = "DELETE FROM ARRENDATARIO a WHERE a.idArrendatario = %s"
        self.executeSQL(query, (id,))

    def agregar_arrendamiento(self, id_propiedad:int, id_arrendatario:int, fecha_inicio:str):
        query = "INSERT INTO `keynova`.`arrendamiento` (`Propiedad_idPropiedad`,`Arriendatario_idArrendatario`,`fecha_inicio`) " \
                "VALUES (%s,%s,%s);"
        variables = (int(id_propiedad), int(id_arrendatario), fecha_inicio)
        self.executeSQL(query, variables)

    # TODO: PROPIEDAD
    def obtener_propiedades(self):
        query = "SELECT * FROM PROPIEDAD"
        arrendamientos = self.executeSQL(query)
        return arrendamientos

    def obtener_propiedad_por_id(self,id):
        query = "SELECT * FROM PROPIEDAD p WHERE p.idPropiedad = %s;"
        propiedad = self.executeSQL(query, (id,))
        if len(propiedad) > 0:
            return propiedad[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Property with this id was not found")

    def obtener_propiedad_por_direccion(self,direccion):
        query = "SELECT * FROM PROPIEDAD p WHERE p.direccion = %s;"
        propiedad = self.executeSQL(query, (direccion,))
        if len(propiedad) > 0:
            return propiedad[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Property with this direction was not found")

    def existe_propiedad_con_direccion(self,direccion):
        query = "SELECT * FROM PROPIEDAD p WHERE p.direccion = %s;"
        propiedad = self.executeSQL(query, (direccion,))
        if len(propiedad) > 0:
            return True
        else:
            return False


    def eliminar_propiedad(self, id:int):
        query = "DELETE FROM PROPIEDAD p WHERE p.idPropiedad = %s"
        self.executeSQL(query, (id,))

    def agregar_propiedad(self, id_propietario:int, direccion:str, tipo:str, imagen:str):
        if self.existe_propiedad_con_direccion(direccion):
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                                detail="You cannot post a Property with an existing address")

        query = "INSERT INTO `keynova`.`propiedad` (`Propietario_idPropietario`,`direccion`,`tipo`,`imagen`) " \
                "VALUES (%s,%s,%s,%s);"
        variables = (int(id_propietario), direccion, tipo, imagen)
        self.executeSQL(query, variables)

    # ADICIONALES PROPIEDAD

    def obtener_propiedades_por_id_propietario(self, id_propietario):
        query = "SELECT * FROM PROPIEDAD p WHERE p.Propietario_idPropietario = %s;"
        propiedades = self.executeSQL(query, (id,))
        return propiedades

    # TODO: HABITACION
    def obtener_habitaciones(self):
        query = "SELECT * FROM HABITACION"
        habitaciones = self.executeSQL(query)
        return habitaciones

    def obtener_habitacion_por_id(self, id):
        query = "SELECT * FROM HABITACION h WHERE h.idHabitacion = %s;"
        habitacion = self.executeSQL(query, (id,))
        if len(habitacion) > 0:
            return habitacion[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Room with this id was not found")

    def eliminar_habitacion(self, id:int):
        query = "DELETE FROM HABITACION h WHERE h.idHabitacion = %s"
        self.executeSQL(query, (id,))

    def agregar_habitacion(self, id_propiedad:int, estado:str, video:str, nombre:str):
        query = "INSERT INTO `keynova`.`habitacion` (`Propiedad_idPropiedad`,`estado`,`video`, `nombre`) " \
                "VALUES (%s,%s,%s,%s);"
        variables = (int(id_propiedad), estado, video,nombre)
        self.executeSQL(query, variables)

    # ADICIONALES HABITACIÓN

    def obtener_habitaciones_por_id_propiedad(self, id_propiedad):
        query = "SELECT * FROM HABITACION h WHERE h.Propiedad_idPropiedad = %s;"
        habitaciones = self.executeSQL(query, (id_propiedad,))
        return habitaciones

    # TODO: MUEBLE
    def obtener_muebles(self):
        query = "SELECT * FROM MUEBLE"
        muebles = self.executeSQL(query)
        return muebles

    def obtener_mueble_por_id(self, id: int):
        query = "SELECT * FROM MUEBLE m WHERE m.idMueble = %s;"
        mueble = self.executeSQL(query, (id,))
        if len(mueble) > 0:
            return mueble[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Furniture with this id was not found")

    def eliminar_mueble(self, id: int):
        query = "DELETE FROM MUEBLE m WHERE m.idMueble = %s"
        self.executeSQL(query, (id,))

    def agregar_mueble(self, id_habitacion:int, estado: str, imagen:str, descripcion:str, nombre :str):
        if self.existe_mueble_con_imagen(imagen):
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                                detail="You cannot post a Furniture with an existing image")
        query = "INSERT INTO `keynova`.`habitacion` (`Habitacion_idHabitacion`,`estado`,`imagen`,`descripcion`,`nombre`) " \
                "VALUES (%s,%s,%s,%s, %s);"
        variables = (int(id_habitacion), estado, imagen, descripcion,nombre)
        self.executeSQL(query, variables)

    # ADICIONALES MUEBLE

    def obtener_muebles_por_id_habitacion(self, id_habitacion):
        query = "SELECT * FROM MUEBLE m WHERE m.Habitacion_idHabitacion = %s;"
        mueble = self.executeSQL(query, (id_habitacion,))
        return mueble

    def obtener_mueble_por_imagen(self, imagen):
        query = "SELECT * FROM MUEBLE m WHERE m.imagen = %s;"
        mueble = self.executeSQL(query, (imagen,))
        if len(mueble) > 0:
            return mueble[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Furniture with this image was not found")

    def existe_mueble_con_imagen(self,imagen):
        query = "SELECT * FROM MUEBLE m WHERE m.imagen = %s;"
        mueble = self.executeSQL(query, (imagen,))
        if len(mueble) > 0:
            return True
        else:
            return False

    # TODO: ACCESO

    def obtener_accesos(self):
        query = "SELECT * FROM ACCESO"
        muebles = self.executeSQL(query)
        return muebles

    def obtener_accesos_por_id_agente(self, id_propiedad: int, id_agente: int):
        query = "SELECT * FROM ACCESO a WHERE a.Propiedad_idPropiedad = %s AND a.Agente_idAgente = %s;"
        accesos = self.executeSQL(query, (id_propiedad,id_agente))
        if len(accesos) > 0:
            return accesos[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Access with this id was not found")

    def eliminar_acceso(self, id_propiedad: int, id_agente: int):
        query = "DELETE FROM ACCESO a WHERE a.Propiedad_idPropiedad = %s AND a.Agente_idAgente = %s;"
        self.executeSQL(query, (id_propiedad,id_agente))

    def agregar_acceso(self, id_propiedad:int, id_agente: int):
        if self.existe_acceso_con_id_propiedad_id_agente(id_propiedad,id_agente):
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                                detail="You cannot post a Access with same property id and agent id")
        query = "INSERT INTO `keynova`.`acceso` (`Propiedad_idPropiedad`,`Agente_idAgente`) " \
                "VALUES (%s,%s);"
        variables = (id_propiedad, id_agente)
        self.executeSQL(query, variables)

    def existe_acceso_con_id_propiedad_id_agente(self,id_propiedad: int, id_agente: int):
        query = "SELECT * FROM ACCESO a WHERE a.Propiedad_idPropiedad = %s AND a.Agente_idAgente = %s;"
        acceso = self.executeSQL(query, (id_propiedad,id_agente))
        if len(acceso) > 0:
            return True
        else:
            return False
