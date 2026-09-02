import json
import sys
from pathlib import Path
from datetime import datetime, date


PROJECT_ROOT = Path(__file__).resolve().parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from loader.json_loader import JsonLoader
from services.oracle_replay_loader import OracleReplayLoader


ID_FLOW = 6
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

    if value is None:
        return ""

    return str(value)


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
    if field == "valor":
        left = safe_value(json_action)
        right = safe_value(oracle_action)

        # En una acción sensible no comparamos la representación
        # real del secreto.
        if is_sensitive(json_action) or is_sensitive(oracle_action):
            return True, left, right

    else:
        left = normalize(getattr(json_action, field, None))
        right = normalize(getattr(oracle_action, field, None))

    return left == right, left, right


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
    total_diferencias = 0

    for index, (json_action, oracle_action) in enumerate(
        zip(json_actions, oracle_actions),
        start=1,
    ):

        diferencias = []

        for field in FIELDS:

            ok, left, right = compare_field(
                json_action,
                oracle_action,
                field,
            )

            if not ok:
                diferencias.append(
                    (
                        field,
                        left,
                        right,
                    )
                )

        seq_oracle = getattr(
            oracle_action,
            "_oracle_secuencia",
            None,
        )

        id_accion = getattr(
            oracle_action,
            "_oracle_id_accion",
            None,
        )

        if diferencias:

            total_diferencias += 1

            print()
            print(
                f"[DIFERENCIA] Acción #{index} "
                f"| SEQ={seq_oracle} "
                f"| ID_ACCION={id_accion}"
            )

            for field, left, right in diferencias:

                # Nunca exponer secretos.
                if field == "valor":
                    left = "********"
                    right = "********"

                print(
                    f"   {field}:"
                )
                print(
                    f"      JSON   = {left!r}"
                )
                print(
                    f"      ORACLE = {right!r}"
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
        f"Acciones con cambios: {total_diferencias}"
    )

    if total_diferencias == 0:

        print()
        print(
            "OK - JSON y Oracle producen Action[] equivalente"
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
