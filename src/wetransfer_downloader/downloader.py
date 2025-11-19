import logging
from pathlib import Path
from playwright.sync_api import sync_playwright

logger = logging.getLogger(__name__)

class WeTransferDownloader:

    def __init__(self, output_dir="downloads", headless=True):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.headless = headless

    def download(self, link: str):
        logger.info(f"Opening: {link}")

        with sync_playwright() as pw:
            browser = pw.chromium.launch(
                headless=self.headless,
                args=["--no-sandbox", "--disable-gpu"]
            )
            context = browser.new_context(accept_downloads=True)
            page = context.new_page()

            page.goto(link)
            page.wait_for_url("**/downloads/**", timeout=20000)
            page.wait_for_load_state("networkidle")

            # Cookie acceptance
            try:
                page.locator("button:has-text('Accept')").click(timeout=4000)
            except:
                pass

            # Pre-download buttons
            for sel in [
                "button:has-text('I accept')",
                "button:has-text('I understand')",
                "button:has-text('Agree')",
            ]:
                try:
                    p = page.locator(sel)
                    p.wait_for(timeout=4000)
                    p.click()
                    break
                except:
                    pass

            # Download button
            dl_button = None
            for sel in [
                "[data-testid='download-transfer-button']",
                "button:has-text('Download')",
                "button:has-text('Download all')",
                "button:has-text('Get files')",
            ]:
                try:
                    locator = page.locator(sel).first
                    locator.wait_for(timeout=8000)
                    dl_button = locator
                    break
                except:
                    pass

            if not dl_button:
                raise RuntimeError("Could not find the Download button.")

            with page.expect_download() as info:
                dl_button.click()

            dl = info.value
            destination = self.output_dir / dl.suggested_filename
            dl.save_as(destination)

            browser.close()
            return destination
