# eyal-ness

## Overview
This project contains automated end-to-end tests for eBay using Playwright and pytest. It includes page object models, utility functions, and Allure reporting for test results.

## Features
- Page Object Model for eBay pages (search, cart, item, login)
- Utilities for price parsing and locator handling
- Logging for traceability and debugging
- Allure reporting integration
- Screenshots for failed assertions
- Git ignores for test artifacts

## Project Structure
```
├── tests/
│   ├── pages/
│   │   ├── cart_page.py
│   │   ├── item_page.py
│   │   ├── login_page.py
│   │   ├── search_page.py
│   ├── utils/
│   │   ├── locator_util.py
│   │   ├── price_parser.py
│   ├── test_e2e_items.py
│   ├── conftest.py
│   ├── pytest.ini
├── allure-results/
├── .gitignore
├── README.md
```

## Setup
1. Create a virtual environment:
   ```sh
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   pip install allure-pytest
   ```
3. (Optional) Install Allure CLI:
   ```sh
   brew install allure
   ```

## Running Tests
Run all tests:
```sh
pytest
```
Run a specific test:
```sh
pytest tests/test_e2e_items.py
```

## Allure Reporting
Generate and view the report:
```sh
allure serve allure-results
```
Or generate static HTML:
```sh
allure generate allure-results -o allure-report --clean
allure open allure-report
```

## How to Run

1. Activate your virtual environment:
   ```sh
   source .venv/bin/activate
   ```

2. Run tests with configurable parameters:
   - To set the search term and price limit, use pytest options or environment variables.
   - Example:
     ```sh
     pytest tests/test_e2e_items.py --search="lego star wars" --limit=5 --max_price=50
     ```
3. To ensure US address and currency:
   - Make sure your test navigates to the US version of eBay (e.g., https://www.ebay.com/).
   - If needed, update the URL in your page objects to use the US site.

4. Handling 'I'm not a robot' CAPTCHA:
   - If a CAPTCHA appears, you must solve it manually in the browser window.
   - The test will pause for manual intervention (using `self.page.pause()` or similar).
   - After solving, resume the test.

5. Allure Reporting:
   - After tests, generate and view the report:
     ```sh
     allure serve allure-results
     ```

## Customization
- The search term and limit are configurable as parameters or environment variables.
- Currency is set by using the US eBay address.
- Manual CAPTCHA handling is required if triggered.

## Notes
- Screenshots and Allure results are ignored by git.
- For Selenium Grid or Moon integration, update your WebDriver endpoint accordingly.

## License
MIT
