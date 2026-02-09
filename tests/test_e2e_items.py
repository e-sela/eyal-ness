import os
import sys
from pathlib import Path
# ensure project root is on sys.path so absolute imports like `tests.*` work
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from playwright.sync_api import Page
from tests.pages.login_page import LoginPage

USERNAME = os.getenv("EBAY_USER", "es342324@gmail.com")
PASSWORD = os.getenv("EBAY_PASS", "eyalNess1")

def test_e2e_add_and_filter_items(page: Page, ebay_user_id: str):
    """Test to verify that the user can identify himself by his user id after signing in"""
    login = LoginPage(page)
    login.sign_in(USERNAME, PASSWORD)
    login.verify_user_id(ebay_user_id)
