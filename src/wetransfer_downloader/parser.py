import re
import json
import logging

logger = logging.getLogger(__name__)

TRANSFER_JSON_REGEX = re.compile(
    r"window\.transfer\s*=\s*(\{.*?\});",
    re.DOTALL
)

def extract_direct_urls(html_text: str):
    """
    Extract real direct file download URLs from WeTransfer download page.
    Looks ONLY for the window.transfer JSON object.
    """

    match = TRANSFER_JSON_REGEX.search(html_text)
    if not match:
        logger.error("Could not find embedded transfer JSON.")
        return []

    try:
        data = json.loads(match.group(1))
    except Exception as e:
        logger.error(f"Failed to parse transfer JSON: {e}")
        return []

    files = data.get("files", [])
    urls = []

    for f in files:
        # Direct link is inside "direct_link" or "url"
        if "direct_link" in f:
            urls.append(f["direct_link"])
        elif "url" in f:
            urls.append(f["url"])
        else:
            logger.warning(f"No direct link found for file: {f}")

    logger.info(f"Extracted {len(urls)} REAL file URL(s).")
    return urls
