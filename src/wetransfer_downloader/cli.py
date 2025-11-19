import argparse
from .downloader import WeTransferDownloader
from .logging_config import setup_logging

def main():
    setup_logging()

    parser = argparse.ArgumentParser(description="WeTransfer Downloader")
    parser.add_argument("url", help="WeTransfer link")
    args = parser.parse_args()

    downloader = WeTransferDownloader(
        output_dir="downloads",
        headless=True
    )

    downloader.download(args.url)
