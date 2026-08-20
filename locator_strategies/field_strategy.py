from models.locator_result import LocatorResult


class FieldStrategy:

    def find(self, page, action):

        if not action.field:
            return None

        selector = f'[formcontrolname="{action.field}"]'
        print(f"[FieldStrategy] selector = {selector}")
        locator = page.locator(selector)
        print(f"[FieldStrategy] encontrados = {locator.count()}")

        if locator.count() == 0:
            return None

        return LocatorResult(
            locator=locator.first,
            strategy="FIELD",
            selector=selector,
            score=90
        )