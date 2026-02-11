import random
from .enums.Items_search_terms import ItemsSearchTerm
import os

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
    search_term = random.choice(list(ItemsSearchTerm)).value
    max_price = random.randint(50, 200)
    limit = random.randint(3, 8)
    items, total_price = search.searchItemsByNameUnderPrice(search_term, max_price=max_price, limit=limit)
    item = ItemPage(page)
    item.addItemsToCart(items)
    cart = CartPage(page)
    cart.assertCartTotalNotExceeds(total_price)