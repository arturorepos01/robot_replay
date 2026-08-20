from engine.action_executor import ActionExecutor


class InputExecutor(ActionExecutor):

    def __init__(self):
        super().__init__()

    def execute(self, action, context):

        result = self.locate(action, context)

        if result is None:
            print("[InputExecutor] No se encontró el campo")
            return

        print(f"[InputExecutor] Llenando: {action.valor}")

        context.driver.fill(result, action.valor)
        result.locator.press("Tab")
