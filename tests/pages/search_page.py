import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from playwright.sync_api import Page
from ..utils.price_parser import parse_price

class SearchPage:
    def __init__(self, page: Page):
        self.page = page
        self.search_input = "#gh-ac"
        self.search_btn = "#gh-search-btn"
        self.card = ".s-card[id^='item']"
        self.view_options_btn = ".srp-view-options .fake-menu-button__button"
        self.lightbox_dialog = ".lightbox-dialog__window"

    def searchItemsByNameUnderPrice(self, search_text: str, max_price: int = None, limit: int = 5) -> tuple[list[str], float]:
        self.page.fill(self.search_input, search_text)
        self.page.click(self.search_btn)
        self.setView()
        if max_price:
            self.page.get_by_label("Maximum value").fill(str(max_price))
            self.page.get_by_label("Maximum value").press("Enter")
            self.page.wait_for_timeout(2000)

        itamUrls: list[str] = []
        totalPrice: float = 0.0
        cards = self.page.locator(self.card)
        count = min(cards.count(), limit)
        for i in range(count):
            item = cards.nth(i)
            price_text = item.locator(".s-card__price").inner_text()
            price_value = parse_price(price_text)
            print(f"Item {i+1}: price={price_value}")
            if price_value > max_price:
                assert False, f"Item {i+1} price ${price_value} exceeds max price ${max_price}"
            
            with self.page.context.expect_page() as new_page_info:
                item.click()
            new_page = new_page_info.value
            itamUrl = new_page.url
            new_page.close()
            
            if itamUrl:
                itamUrls.append(itamUrl)
                totalPrice += price_value

        return itamUrls, round(totalPrice, 2)
    
    def setView(self) -> None:
        """Set the search results view to the specified view name (e.g. 'List', 'Gallery')."""
        self.convertPricesToUSD()
    
    def convertPricesToUSD(self) -> None:
        """Click view options, verify dialog appears, and check 'Convert prices to USD' if not already checked."""
        self.page.locator(self.view_options_btn).click()
        self.page.get_by_label("Customize").click()
        self.page.get_by_test_id("cust_fcpd-1").set_checked(False)
        
            
        
