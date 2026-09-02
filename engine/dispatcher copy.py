class Dispatcher:

    def __init__(self):

        self.executors = {}

    def register(self, tipo, executor):

        self.executors[tipo] = executor

    def dispatch(self, action, context):

        print(
            f"[Dispatcher] tipo={action.tipo}  tipo_logico={action.tipo_logico}"
        )

        executor_key = action.tipo_logico or action.tipo

        executor = self.executors.get(executor_key)

        if executor is None:

            raise Exception(

                f"No existe executor registrado para '{tipo}'"

            )

        executor.execute(action, context)