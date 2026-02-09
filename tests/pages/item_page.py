from playwright.sync_api import Page

class ItemPage:
    def __init__(self, page: Page):
        self.page = page
        self.add_to_cart_btn = "#atcBtn_btn_1"
        self.lightbox_dialog = ".lightbox-dialog__window"

    def addItemsToCart(self, item_links: list[str]):
        for link in item_links:
            #self.page.pause()  # optional debug pause
            self.page.goto(link)
            self.page.wait_for_load_state("networkidle")
            self.page.wait_for_selector(self.add_to_cart_btn, timeout=15000)
            self.page.click(self.add_to_cart_btn)
            #self.addionalService()

    def addionalService(self):
        is_added = self.page.locator(".ux-textspans", has_text="Added to cart").is_visible()
        if is_added:
            see_in_cart_btn = self.page.get_by_role("link", name="See in cart")
            if see_in_cart_btn.count() > 0:
                see_in_cart_btn.click()
                self.page.wait_for_load_state("networkidle")
            return
        if self.page.locator(self.lightbox_dialog).is_visible():
            proceed_btn = self.page.locator(f"{self.lightbox_dialog} button:has-text('Proceed')")
            if proceed_btn.count() > 0:
                proceed_btn.click()
                self.page.wait_for_load_state("networkidle")
