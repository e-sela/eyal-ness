from playwright.sync_api import Page
from ..urls import Urls
from ..utils.price_parser import parse_price

class CartPage:
    CART_URL = Urls.CART.value

    def __init__(self, page: Page):
        self.page = page
        self.subtotal_selector = "[data-test-id='SUBTOTAL']"
        self.shipping_selector = "[data-test-id='SHIPPING']"
        self.delete_btn_selector = ".number-input__delete"

    def goto(self) -> None:
        self.page.goto(self.CART_URL)

    def get_item_prices(self) -> float:
        total_text = self.page.locator(self.subtotal_selector).inner_text()
        return parse_price(total_text)

    def get_shipping_price(self) -> float:
        if self.page.locator(self.shipping_selector).count() == 0:
            return 0.0
        shipping_text = self.page.locator(self.shipping_selector).inner_text()
        return parse_price(shipping_text)

    def assert_cart_total_not_exceeds(self, max_total: float) -> None:
        """Asserts that the total price of items in the cart does not exceed the specified maximum total."""
        self.goto()
        subtotal = self.get_item_prices()
        shipping = self.get_shipping_price()
        total_sum = subtotal - shipping
        print(f"Subtotal: ${subtotal:.2f}, Shipping: ${shipping:.2f}, Cart total: ${total_sum:.2f}, Max allowed: ${max_total:.2f}")
        assert total_sum <= max_total, f"Cart total ${total_sum} exceeds expected maximum ${max_total}"

    def deleteAll(self) -> None:
        """Delete all items from cart by clicking delete button for each item."""
        while self.page.locator(self.delete_btn_selector).count() > 0:
            delete_btn = self.page.locator(self.delete_btn_selector).first
            delete_btn.click()
            self.page.wait_for_timeout(1000)  # wait for item to be removed
        print("All items deleted from cart")