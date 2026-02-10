from typing import List, Optional
from playwright.sync_api import Page

class LocatorUtil:
    """Try a list of selectors and click the first one that works.

    Stops after a successful click.
    """
    def __init__(self, page: Page):
        self.page = page

    def click_first_available(self, selectors: List[str], timeout: int = 500) -> None:
        for sel in selectors:
            locator = self.page.locator(sel)
            try:
                if locator.count() == 0:
                    continue
                locator.first.wait_for(state="visible", timeout=timeout)
                if not locator.first.is_enabled():
                    continue
                locator.first.click()
                break
            except Exception:
                continue