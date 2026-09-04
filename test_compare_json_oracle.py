import json
import sys
from pathlib import Path
from datetime import datetime, date


PROJECT_ROOT = Path(__file__).resolve().parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from loader.json_loader import JsonLoader
from services.oracle_replay_loader import OracleReplayLoader


ID_FLOW = 34
JSON_FILE = PROJECT_ROOT / "user_actions.json"


FIELDS = [
    "tipo",
    "tipo_logico",
    "tipo_componente",
    "modo",
    "tag",
    "texto",
    "valor",
    "field",
    "placeholder",
    "id",
    "name",
    "clase",
    "url",
    "timestamp",
    "container_tag",
    "container_class",
]


def normalize(value):
    """
    Normaliza únicamente para poder comparar representaciones
    equivalentes sin modificar los objetos originales.
    """

    if isinstance(value, datetime):
        # Oracle entrega datetime sin zona horaria.
        # El JSON utiliza ISO-8601 con 'Z' (UTC).
        # Para la comparación eliminamos diferencias de formato:
        # - zona Z
        # - ceros finales de microsegundos
        result = value.isoformat(timespec="milliseconds")
        return result + "Z"

    if isinstance(value, date):
        return value.isoformat()

    # if value is None:
    #     return ""
    return value
    # return str(value)

def display_value(value):
    """
    Representación inequívoca para diagnóstico.
    """

    if value is None:
        return "<NULL>"

    if value == "":
        return "<EMPTY>"

    return repr(value)

def is_sensitive(action):
    """
    Determina si la acción contiene un dato sensible.
    """

    if getattr(action, "tipo_componente", None) == "password":
        return True

    if getattr(action, "field", None):
        field = str(action.field).lower()

        if "password" in field:
            return True

    if getattr(action, "placeholder", None):
        placeholder = str(action.placeholder).lower()

        if "password" in placeholder:
            return True

    for dato in getattr(action, "_oracle_datos", []):
        if dato.get("es_sensible") == "S":
            return True

    return False


def safe_value(action):
    if is_sensitive(action):
        return "********"

    return normalize(getattr(action, "valor", None))


def compare_field(json_action, oracle_action, field):

    json_has_field = hasattr(json_action, field)
    oracle_has_field = hasattr(oracle_action, field)

    if not json_has_field or not oracle_has_field:

        return {
            "status": "ERROR",
            "json": (
                getattr(json_action, field)
                if json_has_field
                else "<ATRIBUTO_INEXISTENTE>"
            ),
            "oracle": (
                getattr(oracle_action, field)
                if oracle_has_field
                else "<ATRIBUTO_INEXISTENTE>"
            ),
        }

    if field == "valor":

        json_sensitive = is_sensitive(json_action)
        oracle_sensitive = is_sensitive(oracle_action)

        if json_sensitive or oracle_sensitive:

            return {
                "status": "SENSITIVE",
                "json": "<OCULTO>",
                "oracle": "<OCULTO>",
            }

    left = normalize(getattr(json_action, field))
    right = normalize(getattr(oracle_action, field))

    if left == right:

        return {
            "status": "OK",
            "json": left,
            "oracle": right,
        }

    # Diferencia NULL vs cadena vacía.
    if (
        (left is None and right == "")
        or
        (left == "" and right is None)
    ):

        return {
            "status": "WARNING",
            "json": left,
            "oracle": right,
        }

    return {
        "status": "ERROR",
        "json": left,
        "oracle": right,
    }


