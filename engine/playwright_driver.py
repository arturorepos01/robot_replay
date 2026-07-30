class PlaywrightDriver:

    def click(self, locator_result):

        locator = locator_result.locator

        print("[PlaywrightDriver] Esperando botón habilitado...")
        locator.wait_for(state="visible")

        print("[PlaywrightDriver] enabled =", locator.is_enabled())
        print("===== ELEMENTO =====")
        print(locator.evaluate("""
        (el) => ({
            tag: el.tagName,
            id: el.id,
            className: el.className,
            type: el.type,
            disabled: el.disabled,
            outerHTML: el.outerHTML
        })
        """))
        print("====================")
        locator.click()

        page = locator.page

        page.wait_for_timeout(1000)

        print("[PlaywrightDriver] URL =", page.url)

        try:
            error = page.locator(".alert, .alert-danger, .invalid-feedback, .toast, .mat-error").all_inner_texts()
            if error:
                print("[PlaywrightDriver] Mensajes:", error)
        except Exception:
            pass

        texto = page.locator("body").inner_text()

        print("========== CUERPO DE LA PÁGINA ==========")
        print(texto[:1000])
        print("========================================")

    def fill(self, locator_result, valor):

        print(f"[PlaywrightDriver] fill('{valor}')")

        locator = locator_result.locator

        locator.wait_for(state="visible")

        locator.fill(valor)

        valor_actual = locator.input_value()

        print(f"[PlaywrightDriver] valor leído = '{valor_actual}'")

        print("[PlaywrightDriver] fill OK")

    def type(self, locator_result, valor):

        locator_result.locator.type(valor)

    def press(self, locator_result, tecla):

        locator_result.locator.press(tecla)