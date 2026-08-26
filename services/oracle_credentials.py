import oracledb


class OracleCredentials:

    def __init__(self, config):
        self.config = config

    def obtener_credencial_aleatoria(self):
        oracle = self.config["oracle"]
        credenciales = self.config["credenciales_test"]

        tabla = credenciales["tabla"]
        campo_cuenta = credenciales["campo_cuenta"]
        campo_password = credenciales["campo_password"]
        campo_activo = credenciales["campo_activo"]
        grupo = credenciales["grupo"]

        sql = f"""
            SELECT {campo_cuenta}, {campo_password}
            FROM (
                SELECT {campo_cuenta}, {campo_password}
                FROM {tabla}
                WHERE {campo_activo} = 'S'
                  AND GRUPO = :grupo
                ORDER BY DBMS_RANDOM.VALUE
            )
            WHERE ROWNUM = 1
        """

        connection = None

        try:
            connection = oracledb.connect(
                user=oracle["usuario"],
                password=oracle["password"],
                dsn=oracle["dsn"]
            )

            with connection.cursor() as cursor:
                cursor.execute(sql, grupo=grupo)
                row = cursor.fetchone()

                if row is None:
                    raise RuntimeError(
                        f"No existen credenciales activas para el grupo: {grupo}"
                    )

                return {
                    "cuenta": row[0],
                    "contrasena": row[1]
                }

        finally:
            if connection:
                connection.close()