from playwright.sync_api import Page
from tests.urls import Urls

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.sign_in_link = ".gh-identity a:has-text('Sign in')"
        self.userid = "#userid"
        self.continue_btn = "#signin-continue-btn, button:has-text('Continue')"
        self.password = "#pass"
        self.signin_btn = "#sgnBt, button:has-text('Sign in')"
        self.identity = ".gh-identity"
        self.identity_dialog_user = ".gh-identity__dialog .gh-identity-signed-in__user-ratings a"

    def goto(self):
        self.page.goto(Urls.EBAY.value)

    def open_signin(self):
        self.page.locator(self.sign_in_link).click()
        self.page.wait_for_timeout(3000)
        self.page.wait_for_selector(self.userid, timeout=15000)

    def login(self, username: str, password: str):
        self.page.fill(self.userid, username)
        self.page.click(self.continue_btn)
        self.page.wait_for_selector(self.password, timeout=15000)
        self.page.fill(self.password, password)
        self.page.click(self.signin_btn)

    def sign_in(self, username: str, password: str):
        self.goto()
        self.open_signin()
        self.login(username, password)

    def verify_user_id(self, userId: str):
        self.page.wait_for_timeout(3000)
        self.page.locator(self.identity).hover()
        user_link = self.page.locator(self.identity_dialog_user).first
        assert userId in user_link.inner_text()