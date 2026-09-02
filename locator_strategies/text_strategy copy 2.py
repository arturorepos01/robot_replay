from models.locator_result import LocatorResult

from locator_strategies.selector_strategy import SelectorStrategy


class TextStrategy(SelectorStrategy):

    def find(self, page, action):

        if not action.texto:
            print("[TextStrategy] texto vacío")
            return None

        # print(f"[TextStrategy] tag={action.tag}")
        # print(f"[TextStrategy] texto='{action.texto}'")

        # Si la acción corresponde a un botón, buscar un botón.
        if action.tag and action.tag.upper() == "BUTTON":

            locator = page.get_by_role("button", name=action.texto)
            # print(f"[TextStrategy] button count={locator.count()}")

        # Si corresponde a un enlace.
        elif action.tag and action.tag.upper() == "A":

            locator = page.get_by_role(
                "link",
                name=action.texto
            )

            count = locator.count()

            print(f"[TextStrategy] link count={count}")

            if count == 0:
                return None

            for i in range(count):

                candidato = locator.nth(i)

                try:
                    print(
                        f"[TextStrategy] link {i}: "
                        f"visible={candidato.is_visible()} "
                        f"enabled={candidato.is_enabled()}"
                    )

                    if candidato.is_visible():
                        print(
                            f"[TextStrategy] usando link visible index={i}"
                        )

                        return LocatorResult(
                            locator=candidato,
                            strategy="LINK",
                            selector=f'link="{action.texto}"',
                            score=93
                        )

                except Exception as e:
                    print(
                        f"[TextStrategy] error evaluando link {i}: {e}"
                    )

            return None
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