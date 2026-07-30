from dataclasses import dataclass
from playwright.sync_api import Locator


@dataclass
class LocatorResult:
    locator: Locator
    strategy: str
    selector: str
    score: float = 1.0