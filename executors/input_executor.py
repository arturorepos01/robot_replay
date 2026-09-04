from engine.action_executor import ActionExecutor

class InputExecutor(ActionExecutor):

    def __init__(self):
        super().__init__()

    def execute(self, action, context):

        result = self.locate(action, context)

        if result is None:
            print("[InputExecutor] No se encontró el campo")
            return

        valor = action.valor

        # ---------------------------------------------------------
        # SELECT_SEARCH
        # El ng-select YA fue abierto por SelectExecutor.
        # Aquí solamente escribimos en su input interno.
        # ---------------------------------------------------------
        if action.tipo_logico == "select_search":
            print(
                f"[InputExecutor] SELECT_SEARCH: "
                f"field='{action.field}' valor='{valor}'"
            )

            # result es LocatorResult.
            # result.locator es el <ng-select>.
            ng_select = result.locator

            # Dentro del ng-select está el input real de búsqueda.
            search_input = ng_select.locator(".ng-input input")

            encontrados = search_input.count()

            print(
                f"[InputExecutor] SELECT_SEARCH input interno encontrados = "
                f"{encontrados}"
            )

            if encontrados == 0:
                raise Exception(
                    f"No se encontró el input interno de búsqueda "
                    f"del ng-select '{action.field}'"
                )

            search_input = search_input.first

            search_input.click()
            search_input.fill("")
            search_input.type(valor, delay=50)

            print(
                f"[InputExecutor] SELECT_SEARCH escrito = '{valor}'"
            )

            return

        # ---------------------------------------------------------
        # INPUT NORMAL
        # ---------------------------------------------------------

        placeholder = (action.placeholder or "").strip().lower()

        if context.credentials:

            if "rut con dígito verificador" in placeholder:
                valor = context.credentials["cuenta"]

            elif placeholder == "contraseña":
                valor = context.credentials["contrasena"]

        if placeholder == "contraseña":
            print("[InputExecutor] Llenando: ********")
        else:
            print(f"[InputExecutor] Llenando: {valor}")

        context.driver.fill(result, valor)

        result.locator.press("Tab")