from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import expect


class Driver:

    def __init__(self, page, logger=None):
        print(f"[Driver] page = {page}")
        self.page = page
        self.logger = logger

    def wait_enabled(self, locator):
        expect(locator).to_be_enabled()

    def stabilize(self):
        self.page.wait_for_timeout(200)

    def click(self, locator_result):
        locator = locator_result.locator
        self.wait_visible(locator)
        self.wait_enabled(locator)
        try:
            self.scroll_into_view(locator)
        except Exception:
            pass
        try:
            
            locator.click()
        except PlaywrightTimeoutError:
            locator.click(force=True)
        # print(self.page.content()[:2000])
        # print("[Driver] Esperando networkidle...")
        try:
            self.page.wait_for_load_state("networkidle", timeout=5000)
            # print("[Driver] networkidle OK")
        except PlaywrightTimeoutError:
            print("[Driver] networkidle TIMEOUT")
        # print(f"[Driver] URL actual = {self.page.url}")
        self.stabilize()
        self.page.wait_for_timeout(1500)

    def fill(self, locator_result, value):
        locator = locator_result.locator

        self.wait_visible(locator)
        self.wait_enabled(locator)

        try:
            self.scroll_into_view(locator)
        except Exception:
            pass

        locator.click()
        locator.fill("")
        locator.type(value, delay=50)
        self.page.wait_for_timeout(3000)
        print("Valor después de 3 segundos:", locator.input_value())
        print("Valor leído:", locator.input_value())
        # locator.press("Tab")

        self.stabilize()

    def wait_visible(self, locator, timeout=10000):
        locator.wait_for(
            state="visible",
            timeout=timeout
        )

    def scroll_into_view(self, locator):
        locator.scroll_into_view_if_needed()