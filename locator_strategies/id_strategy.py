from models.locator_result import LocatorResult

from locator_strategies.selector_strategy import SelectorStrategy


class IdStrategy(SelectorStrategy):

    def find(self, page, action):

        if not action.id:

            return None

        locator = page.locator(f"#{action.id}")

        if locator.count() == 0:

            return None

        return LocatorResult(

            locator=locator.first,

            strategy="ID",

            selector=f"#{action.id}",

            score=100

        )