from engine.action_executor import ActionExecutor


class SelectExecutor(ActionExecutor):

    def __init__(self):
        super().__init__()

    def _abrir_select(self, action, context):

        print("[SelectExecutor] Buscando control...")

        result = self.locate(action, context)

        print(f"[SelectExecutor] LocatorResult = {result}")

        if result:
            print(f"[SelectExecutor] strategy = {result.strategy}")
            print(f"[SelectExecutor] selector = {result.selector}")

        print(f"[SelectExecutor] result = {result}")

        if result is None:
            print("[SelectExecutor] No se encontró el select")
            return None

        print(f"[SelectExecutor] URL = {context.page.url}")

        print("[SelectExecutor] Abriendo el selector...")

        locator = result.locator
        print(locator.evaluate("""
            (el) => ({
                display: getComputedStyle(el).display,
                visibility: getComputedStyle(el).visibility,
                width: el.offsetWidth,
                height: el.offsetHeight
            })
            """))
        try:
            contenedor = locator.locator(".ng-select-container")

            print(
                "[SelectExecutor] ng-select-container encontrados =",
                contenedor.count()
            )

            contenedor.click(timeout=5000)
            # Para ng-select hacemos clic sobre el contenedor visible
            # locator.locator(".ng-select-container").click(timeout=5000)
        except Exception as e:

            print("\n" + "=" * 80)
            print("ERROR AL ABRIR EL NG-SELECT")
            print("Tipo:", type(e).__name__)
            print("Mensaje:", e)
            print("=" * 80 + "\n")

            locator = result.locator
            if result.selector == "#tipPersona":

                print("[SelectExecutor] Capturando pantalla antes de abrir tipPersona...")

                context.page.screenshot(
                    path="antes_tipPersona.png",
                    full_page=True
                )
            
            # locator.wait_for(state="attached", timeout=10000)
            contenedor = locator.locator(".ng-select-container")
            contenedor.wait_for(state="visible", timeout=10000)

            context.page.wait_for_function(
                """
                (el) => {
                    const r = el.getBoundingClientRect();
                    return r.width > 0 && r.height > 0;
                }
                """,
                arg=locator.element_handle(),
                timeout=10000
            )

            # context.driver.click(result)
            contenedor.click(timeout=5000)

        context.page.wait_for_selector(
            ".ng-dropdown-panel",
            state="visible",
            timeout=10000
        )

        return result

    def execute(self, action, context):

        # print("\n========== SELECT EXECUTOR ==========")
        # print(f"tipo             : {action.tipo}")
        # print(f"tipo_logico      : {action.tipo_logico}")
        # print(f"tipo_componente  : {action.tipo_componente}")
        # print(f"field            : {action.field}")
        # print(f"texto            : {action.texto}")
        # print(f"valor            : {action.valor}")
        # print(f"placeholder      : {action.placeholder}")
        # print(f"modo             : {action.modo}")
        # print(f"id               : {action.id}")
        # print("=====================================\n")

        # print(f"[SelectExecutor] tipo_componente = {action.tipo_componente}")
        if action.tipo_componente == "input":
            self._abrir_select(action, context)
            return
        if action.tipo_componente == "select":
            print("[SelectExecutor] Abriendo el selector...")
            self._abrir_select(action, context)
            
            opciones = context.page.locator(".ng-dropdown-panel .ng-option")
            cantidad = opciones.count()
            # print(f"[SelectExecutor] Cantidad de opciones = {cantidad}")

            for i in range(cantidad):

                opcion = opciones.nth(i)

                texto = opcion.inner_text().strip()

                # print("--------------------------------")
                # print(texto)

                if texto == action.texto.strip():

                    # print(f"[SelectExecutor] Opción encontrada en índice {i}")

                    opcion.click()

                    context.page.wait_for_selector(
                        ".ng-dropdown-panel",
                        state="hidden",
                        timeout=10000
                    )

                    context.page.wait_for_timeout(300)

                    print("[SelectExecutor] Opción seleccionada")

                    break

            return

        print("[SelectExecutor] Tipo no soportado")