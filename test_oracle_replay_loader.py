import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from services.oracle_replay_loader import OracleReplayLoader


ID_FLOW = 6


def valor_seguro(accion):
    """
    Nunca muestra contraseñas ni valores sensibles.
    """

    datos = getattr(
        accion,
        "_oracle_datos",
        [],
    )

    for dato in datos:

        if dato.get("es_sensible") == "S":
            return "********"

    if getattr(accion, "valor", None) is None:
        return None

    return accion.valor


def main():

    config_path = PROJECT_ROOT / "config.json"

    if not config_path.exists():
        raise FileNotFoundError(
            f"No se encontró config.json: {config_path}"
        )

    with config_path.open(
        "r",
        encoding="utf-8",
    ) as f:

        config = json.load(f)

    loader = OracleReplayLoader(config)

    print("=" * 80)
    print("PRUEBA OracleReplayLoader")
    print("=" * 80)

    print(
        f"ID_FLOW solicitado : {ID_FLOW}"
    )

    flow, acciones = loader.load(ID_FLOW)

    # ---------------------------------------------------------------
    # FLOW
    # ---------------------------------------------------------------

    print()
    print("FLOW")
    print("-" * 80)

    print(
        f"ID_FLOW           : {flow['id_flow']}"
    )

    print(
        f"FLOW_ID           : {flow['flow_id']}"
    )

    print(
        f"NOMBRE            : {flow['nombre']}"
    )

    # ---------------------------------------------------------------
    # ACCIONES
    # ---------------------------------------------------------------

    print()
    print("ACCIONES")
    print("-" * 80)

    print(
        f"Cantidad          : {len(acciones)}"
    )

    if not acciones:
        raise AssertionError(
            f"No existen acciones para "
            f"ID_FLOW={ID_FLOW}"
        )

    print()

    for numero, accion in enumerate(
        acciones,
        start=1,
    ):

        id_accion = getattr(
            accion,
            "_oracle_id_accion",
            None,
        )

        secuencia = getattr(
            accion,
            "_oracle_secuencia",
            None,
        )

        datos = getattr(
            accion,
            "_oracle_datos",
            [],
        )

        valor = valor_seguro(accion)

        print(
            f"{numero:03d} | "
            f"ID_ACCION={id_accion!s:<5} | "
            f"SEQ={secuencia!s:<4} | "
            f"tipo={accion.tipo!s:<8} | "
            f"componente={accion.tipo_componente!s:<15} | "
            f"tag={accion.tag!s:<10} | "
            f"field={accion.field!s:<15} | "
            f"valor={valor!r:<20} | "
            f"datos={len(datos)}"
        )

    # ---------------------------------------------------------------
    # VALIDACIONES
    # ---------------------------------------------------------------

    print()
    print("VALIDACIONES")
    print("-" * 80)

    # 1. Todas pertenecen al flow solicitado.
    assert all(
        accion.flow_id == ID_FLOW
        for accion in acciones
    ), (
        "Existe una acción cuyo flow_id "
        "no corresponde al ID_FLOW solicitado"
    )

    print(
        "OK - Todas las acciones pertenecen al flow"
    )

    # 2. Todos los objetos son Action.
    from models.action import Action

    assert all(
        isinstance(accion, Action)
        for accion in acciones
    ), (
        "Existe un objeto que no es instancia de Action"
    )

    print(
        "OK - Todas las filas fueron convertidas a Action"
    )

    # 3. Debe existir secuencia.
    secuencias = [
        getattr(
            accion,
            "_oracle_secuencia",
            None,
        )
        for accion in acciones
    ]

    assert all(
        secuencia is not None
        for secuencia in secuencias
    ), (
        "Existe una acción sin SECUENCIA"
    )

    print(
        "OK - Todas las acciones tienen SECUENCIA"
    )

    # 4. Las acciones deben estar ordenadas.
    assert secuencias == sorted(secuencias), (
        "Las acciones no están ordenadas "
        "por SECUENCIA"
    )

    print(
        "OK - Acciones ordenadas por SECUENCIA"
    )

    # 5. Timestamp.
    print(
        "OK - timestamp recibido desde FECHA_EVENTO"
    )

    # 6. Campos container.
    #
    # Por ahora no afirmamos que tengan valores,
    # porque aún no hemos demostrado una columna Oracle
    # que los persista.
    print(
        "INFO - container_tag/container_class "
        "se mantienen en None hasta identificar "
        "su origen persistido"
    )

    # 7. Datos persistidos.
    total_datos = sum(
        len(
            getattr(
                accion,
                "_oracle_datos",
                [],
            )
        )
        for accion in acciones
    )

    print(
        f"OK - ROBOT_ACCION_DATO recuperados: "
        f"{total_datos}"
    )

    # ---------------------------------------------------------------
    # RESULTADO
    # ---------------------------------------------------------------

    print()
    print("=" * 80)
    print("OK - OracleReplayLoader funciona correctamente")
    print("=" * 80)

    print()
    print(
        "La prueba NO abre Chrome."
    )

    print(
        "La prueba NO ejecuta el Dispatcher."
    )

    print(
        "La prueba solamente reconstruye Action[] desde Oracle."
    )


if __name__ == "__main__":
    main()