from models.locator_result import LocatorResult

from locator_strategies.selector_strategy import SelectorStrategy


class TextStrategy(SelectorStrategy):

    def find(self, page, action):

        if not action.texto:
            print("[TextStrategy] texto vacío")
            return None

        texto = action.texto.strip()

        # ============================================================
        # BUTTON
        # ============================================================
        if action.tag and action.tag.upper() == "BUTTON":

            locator = page.get_by_role(
                "button",
                name=texto
            )

            print(
                f"[TextStrategy] button '{texto}' count={locator.count()}"
            )

        # ============================================================
        # LINK
        # ============================================================
        elif action.tag and action.tag.upper() == "A":

            locator = page.locator("a").filter(
                has_text=action.texto
            )

            print(
                f"[TextStrategy] link '{action.texto}' "
                f"count={locator.count()}"
            )

            # Mostrar cuáles están realmente visibles
            count = locator.count()

            for i in range(count):
                item = locator.nth(i)

                try:
                    print(
                        f"[TextStrategy] link[{i}] "
                        f"visible={item.is_visible()} "
                        f"text='{item.inner_text().strip()}' "
                        f"href='{item.get_attribute('href')}'"
                    )
                except Exception as e:
                    print(
                        f"[TextStrategy] link[{i}] ERROR: {e}"
                    )

            # Preferir el enlace visible
            visible_locator = None

            for i in range(count):
                item = locator.nth(i)

                try:
                    if item.is_visible():
                        visible_locator = item
                        break
                except Exception:
                    pass

            if visible_locator is None:
                return None

            locator = visible_locator

            # Buscar específicamente un enlace visible
            for i in range(count):

                l = locator.nth(i)

                try:
                    if l.is_visible():
                        print(
                            f"[TextStrategy] USANDO LINK VISIBLE index={i}"
                        )

                        return LocatorResult(
                            locator=l,
                            strategy="TEXT",
                            selector=f'a:has-text("{action.texto}")',
                            score=80
                        )

                except Exception as e:

                    print(
                        f"[TextStrategy] error evaluando "
                        f"link[{i}]: {e}"
                    )

            return None

        # ============================================================
        # OTROS ELEMENTOS
        # ============================================================
        else:

            locator = page.get_by_text(
                texto,
                exact=True
            )

            print(
                f"[TextStrategy] text '{texto}' count={locator.count()}"
            )

        if locator.count() == 0:
            return None

        # ============================================================
        # Buscar el primer elemento visible
        # ============================================================
        count = locator.count()

        for i in range(count):

            candidato = locator.nth(i)

            try:

                if candidato.is_visible():

                    return LocatorResult(

                        locator=candidato,

                        strategy="TEXT",

                        selector=texto,

                        score=60

                    )

            except Exception:
                pass

        print(
            f"[TextStrategy] '{texto}' encontrado pero "
            f"ninguno está visible"
        )

        return None