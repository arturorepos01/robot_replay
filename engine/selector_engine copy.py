from locator_strategies.id_strategy import IdStrategy
from locator_strategies.name_strategy import NameStrategy
from locator_strategies.placeholder_strategy import PlaceholderStrategy
from locator_strategies.text_strategy import TextStrategy
from locator_strategies.field_strategy import FieldStrategy

class SelectorEngine:

    def __init__(self):
        self.strategies = [
            IdStrategy(),
            NameStrategy(),
            FieldStrategy(),
            PlaceholderStrategy(),
            TextStrategy(),
        ]

    def find(self, page, action):

        for strategy in self.strategies:
            result = strategy.find(page, action)

            if result:
                return result

        return None