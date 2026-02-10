from playwright.sync_api import Page
from ..utils.locator_util import LocatorUtil
import allure

class ItemPage:

    def __init__(self, page: Page):
        self.page = page
        self.add_to_cart_btn = ["#atcBtn_btn_1", "button:has-text('Add to cart')", "button:has-text('Add to basket')"]
        self.lightbox_dialog = ".lightbox-dialog__window"

    @allure.step("Add items to cart")
    def addItemsToCart(self, item_links: list[str]):
        for link in item_links:
            self.page.goto(link)
            self.page.wait_for_load_state("networkidle")
            self.page.wait_for_selector(self.add_to_cart_btn[0], timeout=15000)
            LocatorUtil(self.page).click_first_available(self.add_to_cart_btn)
            self.click_see_in_cart()
    
    @allure.step("Click 'See in cart' if present")
    def click_see_in_cart(self):
        see_in_cart_span = self.page.locator("span.ux-call-to-action__text", has_text="See in cart")
        if see_in_cart_span.count() > 0:
            see_in_cart_span.first.click()
            self.page.wait_for_load_state("networkidle")
