# scraper.py
from playwright.sync_api import sync_playwright

def extract_job(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Extracting job from url: ", url)
        page.goto(url, timeout=60000)

        # Wait for content to load
        page.wait_for_load_state("networkidle", timeout=60000)

        # Try common job description selectors
        selectors = [
            "[class*='description']",
            "[class*='job']",
            "[id*='description']",
            "article",
            "main"
        ]

        content = None

        for sel in selectors:
            try:
                element = page.locator(sel).first
                text = element.inner_text(timeout=10000)
                if len(text) > 200:  # basic quality check
                    content = text
                    break
            except:
                continue

        # Fallback: get full page text
        if not content:
            content = page.locator("body").inner_text(timeout=15000)

        browser.close()

        return {
            "url": url,
            "description": clean_text(content)
        }


def clean_text(text: str):
    return "\n".join(
        line.strip() for line in text.splitlines() if line.strip()
    )