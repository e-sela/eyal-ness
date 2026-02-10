
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from tests.utils.locator_util import LocatorUtil

from playwright.sync_api import Page
from ..utils.price_parser import parse_price
import logging
import allure

logger = logging.getLogger(__name__)

class SearchPage:
    @allure.step("Initialize SearchPage with page")
    def __init__(self, page: Page):
        self.page = page
        self.locator_util = LocatorUtil(page)
        self.search_input = "#gh-ac"
        self.search_btn = ["#gh-search-btn"]
        self.card = ".s-card[id^='item']"
        self.view_options_btn = [".srp-view-options .fake-menu-button__button"]
        self.lightbox_dialog = ".lightbox-dialog__window"

    @allure.step("Search items by name under price")
    def searchItemsByNameUnderPrice(self, search_text: str, max_price: int = None, limit: int = 5) -> tuple[list[str], float]:
        self.page.fill(self.search_input, search_text)
        self.locator_util.click_first_available(self.search_btn)
        self.page.wait_for_selector(self.card, timeout=10000)
        if max_price:
            self.page.get_by_label("Maximum value").fill(str(max_price))
            self.page.get_by_label("Maximum value").press("Enter")
        self.setView()
        itamUrls: list[str] = []
        totalPrice: float = 0.0
        cards = self.page.locator(self.card)
        count = min(cards.count(), limit)
        for i in range(count):
            item = cards.nth(i)
            price_text = item.locator(".s-card__price").inner_text()
            price_value = parse_price(price_text)
            logger.info(f"Item {i+1}: price={price_value}")
            if price_value > max_price:
                logger.error(f"Item {i+1} price ${price_value} exceeds max price ${max_price}")
                assert False, f"Item {i+1} price ${price_value} exceeds max price ${max_price}"

            with self.page.context.expect_page() as new_page_info:
                item.click()
            new_page = new_page_info.value
            itamUrl = new_page.url
            new_page.close()

            if itamUrl:
                itamUrls.append(itamUrl)
                totalPrice += price_value
                logger.info(f"Added item {i+1} URL: {itamUrl}, price: ${price_value:.2f}")

        return itamUrls, round(totalPrice, 2)
    
    @allure.step("Set search results view")
    def setView(self) -> None:
        # Wait for the view options button to be visible and enabled
        self.page.wait_for_selector(self.view_options_btn[0], state="visible", timeout=5000)
        self.locator_util.click_first_available(self.view_options_btn)
        # Wait for the Gallery View span to be attached and visible
        gallery_view_span = self.page.locator(".fake-menu-button__item span", has_text="Gallery View")
        gallery_view_span.wait_for(state="visible", timeout=5000)
        if gallery_view_span.count() > 0:
            gallery_view_span.first.click()
            # Wait for the page to load after clicking Gallery View
            self.page.wait_for_load_state("networkidle")
        
        
            
        
