from loader.json_loader import JsonLoader
from engine.dispatcher import Dispatcher
from executors.click_executor import ClickExecutor
from executors.input_executor import InputExecutor
from executors.select_executor import SelectExecutor
from models.replay_context import ReplayContext
from playwright.sync_api import sync_playwright
from driver import Driver


loader = JsonLoader()

acciones = loader.load("user_actions.json")

ctx = ReplayContext()

ctx.driver = Driver(ctx.page)
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

ctx.page.goto("https://unijud-qa.pjud.cl/login")

dispatcher = Dispatcher()
dispatcher.register("click", ClickExecutor())
dispatcher.register("input", InputExecutor())
dispatcher.register("select", SelectExecutor())

for i, accion in enumerate(acciones, start=1):

    print("=" * 70)
    print(f"Acción {i}")
    print(f"tipo            : {accion.tipo}")
    print(f"tipo_logico     : {accion.tipo_logico}")
    print(f"tipo_componente : {accion.tipo_componente}")
    print(f"texto           : {accion.texto}")
    print(f"placeholder     : {accion.placeholder}")
    print(f"valor           : {accion.valor}")
    print(f"field           : {accion.field}")
    print(f"tag             : {accion.tag}")

    dispatcher.dispatch(accion, ctx)

    if accion.tag == "BUTTON" and accion.texto == "INICIAR SESIÓN":
        print("\n==============================")
        print("LOGIN EJECUTADO")
        print("==============================")
        input("Revisa el navegador y luego presiona ENTER...")