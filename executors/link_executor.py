from executors.base_executor import BaseExecutor


class ClickExecutor(BaseExecutor):

    def execute(self, action, context):

        print()

        print("CLICK")

        print(action.texto)

        print(action.placeholder)