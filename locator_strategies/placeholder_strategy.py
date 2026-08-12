from models.locator_result import LocatorResult

from locator_strategies.selector_strategy import SelectorStrategy


class PlaceholderStrategy(SelectorStrategy):

    def find(self, page, action):

        if not action.placeholder:

            return None

        locator = page.locator(

            f'input[placeholder="{action.placeholder}"]'

        )

        count = locator.count()
        print(f"[PlaceholderStrategy] encontrados = {count}")

        for i in range(count):
            l = locator.nth(i)

            try:
                print(
                    f"{i}: "
                    f"visible={l.is_visible()} "
                    f"enabled={l.is_enabled()} "
                    f"value='{l.input_value()}'"
                )
            except Exception as e:
                print(f"{i}: ERROR {e}")

        # print(f"[PlaceholderStrategy] selector = input[placeholder=\"{action.placeholder}\"]")
        # print(f"[PlaceholderStrategy] encontrados = {count}")

        if count == 0:
            return None

        print(f"[PlaceholderStrategy] index = {action.index}")

        idx = action.index if action.index < count else 0

        return LocatorResult(

            locator=locator.nth(idx),

            strategy="PLACEHOLDER",

            selector=f'input[placeholder="{action.placeholder}"]',

            score=80

        )