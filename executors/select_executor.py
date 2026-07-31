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
            return
        
        print("[SelectExecutor] Abriendo el selector...")
        
        context.driver.click(result)

    def execute(self, action, context):

        print("\n========== SELECT EXECUTOR ==========")
        print(f"tipo             : {action.tipo}")
        print(f"tipo_logico      : {action.tipo_logico}")
        print(f"tipo_componente  : {action.tipo_componente}")
        print(f"field            : {action.field}")
        print(f"texto            : {action.texto}")
        print(f"valor            : {action.valor}")
        print(f"placeholder      : {action.placeholder}")
        print(f"modo             : {action.modo}")
        print(f"id               : {action.id}")
        print("=====================================\n")

        print(f"[SelectExecutor] tipo_componente = {action.tipo_componente}")
        if action.tipo_componente == "input":
            self._abrir_select(action, context)
            return
        if action.tipo_componente == "select":
            print("[SelectExecutor] Abriendo el selector...")
            self._abrir_select(action, context)
            
            opciones = context.page.locator(".ng-dropdown-panel .ng-option")
            cantidad = opciones.count()
            print(f"[SelectExecutor] Cantidad de opciones = {cantidad}")

            for i in range(cantidad):

                opcion = opciones.nth(i)

                texto = opcion.inner_text().strip()

                print("--------------------------------")
                print(texto)

                if texto == action.texto.strip():

                    print(f"[SelectExecutor] Opción encontrada en índice {i}")

                    opcion.click()

                    print("[SelectExecutor] Opción seleccionada")

                    break

            return

        print("[SelectExecutor] Tipo no soportado")