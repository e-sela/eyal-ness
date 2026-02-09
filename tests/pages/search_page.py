import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from playwright.sync_api import Page

class SearchPage:
    def __init__(self, page: Page):
        self.page = page
        self.search_input = "#gh-ac"
        self.search_btn = "#gh-btn"
        self.results_container = ".s-result-item"
        self.max_price_input = ".x-textrange__input input[aria-label='Maximum Value in $']"
        self.apply_filter_btn = "button[title='Submit price range']"

    def search(self, search_text: str, max_price: int = None, limit: int = 5) -> list[str]:
        self.page.fill(self.search_input, search_text)
        self.page.click(self.search_btn)
        self.page.wait_for_selector(self.results_container, timeout=15000)
        
        if max_price:
            self.page.fill(self.max_price_input, str(max_price))
            self.page.click(self.apply_filter_btn)
            self.page.wait_for_timeout(2000)

    def verify_search_results_displayed(self):
        results = self.page.locator(self.results_container)
        assert results.count() > 0, "No search results found"