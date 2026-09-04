import oracledb

from models.action import Action


class OracleReplayLoader:

    def __init__(self, config):
        self.config = config

    def _connect(self):
        oracle = self.config["oracle"]

        return oracledb.connect(
            user=oracle["usuario"],
            password=oracle["password"],
            dsn=oracle["dsn"],
        )

    def obtener_flow(self, id_flow):
        sql = """
            SELECT
                ID_FLOW,
                FLOW_ID,
                NOMBRE
            FROM ROBOT_FLOW
            WHERE ID_FLOW = :id_flow
              AND ACTIVO = 'S'
        """

        connection = None

        try:
            connection = self._connect()

            with connection.cursor() as cursor:
                cursor.execute(sql, id_flow=id_flow)
                row = cursor.fetchone()

                if row is None:
                    raise RuntimeError(
                        f"No existe un ROBOT_FLOW activo "
                        f"para ID_FLOW={id_flow}"
                    )

                return {
                    "id_flow": row[0],
                    "flow_id": row[1],
                    "nombre": row[2],
                }

        finally:
            if connection:
                connection.close()

    def obtener_acciones(self, id_flow):
        sql_acciones = """
            SELECT
                ID_ACCION,
                ID_FLOW,
                SECUENCIA,
                TIPO,
                TIPO_LOGICO,
                TIPO_COMPONENTE,
                MODO,
                TAG,
                TEXTO,
                VALOR,
                FIELD,
                PLACEHOLDER,
                ID_ELEMENTO,
                NAME_ELEMENTO,
                CLASE,
                CONTAINER_TAG,
                CONTAINER_CLASS,
                URL,
                FECHA_EVENTO,
                ES_PASSWORD
            FROM ROBOT_ACCION
            WHERE ID_FLOW = :id_flow
            ORDER BY SECUENCIA
        """

        sql_datos = """
            SELECT
                ID_DATO,
                ID_ACCION,
                NOMBRE,
                VALOR,
                ES_SENSIBLE,
                TIPO_DATO
            FROM ROBOT_ACCION_DATO
            WHERE ID_ACCION = :id_accion
            ORDER BY ID_DATO
        """

        connection = None

        try:
            connection = self._connect()

            acciones = []

            with connection.cursor() as cursor:

                cursor.execute(
                    sql_acciones,
                    id_flow=id_flow,
                )

                rows = cursor.fetchall()

                for row in rows:

                    (
                        id_accion,
                        row_id_flow,
                        secuencia,
                        tipo,
                        tipo_logico,
                        tipo_componente,
                        modo,
                        tag,
                        texto,
                        valor,
                        field,
                        placeholder,
                        id_elemento,
                        name_elemento,
                        clase,
                        container_tag,
                        container_class,
                        url,
                        timestamp,
                        es_password,
                    ) = row

                    # -------------------------------------------------
                    # Datos persistidos de la acción
                    # -------------------------------------------------

                    cursor.execute(
                        sql_datos,
                        id_accion=id_accion,
                    )

                    datos = cursor.fetchall()

                    datos_accion = []

                    for dato in datos:
                        (
                            id_dato,
                            dato_id_accion,
                            nombre,
                            dato_valor,
                            es_sensible,
                            tipo_dato,
                        ) = dato

                        datos_accion.append(
                            {
                                "id_dato": id_dato,
                                "id_accion": dato_id_accion,
                                "nombre": nombre,
                                "valor": dato_valor,
                                "es_sensible": es_sensible,
                                "tipo_dato": tipo_dato,
                            }
                        )

                    # -------------------------------------------------
                    # Determinar valor persistido
                    # -------------------------------------------------

                    valor_persistido = valor

                    for dato in datos_accion:

                        if dato["nombre"] != "valor":
                            continue

                        # Un valor sensible puede estar almacenado
                        # como ******. Nunca lo utilizamos como
                        # contraseña real.
                        if dato["es_sensible"] == "S":
                            continue

                        valor_persistido = dato["valor"]

                    # -------------------------------------------------
                    # container_tag / container_class
                    #
                    # No existen en las columnas que hemos confirmado
                    # de ROBOT_ACCION. No inventamos valores.
                    # -------------------------------------------------

                    # container_tag = None
                    # container_class = None

                    # -------------------------------------------------
                    # Construcción EXACTA del modelo Action
                    # utilizado por JsonLoader.
                    # -------------------------------------------------

                    accion = Action(
                        flow_id=row_id_flow,
                        tipo=tipo,
                        tipo_logico=tipo_logico,
                        tipo_componente=tipo_componente,
                        modo=modo,
                        tag=tag,
                        texto=texto,
                        valor=valor_persistido,
                        field=field,
                        placeholder=placeholder,
                        id=id_elemento,
                        name=name_elemento,
                        clase=clase,
                        url=url,
                        timestamp=timestamp,
                        container_tag=container_tag,
                        container_class=container_class,
                        index=0,
                    )

                    # Guardamos la secuencia fuera de Action para
                    # poder auditarla durante las pruebas.
                    accion._oracle_id_accion = id_accion
                    accion._oracle_secuencia = secuencia
                    accion._oracle_datos = datos_accion

                    acciones.append(accion)

            return acciones

        finally:
            if connection:
                connection.close()

    def load(self, id_flow):
        flow = self.obtener_flow(id_flow)

        acciones = self.obtener_acciones(
            flow["id_flow"]
        )

        return flow, acciones