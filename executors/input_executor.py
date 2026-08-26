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