def main():

    if not JSON_FILE.exists():
        raise FileNotFoundError(
            f"No se encontró: {JSON_FILE}"
        )

    with JSON_FILE.open(
        "r",
        encoding="utf-8",
    ) as f:
        json_data = json.load(f)

    config_path = PROJECT_ROOT / "config.json"

    with config_path.open(
        "r",
        encoding="utf-8",
    ) as f:
        config = json.load(f)

    # ---------------------------------------------------------------
    # Cargar JSON
    # ---------------------------------------------------------------

    json_loader = JsonLoader()

    json_actions = json_loader.load(
        str(JSON_FILE)
    )

    # ---------------------------------------------------------------
    # Cargar Oracle
    # ---------------------------------------------------------------

    oracle_loader = OracleReplayLoader(config)

    flow, oracle_actions = oracle_loader.load(
        ID_FLOW
    )

    # ---------------------------------------------------------------
    # Cabecera
    # ---------------------------------------------------------------

    print("=" * 100)
    print("COMPARACIÓN JSON vs ORACLE")
    print("=" * 100)

    print(f"JSON              : {JSON_FILE.name}")
    print(f"ID_FLOW Oracle     : {ID_FLOW}")
    print(f"FLOW_ID Oracle     : {flow['flow_id']}")
    print(f"Acciones JSON      : {len(json_actions)}")
    print(f"Acciones Oracle    : {len(oracle_actions)}")

    # ---------------------------------------------------------------
    # Validación del FLOW_ID
    # ---------------------------------------------------------------

    json_flow_id = getattr(json_actions[0], "flow_id", None)

    if str(json_flow_id) != str(flow["flow_id"]):
        print()
        print("ERROR - FLOW_ID diferente")
        print(f"   JSON   = {json_flow_id!r}")
        print(f"   ORACLE = {flow['flow_id']!r}")

        raise AssertionError(
            "JSON.flow_id no coincide con ROBOT_FLOW.FLOW_ID"
        )

    print()
    print("OK - JSON.flow_id coincide con ROBOT_FLOW.FLOW_ID")

    # ---------------------------------------------------------------
    # Cantidad
    # ---------------------------------------------------------------

    if len(json_actions) != len(oracle_actions):

        print()
        print("ERROR - Cantidad de acciones diferente")

        raise AssertionError(
            "JSON y Oracle tienen distinta cantidad de acciones"
        )

    print()
    print("OK - Misma cantidad de acciones")

    # ---------------------------------------------------------------
    # Comparación
    # ---------------------------------------------------------------

    total_ok = 0
    total_warnings = 0
    total_errors = 0

    for index, (json_action, oracle_action) in enumerate(
        zip(json_actions, oracle_actions),
        start=1,
    ):

        diferencias = []

        for field in FIELDS:

            resultado = compare_field(
                json_action,
                oracle_action,
                field,
            )

            if resultado["status"] != "OK":

                diferencias.append(
                    (
                        field,
                        resultado["status"],
                        resultado["json"],
                        resultado["oracle"],
                    )
                )

    # ---------------------------------------------------------------
    # VALIDACIÓN DEL ORDEN DE EJECUCIÓN
    # ---------------------------------------------------------------

    seq_oracle = getattr(
        oracle_action,
        "_oracle_secuencia",
        None,
    )

    if seq_oracle is None:

        print(
            f"[INFO] Acción #{index}: "
            "_oracle_secuencia no disponible"
        )

    elif seq_oracle != index:

        diferencias.append(
            (
                "secuencia",
                "ERROR",
                index,
                seq_oracle,
            )
        )

    # ---------------------------------------------------------------
    # VALIDACIÓN DE ID_ACCION
    # ---------------------------------------------------------------

    id_accion = getattr(
        oracle_action,
        "_oracle_id_accion",
        None,
    )

    if id_accion is None:

        print(
            f"[INFO] Acción #{index}: "
            "_oracle_id_accion no disponible"
        )

    # ---------------------------------------------------------------
    # PROCESAR RESULTADO DE LA ACCIÓN
    # ---------------------------------------------------------------

    if diferencias:

        accion_tiene_error = False
        accion_tiene_warning = False

        for field, status, left, right in diferencias:

            if status == "ERROR":
                accion_tiene_error = True

            elif status == "WARNING":
                accion_tiene_warning = True

        if accion_tiene_error:
            total_errors += 1

        elif accion_tiene_warning:
            total_warnings += 1

        print()
        print(
            f"[{('ERROR' if accion_tiene_error else 'WARNING')}] "
            f"Acción #{index} "
            f"| SEQ={seq_oracle} "
            f"| ID_ACCION={id_accion}"
        )

        for field, status, left, right in diferencias:
            print(
                f"   {field} [{status}]"
            )
            print(
                f"      JSON   = {display_value(left)}"
            )
            print(
                f"      ORACLE = {display_value(right)}"
            )

    else:

        total_ok += 1

    # ---------------------------------------------------------------
    # Resultado
    # ---------------------------------------------------------------

    print()
    print("=" * 100)
    print("RESULTADO")
    print("=" * 100)

    print(
        f"Acciones comparadas : {len(json_actions)}"
    )

    print(
        f"Acciones OK         : {total_ok}"
    )

    print(
        f"Acciones WARNING     : {total_warnings}"
    )

    print(
        f"Acciones ERROR       : {total_errors}"
    )

    if total_errors == 0:

        print()
        if total_warnings == 0:

            print(
                "OK - JSON y Oracle producen Action[] "
                "equivalente para replay"
            )

        else:

            print(
                "OK CON ADVERTENCIAS - "
                "No existen diferencias funcionales, "
                "pero existen diferencias de representación."
            )

    else:

        print()
        print(
            "ATENCIÓN - Existen diferencias que debemos resolver "
            "antes de conectar Oracle al Dispatcher."
        )

        sys.exit(1)

    print()
    print(
        "La prueba NO abre Chrome."
    )
    print(
        "La prueba NO ejecuta el Dispatcher."
    )
    print("=" * 100)


if __name__ == "__main__":
    main()
