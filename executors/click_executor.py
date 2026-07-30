from engine.action_executor import ActionExecutor


class ClickExecutor(ActionExecutor):

    def __init__(self):

        super().__init__()


    def execute(self, action, context):

        result = self.locate(action, context)

        print(f"[ClickExecutor] result = {result}")
        print(f"[ClickExecutor] tipo = {type(result)}")

        if result is None:

            print("[ClickExecutor] Selector pendiente de implementar")

            return

        print("[ClickExecutor] Antes del click")

        context.driver.click(result)

        print("[ClickExecutor] Después del click")