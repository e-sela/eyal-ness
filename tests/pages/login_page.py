
from playwright.sync_api import Page
from tests.urls import Urls
from tests.utils.locator_util import LocatorUtil
import allure

class LoginPage:
    @allure.step("Initialize LoginPage with page")
    def __init__(self, page: Page):
        self.page = page
        self.locator_util = LocatorUtil(page)
        self.sign_in_link = [".gh-identity a:has-text('Sign in')"]
        self.userid = "#userid"
        self.continue_btn = ["#signin-continue-btn", "button:has-text('Continue')"]
        self.password = "#pass"
        self.signin_btn = ["#sgnBt", "button:has-text('Sign in')"]
        self.identity = ".gh-identity"
        self.identity_dialog_user = ".gh-identity__dialog .gh-identity-signed-in__user-ratings a"

    @allure.step("Navigate to the eBay homepage")
    def goto(self):
        self.page.goto(Urls.EBAY.value)

    @allure.step("Open sign-in form")
    def open_signin(self):
        self.locator_util.clickFirstAvailable(self.sign_in_link)
        self.page.wait_for_timeout(3000)
        self.page.wait_for_selector(self.userid, timeout=15000)

    @allure.step("Login with username and password")
    def login(self, username: str, password: str):
        self.page.fill(self.userid, username)
        self.locator_util.clickFirstAvailable(self.continue_btn)
        self.page.wait_for_selector(self.password, timeout=15000)
        self.page.fill(self.password, password)
        self.locator_util.clickFirstAvailable(self.signin_btn)

    @allure.step("Sign in with username and password")
    def sign_in(self, username: str, password: str):
        self.goto()
        self.open_signin()
        self.login(username, password)

    @allure.step("Verify logged-in user ID matches expected")
    def verify_user_id(self, userId: str):
        self.page.wait_for_timeout(3000)
        self.page.locator(self.identity).hover()
        user_link = self.page.locator(self.identity_dialog_user).first
        self.page.press("body", "Escape")
        assert userId in user_link.inner_text()
        
        