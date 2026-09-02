from engine.selector_engine import SelectorEngine


class ActionExecutor:

    def __init__(self):

        self.selector = SelectorEngine()

    def locate(self, action, context):

        print(f"[ActionExecutor] page = {context.page}")

        return self.selector.find(

            context.page,

            action

        )