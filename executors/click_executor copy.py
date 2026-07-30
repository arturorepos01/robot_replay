from engine.action_executor import ActionExecutor

from engine.playwright_driver import PlaywrightDriver


class ClickExecutor(ActionExecutor):

    def __init__(self):

        super().__init__()

        self.driver = PlaywrightDriver()

    def execute(self, action, context):

        result = self.locate(

            action,

            context

        )

        if result is None:

            raise Exception(

                "Elemento no encontrado"

            )

        self.driver.click(result)