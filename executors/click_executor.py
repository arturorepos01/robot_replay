from engine.action_executor import ActionExecutor


class ClickExecutor(ActionExecutor):

    def __init__(self):
        super().__init__()

    def execute(self, action, context):

        result = self.locate(action, context)

        if result is None:
            print("[ClickExecutor] Selector pendiente de implementar")
            return

        locator = result.locator

        # ---------------------------------------------------------
        # Obtener href antes del click, si existe
        # ---------------------------------------------------------
        href = None

        try:
            href = locator.get_attribute("href")
        except Exception:
            pass

        print(
            f"[ClickExecutor] strategy={result.strategy} "
            f"selector={result.selector} "
            f"href={href}"
        )

        # ---------------------------------------------------------
        # Click
        # ---------------------------------------------------------
        context.driver.click(result)

        # ---------------------------------------------------------
        # Si el elemento tiene href, esperar navegación SPA
        # ---------------------------------------------------------
        if href and href not in ("", "None", "javascript:void(0);"):

            print(
                f"[ClickExecutor] Esperando navegación hacia: {href}"
            )

            try:

                if href.startswith("/"):
                    expected_url = f"**{href}"
                else:
                    expected_url = href

                context.page.wait_for_url(
                    expected_url,
                    timeout=10000
                )

                print(
                    f"[ClickExecutor] Navegación completada: "
                    f"{context.page.url}"
                )

            except Exception as e:

                print(
                    f"[ClickExecutor] "
                    f"No se confirmó navegación hacia {href}: {e}"
                )