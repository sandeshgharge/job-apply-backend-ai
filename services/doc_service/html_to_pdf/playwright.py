# services/pdf_service.py

from fastapi import Request
from services.browser_service import browser_manager


class PdfService:

    @staticmethod
    async def html_to_pdf(
        html: str
    ) -> bytes:


        browser = browser_manager.browser

        page = await browser.new_page()

        await page.set_content(
            html,
            wait_until="networkidle"
        )

        pdf_bytes = await page.pdf(
            format="A4",
            print_background=True
        )

        await page.close()

        return pdf_bytes