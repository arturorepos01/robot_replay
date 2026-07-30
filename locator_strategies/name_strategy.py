from models.locator_result import LocatorResult

from locator_strategies.selector_strategy import SelectorStrategy


class NameStrategy(SelectorStrategy):

    def find(self, page, action):

        if not action.name:

            return None

        locator = page.locator(

            f'[name="{action.name}"]'

        )

        if locator.count() == 0:

            return None

        return LocatorResult(

            locator=locator.first,

            strategy="NAME",

            selector=f'[name="{action.name}"]',

            score=90

        )