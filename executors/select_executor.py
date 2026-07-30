from engine.action_executor import ActionExecutor


class SelectExecutor(ActionExecutor):

    def __init__(self):
        super().__init__()

    def _abrir_select(self, action, context):
        result = self.locate(action, context)
        print(f"[SelectExecutor] result = {result}")
        if result is None:
            print("[SelectExecutor] No se encontró el select")
            return
        context.driver.click(result)

    def execute(self, action, context):
        print(f"[SelectExecutor] tipo_componente = {action.tipo_componente}")
        if action.tipo_componente == "input":
            self._abrir_select(action, context)
            return
        if action.tipo_componente == "select":
            print("[SelectExecutor] Seleccionar opción")
            return

        print("[SelectExecutor] Tipo no soportado")