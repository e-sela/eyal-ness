
from typing import List
from playwright.sync_api import Page
import logging
import allure

logger = logging.getLogger(__name__)

class LocatorUtil:
    """Try a list of selectors and click the first one that works.

    Stops after a successful click.
    """
    @allure.step("Initialize LocatorUtil with page")
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Click first available selector")
    def click_first_available(self, selectors: List[str], timeout: int = 500) -> None:
        for sel in selectors:
            locator = self.page.locator(sel)
            try:
                if locator.count() == 0:
                    logger.debug(f"Selector '{sel}' not found on page.")
                    continue
                locator.first.wait_for(state="visible", timeout=timeout)
                if not locator.first.is_enabled():
                    logger.debug(f"Selector '{sel}' is not enabled.")
                    continue
                locator.first.click()
                logger.info(f"Successfully clicked selector: {sel}")
                return
            except Exception as e:
                logger.warning(f"Failed to click selector '{sel}': {e}")
                continue
        logger.error("No selectors were successfully clicked.")