from models.locator_result import LocatorResult
from locator_strategies.selector_strategy import SelectorStrategy


class LinkStrategy(SelectorStrategy):

    def find(self, page, action):

        if not action.texto:
            return None

        if not action.tag or action.tag.upper() != "A":
            return None

        texto = action.texto.strip()

        locator = page.get_by_role(
            "link",
            name=texto,
            exact=True
        )

        count = locator.count()

        print(
            f"[LinkStrategy] link '{texto}' count={count}"
        )

        # Buscar específicamente un enlace visible
        for i in range(count):

            candidato = locator.nth(i)

            try:
                visible = candidato.is_visible()

                print(
                    f"[LinkStrategy] {i}: "
                    f"visible={visible}"
                )

                if visible:
                    return LocatorResult(
                        locator=candidato,
                        strategy="LINK",
                        selector=f'role=link[name="{texto}"]',
                        score=95
                    )

            except Exception as e:

                print(
                    f"[LinkStrategy] {i}: ERROR {e}"
                )

        return None