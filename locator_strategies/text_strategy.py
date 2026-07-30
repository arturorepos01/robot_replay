from models.locator_result import LocatorResult

from locator_strategies.selector_strategy import SelectorStrategy


class TextStrategy(SelectorStrategy):

    def find(self, page, action):

        if not action.texto:
            print("[TextStrategy] texto vacío")
            return None

        print(f"[TextStrategy] tag={action.tag}")
        print(f"[TextStrategy] texto='{action.texto}'")

        # Si la acción corresponde a un botón, buscar un botón.
        if action.tag and action.tag.upper() == "BUTTON":

            locator = page.get_by_role("button", name=action.texto)
            print(f"[TextStrategy] button count={locator.count()}")

        # Si corresponde a un enlace.
        elif action.tag and action.tag.upper() == "A":

            locator = page.get_by_text(action.texto, exact=True)

            print(f"[TextStrategy] text(exact) count={locator.count()}")
            print(f"[TextStrategy] link count={locator.count()}")

        # Para cualquier otro caso, mantener la búsqueda por texto.
        else:

            locator = page.get_by_text(action.texto)
            print(f"[TextStrategy] text count={locator.count()}")

        if locator.count() == 0:

            return None

        return LocatorResult(

            locator=locator.first,

            strategy="TEXT",

            selector=action.texto,

            score=60

        )