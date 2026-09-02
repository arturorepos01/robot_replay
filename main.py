import time
# nuevo inicio
import json
# nuevo fin
from loader.json_loader import JsonLoader
from engine.dispatcher import Dispatcher
from executors.click_executor import ClickExecutor
from executors.input_executor import InputExecutor
from executors.select_executor import SelectExecutor
from models.replay_context import ReplayContext
# nuevo inicio
from services.oracle_credentials import OracleCredentials
# nuevo fin
from playwright.sync_api import sync_playwright
from driver import Driver

loader = JsonLoader()

acciones = loader.load("user_actions.json")

ctx = ReplayContext()
# nuevo inicio
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

credential_service = OracleCredentials(config)

ctx.credentials = credential_service.obtener_credencial_aleatoria()

# print("[Oracle] Cuenta de prueba seleccionada:", ctx.credentials["cuenta"])
# print("[Oracle] Contraseña obtenida: ********")
# nuevo fin

# ctx.driver = Driver(ctx.page)
playwright = sync_playwright().start()
browser = playwright.chromium.launch(
    channel="chrome",
    headless=False
)
ctx.browser = browser
ctx.page = browser.new_page()
# Ahora sí existe la página
ctx.driver = Driver(ctx.page)
print(ctx.page)
print(ctx.driver.page)

# ctx.page.goto("https://unijud-qa.pjud.cl/login")
ctx.page.goto("https://unijud-test.pjud.cl/login")

dispatcher = Dispatcher()
dispatcher.register("click", ClickExecutor())
dispatcher.register("input", InputExecutor())
dispatcher.register("select", SelectExecutor())

for i, accion in enumerate(acciones, start=1):

    # print("\n" + "=" * 80)
    # print(f"[REPLAY] ACCIÓN {i}")
    # print("=" * 80)

    # print(
    #     f"tipo={accion.tipo} "
    #     f"logico={accion.tipo_logico} "
    #     f"componente={accion.tipo_componente} "
    #     f"texto='{accion.texto}' "
    #     f"valor='{accion.valor}' "
    #     f"id='{accion.id}' "
    #     f"field='{accion.field}'"
    # )

    # print(f"[REPLAY] URL ANTES = {ctx.page.url}")

    dispatcher.dispatch(accion, ctx)

    time.sleep(3)

    # print(f"[REPLAY] URL DESPUÉS = {ctx.page.url}")