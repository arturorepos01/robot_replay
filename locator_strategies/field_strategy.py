from models.locator_result import LocatorResult


class FieldStrategy:

    def find(self, page, action):

        if not action.field:
            return None

        selector = f'[field="{action.field}"]'

        locator = page.locator(selector)

        if locator.count() == 0:
            return None

        return LocatorResult(
            locator=locator.first,
            strategy="FIELD",
            selector=selector,
            score=90
        )