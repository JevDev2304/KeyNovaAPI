import random
import time

from fastapi import HTTPException, status
from mysql.connector import pooling, Error


class ConnectionDB:

    def __init__(self):
        dbconfig = {
            "user": 'JUANFER',
            "password": 'Duko0505',
            "host": 'project1.mysql.database.azure.com',
            "port": '3306',
            "database": 'keynova'
        }
        self.conn = None  # Mantén la conexión abierta en la instancia
        pool = pooling.MySQLConnectionPool(pool_name="mypool",
                                           pool_size=5,
                                           **dbconfig)

        try:
            connection = pool.get_connection()
            self.conn = connection
        except Error as e:
            print("Error while connecting to MySQL", e)
            raise HTTPException(status_code=500, detail=e.msg)

    def executeSQL(self, consulta_sql, variables_adicionales=None):
        cursor = self.conn.cursor()
        # Agregar la propiedad y obtener el id de la propiedad recién agregada
        cursor.execute(consulta_sql, variables_adicionales)

        if consulta_sql.strip().upper().startswith("INSERT") or consulta_sql.strip().upper().startswith(
                "UPDATE") or consulta_sql.strip().upper().startswith(
            "DELETE") or consulta_sql.strip().upper().startswith("CREATE"):
            self.conn.commit()
            cursor.close()
            return cursor.lastrowid if consulta_sql.strip().upper().startswith("INSERT") else None
        result = cursor.fetchall()
        cursor.close()
        return result


    # TODO: AGENTE (Siempre están quemados)
    def obtener_agente_por_id(self, idAgente: int):
        query = "SELECT * FROM AGENTE a WHERE a.idAgente = %s;"
        agent = self.executeSQL(query, (idAgente,))
        if len(agent) > 0:
            return agent[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent with this id was not found")

    # FIXME
    def obtener_agentes_mantenimiento_acceso_a_propiedad(self, idPropiedad: int):
        if not self.existe_propiedad_con_id(idPropiedad):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property with this id was not found")
        else:
            query = "SELECT * FROM AGENTE WHERE tipo = 'mantenimiento'"
            agentes = self.executeSQL(query)
            agentes_list = []
            for agente in agentes:
                agente_lista = list(agente)
                if self.existe_acceso(idPropiedad, agente[0]):
                    agente_lista.append(True)
                else:
                    agente_lista.append(False)
                agentes_list.append(agente_lista)
            print(agentes_list)
            return agentes_list

    # FIXME
    def eliminar_agente(self, idAgente: int):
        self.obtener_agente_por_id(idAgente)  # Para que salga la excepcion de ahi
        query = "DELETE FROM AGENTE WHERE idAgente = %s;"
        self.executeSQL(query, (idAgente,))

    def obtener_agente_por_correo(self, correo):
        query = "SELECT * FROM AGENTE a WHERE a.correo = %s;"
        owner = self.executeSQL(query, (correo,))
        if len(owner) > 0:
            return owner[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent with this email was not found")

    # TODO: BORRAR PARA REEMPLAZARLO POR TRY CATCH
    def existe_agente_con_correo(self, correo):
        try:
            query = "SELECT * FROM AGENTE a WHERE a.correo = %s;"
            owner = self.executeSQL(query, (correo,))
            if len(owner) > 0:
                return True
            else:
                return False
        except Exception:
            return False

    # TODO: BORRAR PARA REEMPLAZARLO POR TRY CATCH
    def existe_agente_con_id(self, idAgente: int):
        try:
            query = "SELECT * FROM AGENTE a WHERE a.idAgente = %s;"
            owner = self.executeSQL(query, (idAgente,))
            if len(owner) > 0:
                return True
            else:
                return False
        except Exception:
            return False

    #FIXME
    def crear_clave_temporal(self, idAgente: int):
        self.obtener_agente_por_id(idAgente)
        query = "UPDATE `keynova`.`agente` SET `clave_temporal` = %s WHERE `idAgente` = %s;"
        num_aleatorio = random.randint(100000, 999999)
        self.executeSQL(query, (num_aleatorio, idAgente))
        return num_aleatorio

    # TODO: PROPIETARIO

    def obtener_propietario_por_id(self, idPropietario: int):
        query = "SELECT * FROM PROPIETARIO p WHERE p.idPropietario = %s;"
        owner = self.executeSQL(query, (idPropietario,))
        if len(owner) > 0:
            return owner[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner with this id was not found")

    # FIXME
    def obtener_propietario_por_id_propiedad(self, id_propiedad: int):
        if not self.existe_propiedad_con_id(id_propiedad):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property with this id was not found")
        else:
            query = "SELECT * FROM PROPIETARIO p WHERE p.idPropietario = (SELECT Propietario_idPropietario FROM PROPIEDAD WHERE idPropiedad = %s);"
            owner = self.executeSQL(query, (id_propiedad,))
            if len(owner) > 0:
                return owner[0]
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner with this id was not found")

    # FIXME
    def eliminar_propietario(self, idPropietario: int):
        self.obtener_propietario_por_id(idPropietario)
        query = "DELETE FROM PROPIETARIO p WHERE p.idPropietario = %s"
        self.executeSQL(query, (idPropietario,))

    # FIXME
    def agregar_propietario(self, nombre: str, correo: str, genero: str, contrasennia: str,
                            agente_idAgente:int, cedula: int):
        if self.existe_propietario_con_correo(correo):
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                                detail="You cannot post an OWNER  with an existing email")
        else:
            query = "INSERT INTO `keynova`.`propietario` (`nombre`,`correo`,`genero`, `contrasennia`,`agente_idAgente`,`cedula`,`celular`) " \
                    "VALUES (%s,%s,%s,%s,%s,%s,%s);"
            variables = (nombre, correo, genero, contrasennia,agente_idAgente,cedula)
            self.executeSQL(query, variables)
            query = "SELECT * FROM propietario ORDER BY idPropietario DESC LIMIT 1;"
            return self.executeSQL(query)[0]

    def obtener_propietario_por_correo(self, correo):
        query = "SELECT * FROM PROPIETARIO p WHERE p.correo = %s;"
        owner = self.executeSQL(query, (correo,))
        if len(owner) > 0:
            return owner[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner with this email was not found")

    # TODO: BORRAR PARA REEMPLAZARLO POR TRY CATCH
    def existe_propietario_con_correo(self, correo):
        try:
            query = "SELECT * FROM PROPIETARIO p WHERE p.correo = %s;"
            owner = self.executeSQL(query, (correo,))
            if len(owner) > 0:
                return True
            else:
                return False
        except Exception:
            return False

    # TODO: BORRAR PARA REEMPLAZARLO POR TRY CATCH
    def existe_propietario_con_id(self, idPropietario):
        try:
            query = "SELECT * FROM PROPIETARIO p WHERE p.idPropietario = %s;"
            owner = self.executeSQL(query, (idPropietario,))
            if len(owner) > 0:
                return True
            else:
                return False
        except Exception as e:
            print(e.args)
            return False
        # TODO: ACCESO

    # FIXME
    def obtener_acceso_por_id(self, Propiedad_idPropiedad: int, Agente_idAgente: int):
        if not self.existe_agente_con_id(Agente_idAgente):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent with this id was not found")
        elif not self.existe_propiedad_con_id(Propiedad_idPropiedad):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner with this id was not found")
        else:
            query = "SELECT * FROM ACCESO a WHERE a.Propiedad_idPropiedad = %s AND a.Agente_idAgente = %s;"
            accesos = self.executeSQL(query, (Propiedad_idPropiedad, Agente_idAgente))
            if len(accesos) > 0:
                return accesos[0]
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Access with those ids were not found")

    # FIXME
    def eliminar_acceso(self, Propiedad_idPropiedad: int, Agente_idAgente: int):
        if not self.existe_propiedad_con_id(Propiedad_idPropiedad):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property with this id was not found")
        elif not self.existe_agente_con_id(Agente_idAgente):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent with this id was not found")
        else:
            query = "DELETE FROM ACCESO a WHERE a.Propiedad_idPropiedad = %s AND a.Agente_idAgente = %s;"
            self.executeSQL(query, (Propiedad_idPropiedad, Agente_idAgente))

    # FIXME
    def agregar_acceso(self, Propiedad_idPropiedad: int, Agente_idAgente: int):
        if self.existe_acceso(Propiedad_idPropiedad, Agente_idAgente):
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Access already exist")
        else:
            query = "INSERT INTO `keynova`.`acceso` (`Propiedad_idPropiedad`,`Agente_idAgente`) " \
                    "VALUES (%s,%s);"
            variables = (Propiedad_idPropiedad, Agente_idAgente)
            self.executeSQL(query, variables)

    # TODO: BORRAR PARA REEMPLAZARLO POR TRY CATCH
    def existe_acceso(self, Propiedad_idPropiedad: int, Agente_idAgente: int):
        if not self.existe_agente_con_id(Agente_idAgente):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent with this id was not found")
        elif not self.existe_propiedad_con_id(Propiedad_idPropiedad):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner with this id was not found")
        query = "SELECT * FROM ACCESO a WHERE a.Propiedad_idPropiedad = %s AND a.Agente_idAgente = %s;"
        accesos = self.executeSQL(query, (Propiedad_idPropiedad, Agente_idAgente))
        if len(accesos) > 0:
            return True
        else:
            return False

    # TODO: PROPIEDAD

    def obtener_propiedad_por_id(self, idPropiedad: int):
        query = "SELECT * FROM PROPIEDAD p WHERE p.idPropiedad = %s;"
        propiedad = self.executeSQL(query, (idPropiedad,))
        if len(propiedad) > 0:
            return propiedad[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property with this id was not found")

    # FIXME
    def actualizar_propiedad(self, idPropiedad: int, Propietario_idPropietario: int, direccion: str, imagen: str,
                             firmado: int):
        query = ("UPDATE `keynova`.`propiedad` SET `Propietario_idPropietario` = %s,`direccion` = %s,"
                 "`imagen` = %s , `firmado` = %s WHERE `idPropiedad` = %s;")
        variables = (Propietario_idPropietario, direccion, imagen, firmado, idPropiedad)
        self.executeSQL(query, variables)

    # FIXME
    def eliminar_propiedad(self, idPropiedad: int):
        self.obtener_propiedad_por_id(idPropiedad)
        query = "DELETE FROM PROPIEDAD p WHERE p.idPropiedad = %s"
        self.executeSQL(query, (idPropiedad,))

    # FIXME
    def _agregar_propiedad(self, Propietario_idPropietario: int, direccion: str, imagen: str, firmado: int):
        if not self.existe_propietario_con_id(Propietario_idPropietario):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner with this id was not found")
        else:
            query = "INSERT INTO `keynova`.`propiedad` (`Propietario_idPropietario`,`direccion`,`imagen`, `firmado`) " \
                    "VALUES (%s,%s,%s,%s);"
            variables = (int(Propietario_idPropietario), direccion, imagen, firmado)
            self.executeSQL(query, variables)
            query = "SELECT * FROM propiedad ORDER BY idPropiedad DESC LIMIT 1;"
            return self.executeSQL(query)[0]

    # FIXME
    def agregar_propiedad_con_agente(self, idAgente: int, Propietario_idPropietario: int, direccion: str, imagen: str,
                                     firmado: int = 0):
        if not self.existe_propietario_con_id(Propietario_idPropietario):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner with this id was not found")
        else:
            property = self._agregar_propiedad(Propietario_idPropietario, direccion, imagen, firmado)
            self.agregar_acceso(property[0], idAgente)
            return property

    # FIXME
    def obtener_propiedades_por_id_propietario(self, Propietario_idPropietario):
        if not self.existe_propietario_con_id(Propietario_idPropietario):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner with this id was not found")
        else:
            query = "SELECT * FROM PROPIEDAD p WHERE p.Propietario_idPropietario = %s;"
            propiedades = self.executeSQL(query, (Propietario_idPropietario,))
            return propiedades

    # TODO: BORRAR Y REEMPLAZAR
    def existe_propiedad_con_id(self, idPropiedad):
        try:
            query = "SELECT * FROM PROPIEDAD p WHERE p.idPropiedad = %s;"
            propiedad = self.executeSQL(query, (idPropiedad,))
            if len(propiedad) > 0:
                return True
            else:
                return False
        except Exception:
            return False

    def obtener_propiedades_por_id_agente(self, idAgente):
        cursor = self.conn.cursor()
        try:
            query_check_agent = "SELECT COUNT(*) FROM agente WHERE idAgente = %s;"
            cursor.execute(query_check_agent, (idAgente,))
            agent_exists = cursor.fetchone()[0]
            if agent_exists == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent with this id was not found")
            # Obtener propiedades
            query = (
                "SELECT p.idPropiedad, p.Propietario_idPropietario, p.direccion, p.imagen, p.firmado "
                "FROM propiedad p "
                "JOIN acceso ac ON p.idPropiedad = ac.Propiedad_idPropiedad "
                "WHERE ac.Agente_idAgente = %s;"
            )
            cursor.execute(query, (idAgente,))
            properties = cursor.fetchall()
            return properties
        except Error as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            cursor.close()

    # FIXME
    def obtener_propietarios_por_id_agente(self, idAgente):
        if not self.existe_agente_con_id(idAgente):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent with this id was not found")
        else:
            query = ("select distinct pr.idPropietario, pr.nombre, pr.correo, pr.genero, pr.contrasennia from "
                     "propietario pr join (select Propietario_idPropietario from propiedad p join (select * from "
                     "agente ag JOIN acceso ac on ag.idAgente = ac.Agente_idAgente where ag.idAgente = %s) acg on "
                     "p.idPropiedad = acg.Propiedad_idPropiedad) aca on pr.idPropietario = "
                     "aca.Propietario_idPropietario;")
            variables = (idAgente,)
            return self.executeSQL(query, variables)

    # TODO: HABITACION

    def obtener_habitacion_por_id(self, idHabitacion: int):
        query = "SELECT * FROM HABITACION h WHERE h.idHabitacion = %s;"
        habitacion = self.executeSQL(query, (idHabitacion,))
        if len(habitacion) > 0:
            return habitacion[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room with this id was not found")

    # FIXME
    def actualizar_habitacion(self, idHabitacion: int, imagen: str, nombre: str, descripcion):
        query = ("UPDATE `keynova`.`habitacion` SET `imagen` = %s,"
                 "`nombre` = %s, `descripcion` = %s WHERE `idHabitacion` = %s;")
        variables = (imagen, nombre, descripcion, idHabitacion)
        self.executeSQL(query, variables)

    # FIXME
    def eliminar_habitacion(self, idHabitacion: int):
        habitacion = (self.obtener_habitacion_por_id(idHabitacion))
        query = "DELETE FROM HABITACION h WHERE h.idHabitacion = %s"
        self.executeSQL(query, (idHabitacion,))
        return habitacion

    # FIXME
    def agregar_habitacion(self, Propiedad_idPropiedad: int, imagen: str, nombre: str, descripcion):
        if not self.existe_propiedad_con_id(Propiedad_idPropiedad):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property with this id was not found")
        else:
            query = "INSERT INTO `keynova`.`habitacion` (`Propiedad_idPropiedad`,`imagen`,`nombre`, `descripcion`) " \
                    "VALUES (%s,%s,%s,%s);"
            if descripcion is None:
                descripcion = "None"
            variables = (int(Propiedad_idPropiedad), imagen, nombre, descripcion)
            self.executeSQL(query, variables)
            query = "SELECT * FROM habitacion ORDER BY idHabitacion DESC LIMIT 1;"
            return self.executeSQL(query)[0]

    # FIXME
    def obtener_habitaciones_por_id_propiedad(self, idPropiedad):
        if not self.existe_propiedad_con_id(idPropiedad):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property with this id was not found")
        else:
            query = "SELECT * FROM HABITACION h WHERE h.Propiedad_idPropiedad = %s;"
            habitaciones = self.executeSQL(query, (idPropiedad,))
            return habitaciones

    # TODO: BORRAR Y REEMPLAZAR
    def existe_habitacion_con_id(self, idHabitacion):
        try:
            query = "SELECT * FROM HABITACION h WHERE h.idHabitacion = %s;"
            room = self.executeSQL(query, (idHabitacion,))
            if len(room) > 0:
                return True
            else:
                return False
        except Exception:
            return False

    # TODO: MUEBLE

    # FIXME
    def obtener_mueble_por_id(self, idMueble: int):
        if not self.existe_mueble_con_id(idMueble):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Furniture with this id was not found")
        else:
            query = "SELECT * FROM MUEBLE m WHERE m.idMueble = %s;"
            mueble = self.executeSQL(query, (idMueble,))
            return mueble[0]

    # TODO: BORRAR Y REEMPLAZAR
    def existe_mueble_con_id(self, idMueble):
        try:
            query = "SELECT * FROM MUEBLE m WHERE m.idMueble = %s;"
            mueble = self.executeSQL(query, (idMueble,))
            print(mueble)
            if len(mueble) > 0:
                return True
            else:
                return False
        except Exception:
            return False

    # FIXME
    def actualizar_mueble(self, idMueble: int, estado: str, imagen: str, descripcion: str,
                          nombre: str):
        query = ("UPDATE `keynova`.`mueble` SET `estado` = %s, `imagen` = %s, "
                 "`descripcion` = %s, `nombre` = %s WHERE `idMueble` = %s;")
        variables = (estado, imagen, descripcion, nombre, idMueble)
        self.executeSQL(query, variables)

    # FIXME
    def eliminar_mueble(self, idMueble: int):
        mueble = self.obtener_mueble_por_id(idMueble)
        query = "DELETE FROM MUEBLE m WHERE m.idMueble = %s"
        self.executeSQL(query, (idMueble,))
        return mueble

    # FIXME
    def agregar_mueble(self, Habitacion_idHabitacion: int, estado: str, imagen: str, descripcion: str, nombre: str):
        if not self.existe_habitacion_con_id(Habitacion_idHabitacion):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room with this id was not found")
        else:
            query = "INSERT INTO `keynova`.`mueble` (`Habitacion_idHabitacion`,`estado`,`imagen`,`descripcion`,`nombre`) " \
                    "VALUES (%s,%s,%s,%s,%s);"
            variables = (int(Habitacion_idHabitacion), estado, imagen, descripcion, nombre)
            self.executeSQL(query, variables)
            query = "SELECT * FROM mueble ORDER BY idMueble DESC LIMIT 1;"
            return self.executeSQL(query)[0]

    # FIXME
    def obtener_muebles_por_id_habitacion(self, Habitacion_idHabitacion):
        if not self.existe_habitacion_con_id(Habitacion_idHabitacion):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room with this id was not found")
        else:
            query = "SELECT * FROM MUEBLE m WHERE m.Habitacion_idHabitacion = %s;"
            mueble = self.executeSQL(query, (Habitacion_idHabitacion,))
            return mueble

    # TODO: MANTENIMIENTO
    def agregar_mantenimiento(self, Propiedad_idPropiedad: int, descripcion: str, fecha: str, Agente_idAgente: int):
        query = ("INSERT INTO `keynova`.`mantenimiento` (`Propiedad_idPropiedad`,`descripcion`,`fecha`,"
                 "`Agente_idAgente`) VALUES (%s,%s,%s,%s);")
        variables = (int(Propiedad_idPropiedad), descripcion, fecha, int(Agente_idAgente))
        self.executeSQL(query, variables)
        query = "SELECT * FROM mantenimiento ORDER BY idMantenimiento DESC LIMIT 1;"
        return self.executeSQL(query)[0]

    # FIXME
    def obtener_mantenimientos_por_id_propiedad(self, Propiedad_idPropiedad):
        if not self.existe_propiedad_con_id(Propiedad_idPropiedad):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property with this id was not found")
        else:
            query = "SELECT * FROM MANTENIMIENTO m WHERE m.Propiedad_idPropiedad = %s;"
            mantenimientos = self.executeSQL(query, (Propiedad_idPropiedad,))
            return mantenimientos

    # FIXME
    def obtener_mantenimientos_por_id_agente_comercial(self, Agente_idAgente):
        if not self.existe_agente_con_id(Agente_idAgente):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent with this id was not found")
        else:
            query = ("select idMantenimiento,Propiedad_idPropiedad,descripcion,fecha,Agente_idAgente from "
                     "mantenimiento m join (select idPropiedad from propiedad p join (select * from agente ag "
                     "JOIN acceso ac on ag.idAgente = ac.Agente_idAgente where ag.idAgente = %s) acg "
                     "on p.idPropiedad = acg.Propiedad_idPropiedad) aca on m.Propiedad_idPropiedad = aca.idPropiedad")
            mantenimientos = self.executeSQL(query, (Agente_idAgente,))
            return mantenimientos

    # FIXME
    def obtener_mantenimientos_por_id_agente_mantenimiento(self, Agente_idAgente):
        if not self.existe_agente_con_id(Agente_idAgente):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent with this id was not found")
        else:
            query = ("select m.idMantenimiento, m.Propiedad_idPropiedad, m.descripcion, m.fecha, m.Agente_idAgente "
                     "from agente a join mantenimiento m on a.idAgente = m.Agente_idAgente where a.idAgente = %s;")
            mantenimientos = self.executeSQL(query, (Agente_idAgente,))
            return mantenimientos

    # FIXME
    def eliminar_mantenimiento(self, idMantenimiento: int):
        mantenimiento = self.obtener_mantenimiento_por_id(idMantenimiento)
        query = "DELETE FROM MANTENIMIENTO m WHERE m.idMantenimiento = %s"
        self.executeSQL(query, (idMantenimiento,))
        return mantenimiento

    def obtener_mantenimiento_por_id(self, idMantenimiento: int):
        query = "SELECT * FROM MANTENIMIENTO m WHERE m.idMantenimiento = %s;"
        mantenimiento = self.executeSQL(query, (idMantenimiento,))
        if len(mantenimiento) > 0:
            return mantenimiento[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Maintenance with this id was not found")

    # TODO: BORRAR Y REEMPLAZAR
    def existe_mantenimiento_con_id(self, idMantenimiento):
        try:
            query = "SELECT * FROM MANTENIMIENTO m WHERE m.idMantenimiento = %s;"
            mantenimiento = self.executeSQL(query, (idMantenimiento,))
            if len(mantenimiento) > 0:
                return True
            else:
                return False
        except Exception:
            return False
    # TODO: INVENTARIO
    # FIXME
    def obtener_inventario_por_id_propiedad(self, Propiedad_idPropiedad):
        if not self.existe_propiedad_con_id(Propiedad_idPropiedad):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property with this id was not found")
        else:
            propiedad = self.obtener_propiedad_por_id(Propiedad_idPropiedad)
            inventario = {"direccion": propiedad[2],
                          "imagen": propiedad[3],
                          "habitaciones": []}
            habitaciones = self.obtener_habitaciones_por_id_propiedad(Propiedad_idPropiedad)
            for habitacion in habitaciones:
                idHabitacion = habitacion[0]
                habitacion = {"imagen": habitacion[2],
                              "nombre": habitacion[3],
                              "descripcion": habitacion[4],
                              "muebles": []}
                muebles = self.obtener_muebles_por_id_habitacion(idHabitacion)
                for mueble in muebles:
                    mueble = {"estado": mueble[2],
                              "imagen": mueble[3],
                              "descripcion": mueble[4],
                              "nombre": mueble[5]}
                    habitacion["muebles"].append(mueble)
                inventario["habitaciones"].append(habitacion)
            return inventario
