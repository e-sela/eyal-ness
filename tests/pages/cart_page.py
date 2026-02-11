
from playwright.sync_api import Page
from ..enums.urls import Urls
from ..utils.price_parser import parsePrice
import logging
import allure

logger = logging.getLogger(__name__)

class CartPage:
    CART_URL = Urls.CART.value

    def __init__(self, page: Page):
        self.page = page
        self.subtotal_selector = "[data-test-id='SUBTOTAL']"
        self.shipping_selector = "[data-test-id='SHIPPING']"
        self.delete_btn_selector = ".number-input__delete"

    @allure.step("Navigate to the cart page")
    def goto(self) -> None:
        self.page.goto(self.CART_URL)

    @allure.step("Get item prices from cart")
    def get_item_prices(self) -> float:
        total_text = self.page.locator(self.subtotal_selector).inner_text()
        return parsePrice(total_text)

    @allure.step("Get shipping price from cart")
    def getShippingPrice(self) -> float:
        if self.page.locator(self.shipping_selector).count() == 0:
            return 0.0
        shipping_text = self.page.locator(self.shipping_selector).inner_text()
        return parsePrice(shipping_text)

    @allure.step("Assert cart total does not exceed maximum allowed")
    def assertCartTotalNotExceeds(self, max_total: float) -> None:
        self.goto()
        self.page.reload()
        subtotal = self.get_item_prices()
        shipping = self.getShippingPrice()
        total_sum = subtotal - shipping
        total_sum = round(total_sum, 2)
        logger.info(f"Subtotal: ${subtotal:.2f}, Shipping: ${shipping:.2f}, Cart total: ${total_sum:.2f}, Max allowed: ${max_total:.2f}")
        screenshot_path = f"cart_total_{int(total_sum)}.png"
        self.page.screenshot(path=screenshot_path, full_page=True)
        logger.info(f"the total actual ${total_sum} the tottal expected ${max_total}")
        if total_sum == max_total:
            logger.info(f"Cart total ${total_sum} equals the maximum allowed ${max_total}. Screenshot saved to {screenshot_path}. Assertion passed.")
            assert True
        else:
            logger.error(f"Cart total ${total_sum} exceeds expected maximum ${max_total}. Screenshot saved to {screenshot_path}")
            assert False, f"Cart total ${total_sum} exceeds expected maximum ${max_total}"

    @allure.step("Delete all items from cart")
    def deleteAll(self) -> None:
        while self.page.locator(self.delete_btn_selector).count() > 0:
            delete_btn = self.page.locator(self.delete_btn_selector).first
            delete_btn.click()
            self.page.wait_for_timeout(1000)
        logger.info("All items deleted from cart")