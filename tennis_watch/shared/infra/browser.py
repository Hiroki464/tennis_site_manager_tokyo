# shared/infra/browser.py
from playwright.sync_api import sync_playwright


class BrowserSession:
    def __init__(self, headless: bool):
        self.headless = headless
        self.p = None
        self.browser = None
        self.page = None

    def __enter__(self):
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch(headless=self.headless)
        self.page = self.browser.new_page()
        return self

    def __exit__(self, exc_type, exc, tb):
        try:
            if self.browser:
                self.browser.close()
        finally:
            if self.p:
                self.p.stop()