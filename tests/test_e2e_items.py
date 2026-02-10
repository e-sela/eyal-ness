import os
import sys
from pathlib import Path

from playwright.sync_api import Page
from .pages.cart_page import CartPage
from .pages.item_page import ItemPage
from .pages.search_page import SearchPage
from .pages.login_page import LoginPage

USERNAME = os.getenv("EBAY_USER", "es342324@gmail.com")
PASSWORD = os.getenv("EBAY_PASS", "eyalNess1")

def test_e2e_add_and_filter_items(page: Page, ebay_user_id: str):
    """Test to verify that the user can identify himself by his user id after signing in"""
    login = LoginPage(page)
    login.sign_in(USERNAME, PASSWORD)
    login.verify_user_id(ebay_user_id)
    search = SearchPage(page)
    items, total_price = search.searchItemsByNameUnderPrice("frozen lego duplo", max_price=50, limit=3)
    item = ItemPage(page)
    item.addItemsToCart(items)
    cart = CartPage(page)
    cart.assert_cart_total_not_exceeds(total_price)