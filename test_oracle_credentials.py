import json

from services.oracle_credentials import OracleCredentials


with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)


oracle = OracleCredentials(config)

credenciales = oracle.obtener_credencial_aleatoria()


print("Cuenta seleccionada:", credenciales["cuenta"])
print("Contraseña seleccionada: ********")