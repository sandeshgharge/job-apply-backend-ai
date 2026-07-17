# scraper.py
from services.browser_service import browser_manager

async def extract_job(url: str):
    # Open a new tab/page on the shared browser instance
    page = await browser_manager.new_page()

    try:
        print("Extracting job from url: ", url)
        await page.goto(url, timeout=60000)

        # Wait for content to load
        await page.wait_for_load_state("networkidle", timeout=60000)

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
                text = await element.inner_text(timeout=10000)
                if len(text) > 200:  # basic quality check
                    content = text
                    break
            except:
                continue

        # Fallback: get full page text
        if not content:
            content = await page.locator("body").inner_text(timeout=15000)

        return {
            "url": url,
            "description": clean_text(content)
        }
    finally:
        # Always close the page (not the shared browser)
        await page.close()



def clean_text(text: str):
    return "\n".join(
        line.strip() for line in text.splitlines() if line.strip()
    )