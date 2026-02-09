from playwright.sync_api import Page
from ..urls import Urls
from ..utils.price_parser import parse_price

class CartPage:
    CART_URL = Urls.CART.value

    def __init__(self, page: Page):
        self.page = page
        self.subtotal_selector = "[data-test-id='SUBTOTAL']"

    def goto(self) -> None:
        self.page.goto(self.CART_URL)

    def get_item_prices(self) -> float:
        total_text = self.page.locator(self.subtotal_selector).inner_text()
        return parse_price(total_text)

    def assert_cart_total_not_exceeds(self, max_total: float) -> None:
        """Asserts that the total price of items in the cart does not exceed the specified maximum total."""
        self.goto()
        total_sum = self.get_item_prices()
        print(f"Cart total: ${total_sum:.2f}, Max allowed: ${max_total:.2f}")
        assert total_sum <= max_total, f"Cart total ${total_sum} exceeds expected maximum ${max_total}"