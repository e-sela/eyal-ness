import pytest
from .pages.cart_page import CartPage

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
    }

def pytest_configure(config):
    # This forces headless to False programmatically
    config.option.headed = True

@pytest.fixture
def ebay_user_id():
    return "es34-4529"

@pytest.fixture(autouse=True)
def cleanup_cart(page):
    """Auto cleanup cart after each test"""
    yield
    cart = CartPage(page)
    try:
        cart.deleteAll()
    except Exception:
        pass