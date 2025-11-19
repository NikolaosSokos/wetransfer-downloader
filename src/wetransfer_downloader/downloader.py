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

            # 1. Open the short link
            logger.info("Navigating to short link…")
            page.goto(link)

            # 2. Wait for redirect to the real download page
            logger.info("Waiting for redirect to /downloads/... page…")
            page.wait_for_url("**/downloads/**", timeout=20000)
            logger.info(f"Redirected to: {page.url}")

            # 3. Wait for React UI to load
            page.wait_for_load_state("networkidle")

            # 4. Handle cookie popup
            try:
                page.locator("button:has-text('Accept')").click(timeout=6000)
                logger.info("Cookie popup closed.")
            except:
                pass

            # 5. Handle “I accept” or pre-download confirmation
            pre_accept = [
                "button:has-text('I accept')",
                "button:has-text('I agree')",
                "button:has-text('I understand')",
                "button:has-text('Accept and continue')",
            ]

            for sel in pre_accept:
                try:
                    btn = page.locator(sel)
                    btn.wait_for(timeout=4000)
                    btn.click()
                    logger.info(f"Clicked pre-download button: {sel}")
                    break
                except:
                    pass

            # 6. Find the real Download button
            selectors = [
                "[data-testid='download-transfer-button']",
                "button:has-text('Download')",
                "button:has-text('Download all')",
                "button:has-text('Get files')",
                "a:has-text('Download')",
            ]

            download_button = None

            for sel in selectors:
                try:
                    locator = page.locator(sel).first
                    locator.wait_for(timeout=9000)
                    download_button = locator
                    logger.info(f"Found download button using: {sel}")
                    break
                except:
                    pass

            if not download_button:
                raise RuntimeError("Could not find the Download button.")

            # 7. Download the file
            with page.expect_download() as dl_info:
                logger.info("Clicking download button…")
                download_button.click()

            dl = dl_info.value
            output_path = self.output_dir / dl.suggested_filename
            dl.save_as(output_path)

            logger.info(f"Saved → {output_path}")

            browser.close()
