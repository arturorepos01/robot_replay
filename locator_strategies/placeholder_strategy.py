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