class Dispatcher:

    def __init__(self):
        self.executors = {}

    def register(self, tipo, executor):
        self.executors[tipo] = executor

    def dispatch(self, action, context):

        print(
            f"[Dispatcher] tipo={action.tipo}  tipo_logico={action.tipo_logico}"
        )

        # Las búsquedas internas de un ng-select son INPUT.
        if action.tipo_logico == "select_search":
            executor_key = "input"

        # El resto mantiene la lógica original:
        # select -> SelectExecutor
        # click  -> ClickExecutor
        # input  -> InputExecutor
        else:
            executor_key = action.tipo_logico or action.tipo

        print(f"[Dispatcher] executor_key = {executor_key}")

        executor = self.executors.get(executor_key)

        if executor is None:
            raise Exception(
                f"No existe executor registrado para '{executor_key}'"
            )

        print(
            f"[Dispatcher] ejecutando executor = "
            f"{executor.__class__.__name__}"
        )

        executor.execute(action, context)