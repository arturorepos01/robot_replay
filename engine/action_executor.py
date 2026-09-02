from engine.selector_engine import SelectorEngine


class ActionExecutor:

    def __init__(self):

        self.selector = SelectorEngine()

    def locate(self, action, context):

        print(f"[ActionExecutor] page = {context.page}")
        print(
            "[ActionExecutor] "
            f"tipo={action.tipo} "
            f"logico={action.tipo_logico} "
            f"componente={action.tipo_componente} "
            f"tag={action.tag} "
            f"texto={action.texto!r} "
            f"valor={action.valor!r} "
            f"id={action.id!r} "
            f"name={action.name!r} "
            f"field={action.field!r} "
            f"placeholder={action.placeholder!r}"
        )

        return self.selector.find(
            context.page,
            action
        )