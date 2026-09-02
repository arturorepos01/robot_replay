import json
import time

from services.oracle_credentials import OracleCredentials
from loader.json_loader import JsonLoader
from models.replay_context import ReplayContext
from engine.dispatcher import Dispatcher
from executors.click_executor import ClickExecutor
from executors.input_executor import InputExecutor
from executors.select_executor import SelectExecutor

from playwright.sync_api import sync_playwright
from driver import Driver


print("=" * 80)
print("PRUEBA ROBOT_REPLAY + ORACLE")
print("=" * 80)


# ----------------------------------------------------------------------
# 1. CONFIGURACIÓN
# ----------------------------------------------------------------------

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)


# ----------------------------------------------------------------------
# 2. OBTENER CREDENCIAL DESDE ORACLE
# ----------------------------------------------------------------------

credential_service = OracleCredentials(config)

credentials = credential_service.obtener_credencial_aleatoria()

print()
print("[TEST] Cuenta obtenida desde Oracle:")
print("       ", credentials["cuenta"])
print("[TEST] Contraseña obtenida desde Oracle: ********")
print()


# ----------------------------------------------------------------------
# 3. CREAR CONTEXTO DEL REPLAY
# ----------------------------------------------------------------------

ctx = ReplayContext()

ctx.credentials = credentials


# ----------------------------------------------------------------------
# 4. CARGAR ACCIONES DEL ROBOT
# ----------------------------------------------------------------------

loader = JsonLoader()

acciones = loader.load("user_actions.json")

print("[TEST] Acciones cargadas:", len(acciones))
print()


# ----------------------------------------------------------------------
# 5. INICIAR PLAYWRIGHT
# ----------------------------------------------------------------------

playwright = sync_playwright().start()

browser = playwright.chromium.launch(
    channel="chrome",
    headless=False
)

ctx.browser = browser

ctx.page = browser.new_page()

ctx.driver = Driver(ctx.page)


# ----------------------------------------------------------------------
# 6. REGISTRAR EXECUTORS
# ----------------------------------------------------------------------

dispatcher = Dispatcher()

dispatcher.register("click", ClickExecutor())
dispatcher.register("input", InputExecutor())
dispatcher.register("select", SelectExecutor())

# ----------------------------------------------------------------------
# 7. ABRIR LOGIN
# ----------------------------------------------------------------------

ctx.page.goto("https://unijud-qa.pjud.cl/login")

print("[TEST] URL inicial:", ctx.page.url)
print()


# ----------------------------------------------------------------------
# 8. EJECUTAR SOLAMENTE LAS ACCIONES DEL LOGIN
# ----------------------------------------------------------------------

for i, accion in enumerate(acciones[:32], start=1):

    print("-" * 80)
    print(f"[TEST] ACCIÓN {i}")
    print("-" * 80)

    print("tipo       =", accion.tipo)
    print("logico     =", accion.tipo_logico)
    print("componente =", accion.tipo_componente)
    print("texto      =", accion.texto)
    print("field      =", accion.field)
    print("placeholder=", accion.placeholder)

    dispatcher.dispatch(accion, ctx)

    time.sleep(1)


# ----------------------------------------------------------------------
# 9. VERIFICAR QUE EL USUARIO DE ORACLE FUE INGRESADO
# ----------------------------------------------------------------------

usuario = ctx.page.get_by_placeholder(
    "Rut con dígito verificador"
)

if usuario.count() > 0:

    valor_usuario = usuario.input_value()

    print()
    print("=" * 80)
    print("VERIFICACIÓN")
    print("=" * 80)

    print("Oracle :", credentials["cuenta"])
    print("Pantalla:", valor_usuario)

    if valor_usuario == credentials["cuenta"]:
        print()
        print("[OK] El usuario de Oracle fue ingresado correctamente.")
    else:
        print()
        print("[ERROR] El usuario de Oracle NO coincide.")


print()
print("URL FINAL:", ctx.page.url)
print()
print("Prueba terminada.")
# input("Presiona ENTER para cerrar...")

browser.close()
playwright.stop()